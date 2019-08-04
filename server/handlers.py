import json
import logging
from protocol import validate_request, make_response
from actions import resolve
from middlewares import compression, encryption


@compression
@encryption
def handle_default_request(bytes_request):

    message = json.loads(bytes_request.decode())

    if validate_request(message):
        actions_name = message.get('action')
        controller = resolve(actions_name)
        if controller:

            try:
                logging.info(
                    f'Valid client was identified with the following message: {message}'
                )
                response = controller(message)
            except Exception as err:
                logging.critical(f'Internal server error: {err}')
                response = make_response(message, 500, data='Internal Server Error')

        else:
            logging.error(f'Controller with action name {actions_name} does not exist.')
            response = make_response(message, 404, 'Action not found')

    else:

        logging.error('Invalid request{}'.format(message))
        response = make_response(message, 404, 'Wrong request')

    response = json.dumps(response).encode()

    return response
