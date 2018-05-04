# [Pwn 300] Hexalicious

## How It Works

If the user inputs `0` at the menu, then the format string given to the next call to `sscanf()` will be read from OOB of the formats array. This will cause the user's `name` to be used as the format string for `sscanf()`. As the data being scanned is read onto the stack, a high argument index such as `%29$x` will cause data in the input string to be used as the address to write to. This can be used as a write-what-where primitive. By overwriting the global `data` pointer, this can lead to a read-anywhere primitive as well, which can be used to read the contents of the global `flag` buffer.

## Building

* PwnableHarness

## Deployment

* PwnableHarness

## Maintenance

* PwnableHarness
