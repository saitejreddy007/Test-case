import pytest
from app import app, db, Calculation

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

@pytest.fixture(autouse=True)
def run_around_tests():
    with app.app_context():
        yield
        db.session.remove()
        db.drop_all()


def test_calculate_tax(client):
    response = client.post('/calculate', json={'type': 'tax', 'amount': 100})
    assert response.status_code == 200
    assert response.json['result'] == 20.0


def test_calculate_discount(client):
    response = client.post('/calculate', json={'type': 'discount', 'amount': 100})
    assert response.status_code == 200
    assert response.json['result'] == 10.0


def test_calculate_invalid_type(client):
    response = client.post('/calculate', json={'type': 'invalid', 'amount': 100})
    assert response.status_code == 400
    assert 'error' in response.json