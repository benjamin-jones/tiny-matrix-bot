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

channel.queue_declare(queue=message_q, durable=True)
channel.basic_qos(prefetch_count=1)

def callback(ch, method, properties, body):
    global server
    
    message = bytes(str(body),'utf-8')
    server.sendall(message)
    server.close()

    time.sleep(body.count(b'.'))
    print(" [x] Done")
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_consume(callback,
                      queue=message_q)





