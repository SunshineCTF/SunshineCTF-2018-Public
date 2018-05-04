The challenge is figuring out the correct order of the base-64 string that decodes to the flag.

The program takes in a "password". This password is the order in which to run the functions. 
Each function return a hex value that represents 4 characters of the base64 string. 
(For example: 03041114 would run the 3rd, then 4th, then 11th, then 14th function)

The program then does an operation on the function and compares it to a value. 
This value is the value you would get if you entered the correct password.
When the correct password is entered, the program displays an access granted statement.

The base64 string of the flag is: 
c3Vue21ZX0lEQV9iUjFuZ1NfYTExX1RoM19CMHlzX3QwX3RIM195NHJEfQ==

The correct password is:
041302061503101411120501090708