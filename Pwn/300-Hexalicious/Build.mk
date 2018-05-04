TARGET := hexalicious

NX := 1
RELRO := partial

# Docker configuration
DOCKER_IMAGE := hexalicious
DOCKER_RUN_ARGS := --read-only
DOCKER_PORTS := 20003

# Only the binary is available for download
PUBLISH := $(TARGET)
