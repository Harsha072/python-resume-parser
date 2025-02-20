

import json
import pika
import os
import tempfile

from spellchecker import SpellChecker
from src.parser.textextract import extract_text_from_pdf
from src.config.settings import settings



def detect_typos(text):
        spell = SpellChecker()
        # Split the text into words and check for misspellings
        misspelled = spell.unknown(text.split())
        return list(misspelled)  # Return a list of misspelled words

def send_feedback(ch, feedback):
            # Send feedback to the feedback queue
         ch.basic_publish(
                    exchange="",
                    routing_key=settings.feedback_queue,
                    body=json.dumps(feedback).encode("utf-8")
        )
         
def callback(ch, method, properties, body):
        try:
            print(f"hello", properties.correlation_id)

            # Create a temporary file to store the binary data
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                temp_file.write(body) 
                print(temp_file); # Write the binary data to the file
                temp_file_path = temp_file.name  # Get the path to the temporary file

            print(f"Temporary file created at: {temp_file_path}")

            # Open the temporary file in binary mode and parse it
            with open(temp_file_path, "rb") as file:
                text = text_extract(file)
                print("Parsed id:", text)
                typos = detect_typos(text)
            feedback = {
                "resumeId":properties.correlation_id,
                "parsed_text": text,
                "typos": typos,
                "status": "success" if not typos else "typos_found"
            }

            # Send feedback to Spring Boot via RabbitMQ
            send_feedback(ch, feedback)

        except Exception as e:
            print(f"Error processing resume: {e}")
             
            feedback = {
                "error": str(e),
                "status": "error"
            }
            send_feedback(ch, feedback)
        finally:
            # Clean up: Delete the temporary file
            remove(temp_file_path)

            # Acknowledge the message
            ch.basic_ack(delivery_tag=method.delivery_tag)

def text_extract(file):
    return extract_text_from_pdf(file)

def remove(temp_file_path):
    if os.path.exists(temp_file_path):
        os.remove(temp_file_path)
        print(f"Deleted temporary file: {temp_file_path}")


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
    

    # # Start consuming messages
    channel.basic_consume(queue=settings.rabbitmq_queue, on_message_callback=callback)
    print("Waiting for messages. To exit, press CTRL+C")
    channel.start_consuming()