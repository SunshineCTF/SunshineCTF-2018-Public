TARGET := bookwriter

BITS := 32
CANARY := 1
NX := 1
ASLR := 1
DEBUG := 1
UBUNTU_VERSION := 16.04

DOCKER_IMAGE := sun18-bookwriter
DOCKER_PORTS := 18006
DOCKER_TIMELIMIT := 30

PUBLISH_BUILD := $(TARGET)
PUBLISH := bookwriter.c
PUBLISH_LIBC := $(TARGET)-libc.so

# `pwnmake check`: run the exploit and verify it prints the flag
$(call ctf_check,$(DIR),$(DOCKER_PORTS),python3 bookwriter.py)
