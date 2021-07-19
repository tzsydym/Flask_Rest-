import json
from app import app
from user_DAO import UserDAOMongo
import pytest

user_dao_mongo = UserDAOMongo()
data_id = 10001
user_name = "Test User"
user_name_updated = "Test User 2"
user_data = {
        "_id": data_id,
        "name": user_name,
        "dob": "1234",
        "address": {"longitude":000,"latitude":111},
        "description": "test user",
        "createdAt": ""
    }
##########################################################
# Test DAO
##########################################################
@pytest.mark.parametrize("user_dao", [user_dao_mongo])
def test_user_create_update_delete_get(user_dao):
    # Insert
    inserted_id = user_dao.create(user_data)
    assert inserted_id is not None
    # Get All
    users_fetched = user_dao.get_all()
    assert len(users_fetched) > 0
    # Get
    user_fetched = user_dao.get(user_name)
    assert user_fetched is not None
    # update
    updated_count = user_dao.update(user_name, {"name": user_name_updated})
    assert updated_count == 1
    # Get
    user_fetched = user_dao.get(user_name_updated)
    assert user_fetched is not None
    # Delete
    delete_count = user_dao.delete(user_name_updated)
    assert delete_count == 1
    # Get
    user_fetched = user_dao.get(user_name)
    assert user_fetched is None
    # Get
    user_fetched = user_dao.get(user_name_updated)
    assert user_fetched is None

##########################################################
# Test REST
##########################################################

@pytest.fixture
def client():
    client = app.test_client()
    return client

def _get_response_data_as_dict(response):
    return json.loads(response.data.decode('utf8'))

def test_creat():
    response = app.test_client().post('/api/v0.0/users', data=json.dumps({"user": user_data}),
                           content_type='application/json')
    assert response.status_code == 201
    assert 'inserted_id' in _get_response_data_as_dict(response).keys()

def test_get_all():
    response = app.test_client().get('/api/v0.0/users')
    assert len(_get_response_data_as_dict(response)) > 0

def test_get():
    response = app.test_client().get('/api/v0.0/users/{}'.format(user_name))
    assert response.status_code == 200
    assert _get_response_data_as_dict(response)['name'] == user_name

def test_update():
    response = app.test_client().put(
        '/api/v0.0/users/{}'.format(user_name),
        data=json.dumps({"user":{
            "_id": data_id,
            "name": user_name_updated,
            "dob": "4321",
            "address": {"longitude":123,"latitude":456},
            "description": "test user 2"
        }}),
        content_type='application/json')
    assert response.status_code == 201
    assert 'matched_count' in _get_response_data_as_dict(response).keys()

def test_delete():
    response = app.test_client().delete(
        '/api/v0.0/users/{}'.format(user_name_updated),
        content_type='application/json')
    assert response.status_code == 204
    assert '' == response.data.decode('utf-8')
