#!/bin/bash
mkdir -p sockets
mkdir -p data
ln -s ../matrix-python-sdk/matrix_client

python3 tiny-matrix-bot.py ../tiny-matrix-bot.cfg &
sleep 5
python3 rabbitmq-responder.py &
