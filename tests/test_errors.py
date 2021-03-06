import pytest


def test_abort_422(client):
    response = client.get('/abort_422')
    assert response.get_json() == {'error_code': 'some_422'}


def test_app_specific_exception(client):
    response = client.get('/raise_app_specific_exception')
    assert response.get_json() == {
        'error_code': 'my_custom_exception',
    }


def test_unexpected_exception_propagation(client):
    with pytest.raises(ValueError, match='foo'):
        client.get('/raise_unexpected_exception')


def test_unexpected_exception(client, monkeypatch):
    from example.app import app
    monkeypatch.setattr(app, 'testing', False)  # disable exception propagation for this test

    response = client.get('/raise_unexpected_exception')
    assert response.get_json() == {
        'error_code': 'custom_error',
        'error_type': "<class 'ValueError'>",
    }


def test_validation_error(client):
    response = client.get('/webargs_validation', data={'number': 'foobar'})
    assert response.get_json() == {
        'error_code': 'webargs_422',
        'messages': {'number': ['Not a valid number.']},
    }
