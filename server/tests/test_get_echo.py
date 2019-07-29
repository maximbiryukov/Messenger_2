import pytest
import time

from echo.controllers import get_echo

@pytest.fixture
def expected_action():
    return 'echo'


@pytest.fixture
def expected_code():
    return 200


@pytest.fixture
def expected_data():
    return 'Echo, bitch'


@pytest.fixture
def expected_request(expected_action, expected_data):
    return {
        'action': expected_action,
        'time': time.ctime(),
        'data': expected_data
    }

def test_action_get_echo(expected_request):
    actual_response = get_echo(expected_request)
    assert actual_response.get('action') == 'echo'


def test_code_get_echo(expected_request):
    actual_response = get_echo(expected_request)
    assert actual_response.get('code') == 200


def test_data_get_echo(expected_request):
    actual_response = get_echo(expected_request)
    assert actual_response.get('data') == 'Echo, bitch'