import pytest
from models import models
from app import app, db


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200


def test_add(client):
    test_data = {
        'name': 'Mickey Test',
        'gender': 'male',
        'address': 'IN',
        'phone': '0123456789',
        'salary': '2000',
        'department': 'Sales'
    }
    response = client.post('/add', data=test_data)
    assert response.status_code == 200
    with app.app_context():
        assert models.Employee.query.count() == 1


def test_edit(client):
    response = client.post('/edit/0')
    assert response.status_code == 200
    assert b"Sorry, the employee does not exist." in response.data


def test_delete(client):
    test_data = {'emp_id': 0}
    response = client.post('/delete', data=test_data)
    assert response.status_code == 200
    assert b"Sorry, the employee does not exist." in response.data
