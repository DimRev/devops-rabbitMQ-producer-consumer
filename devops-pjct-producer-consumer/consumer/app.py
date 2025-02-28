import pika
import logging
import sys
import argparse
import os
from argparse import RawTextHelpFormatter
from time import sleep

with open('version', 'r') as f:
    VERSION = f.read().strip()
    print(f"Starting consumer.py, {VERSION}")


def on_message(channel, method_frame, header_frame, body):
    print(method_frame.delivery_tag)
    print(body.decode())
    LOG.info('Message has been received %s', body.decode())
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)

def main():
    examples = f"{sys.argv[0]} -p 5672 -s rabbitmq"
    parser = argparse.ArgumentParser(
        formatter_class=RawTextHelpFormatter,
        description='Run consumer.py',
        epilog=examples
    )
    parser.add_argument('-p', '--port', action='store', dest='port',
                        help='The port to listen on.')
    parser.add_argument('-s', '--server', action='store', dest='server',
                        help='The RabbitMQ server.')

    args = parser.parse_args()
    if args.port is None:
        print("Missing required argument: -p/--port")
        sys.exit(1)
    if args.server is None:
        print("Missing required argument: -s/--server")
        sys.exit(1)

    # Sleep a few seconds to allow RabbitMQ server to come up
    sleep(5)
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    global LOG
    LOG = logging.getLogger(__name__)

    # Fetch credentials from environment variables with defaults
    username = os.environ.get("RABBITMQ_DEFAULT_USER", "user")
    password = os.environ.get("RABBITMQ_DEFAULT_PASS", "password")
    credentials = pika.PlainCredentials(username, password)

    parameters = pika.ConnectionParameters(
        args.server,
        int(args.port),
        '/',
        credentials
    )
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.queue_declare(queue='pc')
    channel.basic_consume(
        queue='pc',
        on_message_callback=on_message
    )

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    connection.close()

if __name__ == '__main__':
    main()
