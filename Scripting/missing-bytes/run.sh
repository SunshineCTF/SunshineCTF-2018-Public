#!/bin/bash

socat tcp4-l:30001,reuseaddr,fork EXEC:"./server.py",pty,ctty,echo=0