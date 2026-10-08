TARGET := logsearch

BITS := 32
CANARY := 1
NX := 1
DEBUG := 1
UBUNTU_VERSION := 16.04

DOCKER_IMAGE := sun18-logsearch
DOCKER_PORTS := 18002
DOCKER_TIMELIMIT := 30

PUBLISH_BUILD := $(TARGET)
PUBLISH := logsearch.c

# `pwnmake check`: run the exploit and verify it prints the flag
$(call ctf_check,$(DIR),$(DOCKER_PORTS),python3 logsearch.py)
