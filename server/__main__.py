import socket
import json
import time
from protocol import validate_request, make_response
from actions import resolve

from argparse import ArgumentParser


parser = ArgumentParser()

parser.add_argument('-c', '--config', type=str, required=False, help='Sets config file path')

args = parser.parse_args()

config = {'host': 'localhost', 'port': 8000, 'buffersize': 1024}

if args.config:
    with open(args.config) as file:
        file_config = json.load(file)
        config.update(file_config)

host, port = config.get('host'), config.get('port')


try:
    sock = socket.socket()
    sock.bind((host, port))
    sock.listen(5)

    print("server started with {}:{} at {}".format(host, port, time.ctime()))

    while True:
        client, address = sock.accept()
        print('Client was detected {}:{} at {} '.format(address[0], address[1], time.ctime()))

        b_request = client.recv(config.get('buffersize')) # принимаем сообщение клиента

        message = json.loads(b_request.decode())

        if validate_request(message):
            actions_name = message.get('action')
            controller = resolve(actions_name)
            if controller:

                try:
                    print('Valid client was identified as {}. Request sent: {}'.format(message['user']['account_name'], message))
                    response = controller(message)
                except Exception as err:
                    print(f'Internal server error: {err}')
                    response = make_response(message, 500, data='Internal Server Error')

            else:
                print(f'Controller with action name {actions_name} does not exist.')
                response = make_response(message, 404, 'Action not found')

        else:

            print('Invalid request{}'.format(message))
            response = make_response(message, 404, 'Wrong request')

        client.send(json.dumps(response).encode())

        client.close()

except KeyboardInterrupt:
    print()
    print('Server was shut down')