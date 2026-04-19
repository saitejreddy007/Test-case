import pytest
from app import app, db, TaxCalculation

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

@pytest.fixture
def init_database():
    with app.app_context():
        db.create_all()
    yield
    with app.app_context():
        db.drop_all()

def test_calculate_tax(client, init_database):
    response = client.post('/calculate_tax', json={'amount': 100, 'tax_rate': 15})
    json_data = response.get_json()
    assert response.status_code == 200
    assert json_data['tax_amount'] == 15.0

    response = client.post('/calculate_tax', json={'amount': 200, 'tax_rate': 10})
    json_data = response.get_json()
    assert response.status_code == 200
    assert json_data['tax_amount'] == 20.0

    response = client.post('/calculate_tax', json={'amount': 100})
    assert response.status_code == 400
    assert response.get_json() == {'error': 'Amount and tax rate are required'}