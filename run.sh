#!/bin/bash
mkdir -p sockets
ln -s ../matrix-python-sdk/matrix_client

python3 tiny-matrix-bot.py tiny-matrix-bot.cfg
