import json
from http import HTTPStatus

import pytest

def add_task_view(session,test_client):
    # Check for valid data if all the fields are present
    data = {"number":4}
    response = test_client.post('http://localhost:5000/api/tasks',data = json.dumps(data) ,content_type='application/json')
    response_data = response.get_json()
    assert response.status_code == 201
    assert len(response_data.keys()) == 3
    assert 'task_id' in response_data
    assert 'status' in response_data
    assert 'result' in response_data
    assert response_data['result'] == None

    # Check for invalid data if correct error messages are shown
    # the below is true for negative numbers also
    data = {"number":0}
    response = test_client.post('http://localhost:5000/api/tasks',data = json.dumps(data) ,content_type='application/json')
    errors = response.get_json()
    assert len(errors.keys()) == 2
    assert response.status_code == 400

    # Check error message for invalid string input
    data = {"number":"abcd"}
    response = test_client.post('http://localhost:5000/api/tasks',data = json.dumps(data) ,content_type='application/json')
    errors = response.get_json()
    assert len(errors.keys()) == 2
    assert response.status_code == 400

def get_task_status_view(session, test_client):
    # Check for valid data if all the fields are present
    data = {"number":5}
    response_post = test_client.post('http://localhost:5000/api/tasks',data = json.dumps(data) ,content_type='application/json')
    response_data = response_post.get_json()

    response = test_client.get('http://localhost:5000/api/tasks/'+response_data['task_id'])
    response_data_get = response.get_json()
    assert len(response_data_get) == 3
    assert response.status_code == 200
    assert len(response_data_get.keys()) == 3
    assert 'task_id' in response_data_get
    assert 'status' in response_data_get
    assert 'result' in response_data_get
    assert response_data_get['result'] in ["PENDING","SUCCESS"]

    # Invalid task id
    task_id = "1"
    response = test_client.get('http://localhost:5000/api/tasks/'+ task_id)
    assert response.status_code == 400
    assert len(response.keys()) == 2
    assert response['message'] == "Given task id does not exist in database"

