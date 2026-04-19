import pytest
from app import app, db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_calculate_discount(client):
    response = client.post('/calculate_discount', json={'amount': 100, 'discount_rate': 10})
    assert response.status_code == 200
    assert response.json['discount_amount'] == 10.0

    response = client.post('/calculate_discount', json={'amount': 200, 'discount_rate': 25})
    assert response.status_code == 200
    assert response.json['discount_amount'] == 50.0

    response = client.post('/calculate_discount', json={'amount': 100, 'discount_rate': -10})
    assert response.status_code == 400
    assert 'error' in response.json

    response = client.post('/calculate_discount', json={'amount': -100, 'discount_rate': 10})
    assert response.status_code == 400
    assert 'error' in response.json

    response = client.post('/calculate_discount', json={})
    assert response.status_code == 400
    assert 'error' in response.json