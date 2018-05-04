# [Reversing 100] Source Protection
The goal for this challenge is to get the source code of a python script that has been compiled using pyinstaller.

## How it works
The python script is supposed to be a password manager, it takes in a secret phrase and if the phrase is correct it will return all of the stored passwords. This script has been compiled using pyinstaller, which is a tool that compiles python code so that you can easily distribute it.

## How to solve it
### Method one:
1. Run the program
2. Take a memory dump of the program while its running
3. Extract the pyc file from the memory dump
4. Use pyREtic or uncompyle to turn the pyc back into python source
5. Find the flag in the source

### Method two:
1. Use google, find the tool pyinstextractor
2. Use pyinstextractor to extract the the contents of the PYZ from the exe
3. Add the pyc header to the "passwords" file in the extracted folder
4. Use pyREtic or uncompyle to get the source from the pyc
4. OR you can just run strings on the extracted folder

