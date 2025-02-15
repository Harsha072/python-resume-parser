

import pika
import os
import tempfile
from parser.textextract import extract_text_from_pdf
from config.settings import settings

def start_consumer():
    print(settings.rabbitmq_host)
    #Connect to RabbitMQ
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
            print(f"hello")

            # Create a temporary file to store the binary data
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                temp_file.write(body)  # Write the binary data to the file
                temp_file_path = temp_file.name  # Get the path to the temporary file

            print(f"Temporary file created at: {temp_file_path}")

            # Open the temporary file in binary mode and parse it
            with open(temp_file_path, "rb") as file:
                text = extract_text_from_pdf(file)
                print("Parsed Data:", text)

        except Exception as e:
            print(f"Error processing resume: {e}")
        finally:
            # Clean up: Delete the temporary file
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
                print(f"Deleted temporary file: {temp_file_path}")

            # Acknowledge the message
            ch.basic_ack(delivery_tag=method.delivery_tag)

    # # Start consuming messages
    channel.basic_consume(queue=settings.rabbitmq_queue, on_message_callback=callback)
    print("Waiting for messages. To exit, press CTRL+C")
    channel.start_consuming()