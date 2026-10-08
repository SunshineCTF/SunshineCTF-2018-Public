TARGET := rot13

BITS := 32
ASLR := 1
NX := 1
CANARY := 1
UBUNTU_VERSION := 16.04

DOCKER_IMAGE := sun18-rot13
DOCKER_PORTS := 18003
DOCKER_TIMELIMIT := 30

PUBLISH_BUILD := $(TARGET)
PUBLISH_LIBC := $(TARGET)-libc.so

# `pwnmake check`: run the exploit and verify it prints the flag
$(call ctf_check,$(DIR),$(DOCKER_PORTS),python3 rot13.py)
