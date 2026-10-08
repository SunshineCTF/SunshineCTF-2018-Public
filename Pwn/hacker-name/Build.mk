TARGET := hacker-name

BITS := 32
NX := 1
UBUNTU_VERSION := 16.04

DOCKER_IMAGE := sun18-hacker-name
DOCKER_PORTS := 18001
DOCKER_TIMELIMIT := 30

PUBLISH_BUILD := $(TARGET)

# `pwnmake check`: run the exploit and verify it prints the flag
$(call ctf_check,$(DIR),$(DOCKER_PORTS),python3 solve.py)
