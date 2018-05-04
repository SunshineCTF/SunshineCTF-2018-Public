# [Pwn 300] UAF

Simple heap UAF.

## How It Works

When the user connects to the service, they are presented with a menu of choices such as create/display/delete arrays of integers and text strings. When an object is created, its "id", which is actually its pointer, is displayed. Object types are checked, so this isn't a type confusion challenge. However, after an object is deleted, the user may still reference its id to trigger a UAF bug.

The trick for this one is to create an integer array, then delete it, then create a text string with the correct size and crafted contents to be allocated in the same address as the deleted integer array structure. By controlling the `intArr->ints` pointer and then editing the integer array, the user can write arbitrary data to an arbitrary address. The chosen exploitation route in this case is to replace `free.got` with the address of `system()` in libc, and then delete a text string containing the text `/bin/sh`.

This exploit is made a little tricker because of how the integer array structure is overwritten. As the memory contents must be a C string, the user can't write data containing null bytes. That means the `intArr->count` value must be insanely large to not contain any null bytes. The problem here is that when trying to read the contents of the array, it reads the entire array. With a ridiculously large value for count, this is almost certain to crash. To avoid this problem, two integer array objects, `arr1` and `arr2` can be created. The `arr1` array is created with a single element so its count is 1. Then, `arr2` is deleted and replaced with a text string that sets `arr2->count` to a ridiculously large value (to avoid null bytes) and `arr2->ints` to `&arr1->ints`. Then, `arr2` is edited, and the integer at index 0 is replaced with the desired address to read. This sets `arr1->ints` to the read address. Following this, `arr1` is displayed, which reads the data from the controlled address, giving the user a read-anywhere primitive. After this, they can now edit this array to perform a write-what-where primitive, which is used to replace `free.got` with the address of `system()` in libc. Finally, we delete a text string object containing the contents `/bin/sh` to get a shell.

See included [`uaf.py`](uaf.py) exploit script for complete technical details.

## Deployment

PwnableHarness

## Maintenance

PwnableHarness
