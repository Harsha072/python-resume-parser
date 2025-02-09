

import pika
from parser.textextract import extract_text_from_pdf
from parser.nlpprocessor import process_text
from config.settings import settings

def start_consumer():
    # Connect to RabbitMQ
    credentials = pika.PlainCredentials(settings.rabbitmq_username, settings.rabbitmq_password)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=settings.rabbitmq_host, port=settings.rabbitmq_port, credentials=credentials)
    )
    channel = connection.channel()

    # Declare the queue
    channel.queue_declare(queue=settings.rabbitmq_queue, durable=True)

    # Define the callback function
    def callback(ch, method, properties, body):
        try:
            # Parse the resume
            file_path = body.decode()  # Assume the message contains the file path
            with open(file_path, "rb") as file:
                text = extract_text_from_pdf(file)
                # parsed_data = process_text(text)
                print("Parsed Data:", text)
        except Exception as e:
            print(f"Error processing resume: {e}")
        finally:
            ch.basic_ack(delivery_tag=method.delivery_tag)

    # Start consuming messages
    channel.basic_consume(queue=settings.rabbitmq_queue, on_message_callback=callback)
    print("Waiting for messages. To exit, press CTRL+C")
    channel.start_consuming()