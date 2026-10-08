TARGET := hexalicious

BITS := 32
NX := 1
RELRO := partial
UBUNTU_VERSION := 16.04

DOCKER_IMAGE := sun18-hexalicious
DOCKER_PORTS := 18004
DOCKER_TIMELIMIT := 30

PUBLISH_BUILD := $(TARGET)

# `pwnmake check`: run the exploit and verify it prints the flag
$(call ctf_check,$(DIR),$(DOCKER_PORTS),python3 hexalicious.py)
