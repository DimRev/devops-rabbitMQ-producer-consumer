import pika
import logging
import sys
import argparse
from argparse import RawTextHelpFormatter
from time import sleep
import os

def main():
    examples = f"{sys.argv[0]} -p 5672 -s rabbitmq -m 'Hello'"
    parser = argparse.ArgumentParser(
        formatter_class=RawTextHelpFormatter,
        description='Run producer.py',
        epilog=examples
    )
    parser.add_argument('-p', '--port', action='store', dest='port',
                        help='The port to listen on.')
    parser.add_argument('-s', '--server', action='store', dest='server',
                        help='The RabbitMQ server.')
    parser.add_argument('-m', '--message', action='store', dest='message',
                        help='The message to send', required=False, default='Hello')
    parser.add_argument('-r', '--repeat', action='store', dest='repeat',
                        help='Number of times to repeat the message', required=False, default='30')

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
    LOG = logging.getLogger(__name__)

    # Use environment variables if provided, otherwise default to 'user' and 'password'
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

    q = channel.queue_declare(queue='pc')
    q_name = q.method.queue

    # Turn on delivery confirmations
    channel.confirm_delivery()

    for i in range(int(args.repeat)):
        if channel.basic_publish('', q_name, args.message.encode()):
            LOG.info('Message has been delivered')
        else:
            LOG.warning('Message NOT delivered')
        sleep(2)

    connection.close()

if __name__ == '__main__':
    main()
