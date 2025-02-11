import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='my_queue')

messages = ["это первое", "а это второе", "а это третье"]

for message in messages:
    channel.basic_publish(exchange='', routing_key='my_queue', body=message)
    print(f" [x] Отправлено: {message}")

connection.close()