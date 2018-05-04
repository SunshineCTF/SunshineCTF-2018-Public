TARGET := logsearch

CANARY := 1
NX := 1
DEBUG := 1

DOCKER_IMAGE := logsearch
DOCKER_PORTS := 20008
DOCKER_RUN_ARGS := --read-only

PUBLISH := $(TARGET) logsearch.c
