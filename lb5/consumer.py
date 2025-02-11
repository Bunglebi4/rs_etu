import pika

def callback(ch, method, properties, body):
    print(f" [x] Получено: {body.decode()}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='my_queue')

channel.basic_consume(queue='my_queue', on_message_callback=callback, auto_ack=False)

print(' [*] Ожидание сообщений. Для выхода нажмите CTRL+C')
channel.start_consuming()