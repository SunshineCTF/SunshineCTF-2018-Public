# [Pwn 500] BookWriter

Heap UAF and doubly-linked list corruption.

## How It Works

Players are presented with a menu of choices upon connecting to the service. They can insert a new page, delete the current page, and flip to the previous or next page. When the menu is displayed, it prints the page's address as the "page number", which serves as an information leak. As the "first" page is `g_cover`, a global variable, the first page number points within the `bookwriter` executable, allowing players to locate it in memory as ASLR is enabled.

The main vulnerability is that when the current page is deleted, `book->current_page` still points to the page that was just freed. This dangling pointer causes a UAF vulnerability when a new page is inserted directly after deleting a page. Due to the order of the allocations and frees, the user can control the contents of the `book->current_page` structure when inserting a new page. This gives the user some control over the program.

By controlling the contents of a page structure, the user can read arbitrary data by pointing the `page->text` pointer to the address the user wants to read. When the user flips to that page, its text content will be displayed as a C string, which will leak the memory contents until the next null byte.

The user can also control the previous (and maybe even next) pointer of a page structure, which means they can make `book->current_page` point to a page whose contents are completely controllable with the exception of null bytes. By deleting a carefully crafted page, the user may write a writeable memory address to another writeable memory address. This can be manipulated into arbitrary data writes.

To write arbitrary data to a chosen address, the user can create a 64k-aligned region of data of at least 64k bytes. This is so that no matter what the two low bytes of a pointer are, as long as the upper two bytes are the upper two of the 64k region, the pointer will point to writeable memory within the 64k region. As the write primitive we have is writing a writeable memory address to a writeable memory address, we can control the low 2 bytes of the address that's written to our target address to control some of the data. By doing a combination of this and unaligned writes, we can write completely controllable data. Example:

```
target = 0x56f08824 //*target is 0xXXXXXXXX)
value = 0xDEADBEEF
64k = 0xABCD0000

// Use write primitive
*target = 0xABCDBEEF //*target is now 0xABCDBEEF

// This will write an extra 2 bytes beyond target, but that's okay now
*(target + 2) = 0xABCDDEAD //*target is now 0xDEADBEEF
```

This technique for writing controllable data is used to replace `strncasecmp.got` with `&system` from libc. After this, the user selects choice 0 from the menu (to quit). The program will ask the user if they're sure they want to quit, and then their input is passed to the `strncasecmp()` function. However, as we've overwritten `strncasecmp()'s` GOT function pointer with the address of `system()`, it actually calls `system()` on our input at the `[y/N]` prompt. Therefore, we just enter `/bin/sh` at the prompt to get a shell.

See included [`bookwriter.py`](bookwriter.py) exploit script for complete technical details.

## Deployment

PwnableHarness

## Maintenance

PwnableHarness
