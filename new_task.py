#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue0', durable=True)
channel.queue_declare(queue='task_queue1', durable=True)
channel.queue_declare(queue='task_queue2', durable=True)


message = ' '.join(sys.argv[1:]) or "Hello World!"
#message = ' '.join(sys.argv[2:]) or "Hello World!"


print ("arg0 %s" % (sys.argv[0]))
print ("arg1 %s" % (sys.argv[1]))
#print ("arg2 %s" % (sys.argv[2]))


channel.basic_publish(exchange='',
                      routing_key='task_queue1',
                      #routing_key=sys.argv[1],
                      body=message,
                      properties=pika.BasicProperties(
                         delivery_mode = 2, # make message persistent
                      ))
print(" [x] Sent %r" % message)
connection.close()
