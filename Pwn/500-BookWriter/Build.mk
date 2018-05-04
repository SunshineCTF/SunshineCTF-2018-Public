TARGET := bookwriter

CANARY := 1
NX := 1
ASLR := 1
DEBUG := 1

DOCKER_IMAGE := bookwriter
DOCKER_PORTS := 20002
DOCKER_RUN_ARGS := --read-only

PUBLISH := $(TARGET) bookwriter.c
PUBLISH_LIBC := $(TARGET)-libc.so
