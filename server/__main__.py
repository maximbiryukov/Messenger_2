import socket
import json
import time
import logging
import select
import threading

from handlers import handle_default_request

from argparse import ArgumentParser


def read(socket,connections, requests, buffersize):
    try:
        bytes_request = socket.recv(buffersize)
    except Exception:
        connections.remove(socket)
    else:
        requests.append(bytes_request)


def write(socket, connections, response):
    try:
        write_client.send(response)
    except Exception:
        connections.remove(socket)


parser = ArgumentParser()

parser.add_argument('-c', '--config', type=str, required=False, help='Sets config file path')

args = parser.parse_args()

config = {'host': 'localhost', 'port': 8000, 'buffersize': 1024}

if args.config:
    with open(args.config) as file:
        file_config = json.load(file)
        config.update(file_config)


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers = [
        logging.FileHandler('main.log'),
        logging.StreamHandler()
    ]
)

connections = []
requests = []

host, port = config.get('host'), config.get('port')


try:
    sock = socket.socket()
    sock.bind((host, port))
    sock.settimeout(0)
    sock.listen(5)

    logging.info("server started with {}:{} at {}".format(host, port, time.ctime()))

    while True:
        try:
            client, address = sock.accept()
            logging.info('Client was detected {}:{} at {} '.format(address[0], address[1], time.ctime()))
            connections.append(client)
        except:
            pass

        rlist, wlist, xlist = select.select(
            connections, connections, connections, 0
        )

        for read_client in rlist:
            read_thread = threading.Thread(
                target=read,
                args=[read_client, connections, requests, config.get('buffersize')]
            )
            read_thread.start()

        if requests:
            bytes_request = requests.pop()
            bytes_response = handle_default_request(bytes_request)

            for write_client in wlist:
                write_thread = threading.Thread(
                    target=write,
                    args=[write_client, connections, bytes_response]
                )
                write_thread.start()

            for read_client in rlist:

                try:
                    read_client.send(bytes_response)
                except Exception:
                    connections.remove(read_client)


except KeyboardInterrupt:
    logging.info('Server was shut down')
