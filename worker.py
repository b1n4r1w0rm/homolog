#!/usr/bin/env python
import pika
import time
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue0', durable=True)
channel.queue_declare(queue='task_queue1', durable=True)
channel.queue_declare(queue='task_queue2', durable=True)

print(' [*] Waiting for messages. To exit press CTRL+C')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body[0:])
    time.sleep(body.count(b'.'))
    ch.basic_ack(delivery_tag = method.delivery_tag)
    #print(queue_name)
    #print(result)
    #print(body)
    #arra = []
    #arra = ''.join(body)
    arra=body
    z = arra.split()
    #print z[0]
    print z


channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback, queue='task_queue0')
channel.basic_consume(callback, queue='task_queue1')
channel.basic_consume(callback, queue='task_queue2')



try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()
connection.close()

