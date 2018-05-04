# [Pwn 50] Hacker Name

## How It Works

The user is prompted for their hacker name. This is a standard buffer overflow, where `scanf` is used to read in input larger than the allocated array. To solve, the name "hacker" must be appended after an input of length 7 is provided, as the variable `buffer` is being overflowed into, and is later `strcmp`'d to the string "hacker" in order to trigger `print_flag`.

## Building

* PwnableHarness

## Deployment

* PwnableHarness

## Maintenance

* PwnableHarness
