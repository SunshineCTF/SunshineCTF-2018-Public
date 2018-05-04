# [Pwn 200] Rot13

Printf format string exploitation.

## How It Works

Format string exploitation, made a little more difficult because the input is rot13-decoded before being passed to printf. Also, ASLR is enabled so the player has to leak both the executable's ASLR slide and the base address of libc. The exploit approach taken was to replace strlen() in the GOT with system() from libc to get a shell.

See included [`rot13.py`](rot13.py) exploit script for complete technical details.

## Deployment

PwnableHarness

## Maintenance

PwnableHarness
