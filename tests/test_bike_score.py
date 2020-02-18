from bike_score_app import create_app


def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


def test_hello(client):
    response = client.get('/bike_score')
    assert response.data == b'HELLO I AM THE TEMPLATE'
    
def test_register_validate_input(client):
    assert 'a' in 'a'