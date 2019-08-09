import zlib
import json
import socket
import time
import threading

from argparse import ArgumentParser

WRITE_MODE = 'write'
READ_MODE = 'read'


def read(socket, buffersize):
    while True:
        response = socket.recv(buffersize)
        bytes_response = zlib.decompress(response)
        str_response = bytes_response.decode()
        message = json.loads(str_response)['data']
        print(f'Received the following from the server: {message}')


def make_request(action_name, data):
    message = {
        "action": action_name,
        "time": time.ctime(),
        "data": data,
    }
    return message


parser = ArgumentParser()

parser.add_argument('-c', '--config', type=str, required=False, help='Sets config file path')

args = parser.parse_args()

config = {'host': '127.0.0.1', 'port': 8000, 'buffersize': 1024}

if args.config:
    with open(args.config) as file:
        file_config = json.load(file)
        config.update(file_config)

host, port, buffersize = config.get('host'), config.get('port'), config.get('buffersize')


try:
    sock = socket.socket()
    sock.connect((host, port))
    print(f'Connected to server at {time.ctime()}')

    read_thread = threading.Thread(
        target=read,
        args=[sock, config.get('buffersize')]
    )
    read_thread.start()

    while True:

        print('Action: ')
        action = input()
        print('Сообщение серверу:')
        data = input()
        message = make_request(action, data)

        request = json.dumps(message)
        bytes_request = zlib.compress(request.encode())

        sock.send(bytes_request)
        print(f'Sent the following to the server: {data}')
        time.sleep(1)

except KeyboardInterrupt:
    print()
    print('Client shut down')
