#!/usr/bin/env python3
# python3 port. For each generated filesystem, a corrupted folder is one whose
# reported size does not equal the sum of its direct children's sizes (the game
# inflates each corrupt folder and its ancestors equally, so only the corrupt
# folder itself fails the check). Traverse every directory with `ls <abspath>`,
# collect the mismatched folders, and `send` each.
import sys, os, re
from pwn import remote, context
context.log_level='error'
HOST=os.environ.get('HOST', sys.argv[1] if len(sys.argv)>1 else '127.0.0.1')
PORT=int(os.environ.get('PORT', sys.argv[2] if len(sys.argv)>2 else 18201))
io=remote(HOST,PORT)
io.recvuntil(b'to begin.'); io.sendline(b"start")
def ls(path):
    io.recvuntil(b"/: $ "); io.sendline(("ls "+path).encode())
    data=io.recvuntil(b"/: $ ",drop=True).decode()
    # drop the prompt we just consumed context; parse entry lines
    entries=[]
    for line in data.splitlines():
        m=re.match(r'^(\S+)\s+(DIR |FILE)\s+(\d+)\s*$', line)
        if m: entries.append((m.group(1), m.group(2).strip(), int(m.group(3))))
    io.unrecv(b"/: $ ")
    return entries
def solve_game():
    corrupt=[]
    def visit(path, children):
        for fname,ftype,size in children:
            child_path=(path.rstrip("/")+"/"+fname) if path!="/" else "/"+fname
            if ftype=="DIR":
                sub=ls(child_path)
                if sum(s for _,_,s in sub)!=size:
                    corrupt.append(child_path)
                visit(child_path, sub)
    root=ls("/")
    visit("/", root)
    for c in corrupt:
        io.recvuntil(b"/: $ "); io.sendline(("send "+c).encode())
        r=io.recvuntil([b"Correct!",b"incorrect"],timeout=5)
        if b"incorrect" in r:
            return False
    return True
for g in range(20):
    ok=solve_game()
    if not ok:
        print("FAILED at game",g); break
    io.recvuntil(b"Hooray")
else:
    data=io.recvall(timeout=5).decode(errors='replace')
    m=re.search(r'sun\{[^}]*\}', data)
    print(m.group(0) if m else "no flag:\n"+data[-200:])
