import zlib
import json
import socket
import time

from argparse import ArgumentParser

WRITE_MODE = 'write'
READ_MODE = 'read'


def make_request(action_name, data):
    message = {
        "action": action_name,
        "time": time.ctime(),
        "data": data,
    }
    return message


parser = ArgumentParser()

parser.add_argument('-c', '--config', type=str, required=False, help='Sets config file path')

parser.add_argument(
    '-m', '--mode', type=str, required=False, default=WRITE_MODE,
    help='sets client mode'
)

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

    while True:
        if args.mode == WRITE_MODE:
            print('Action: ')
            action = input()
            print('Сообщение серверу:')
            data = input()

            message = make_request(action, data)

            request = json.dumps(message)
            bytes_request = zlib.compress(request.encode())

            sock.send(bytes_request)

        elif args.mode == READ_MODE:
            print()
            print('Ждем сообщения от сервера...')
            print()

        b_response = sock.recv(buffersize)
        response = zlib.decompress(b_response).decode()

        print('Получено следующее сообщение: {}'.format(json.loads(response)['data']))  # Выводим ответ сервера

except KeyboardInterrupt:
    print()
    print('Client shut down')
