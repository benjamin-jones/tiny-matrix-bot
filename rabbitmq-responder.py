# -*- coding: utf-8 -*-
import socket
import os, os.path
import time
import pika
import sys

from collections import deque    


socketfile = "./sockets/NKiOUeCkGiPmCPlSFD"
message_q = "boris_chat_tx_q"

if not os.path.exists(socketfile):
    print("No socket found")
    exit(2)

server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
server.connect(socketfile)

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='bots', exchange_type='fanout', durable=False)

result = channel.queue_declare(queue=message_q, durable=True)
channel.queue_bind(exchange='bots', queue=result.method.queue)

def callback(ch, method, properties, body):
    global server

    if len(body) > 1:
        body = body.decode('utf-8')
        message = bytes(str(body),'utf-8')
        server.sendall(message)

        server.close()
        time.sleep(3)

        server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        server.connect(socketfile)


channel.basic_consume(callback, queue=message_q, no_ack=True)
channel.start_consuming()
server.close()
