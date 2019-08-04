import zlib
from functools import wraps


def compression(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        bytes_request = zlib.decompress(request)
        bytes_response = func(bytes_request, *args, **kwargs)
        return zlib.compress(bytes_response)
    return wrapper


def encryption(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        bytes_response = func(request, *args, **kwargs)
        return bytes_response
    return wrapper
