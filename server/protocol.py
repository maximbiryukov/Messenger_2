import time


def validate_request(request):
    if 'action' in request and 'time' in request:
        return True
    else:
        False


def make_response(request, code, data=None):
    return {
        'action': request.get('action'),
        'time': time.ctime(),
        'code': code,
        'data': data
    }
