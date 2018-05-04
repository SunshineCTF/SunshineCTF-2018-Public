# [Crypto 100] Visionary

## How to solve

This is a simple vigenere with a specified table.
from the table we can identify that the range of ascii values are from 33 to 126.
this gives us a range of 94 and an offset of 33 from this information we can write
an algorithm that we can use to recover the key. once we have the key we will
be able to use a similar algorithm to the final message, the flag!
