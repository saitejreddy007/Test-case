import pytest
from app import app, db

@pytest.fixture(scope='module')
def test_client():
    with app.test_client() as client:
        yield client

@pytest.fixture(scope='module', autouse=True)
def init_database():
    with app.app_context():
        db.create_all()
        yield
        db.drop_all()


def test_hello(test_client):
    response = test_client.get('/hello')
    assert response.status_code == 200
    assert response.json == {'message': 'Hello, World!'}