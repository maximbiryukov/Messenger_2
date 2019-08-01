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


def test_action_get_echo(expected_request, expected_action):
    actual_response = get_echo(expected_request)
    assert actual_response.get('action') == expected_action


def test_code_get_echo(expected_request, expected_code):
    actual_response = get_echo(expected_request)
    assert actual_response.get('code') == expected_code


def test_data_get_echo(expected_request, expected_data):
    actual_response = get_echo(expected_request)
    assert actual_response.get('data') == expected_data