import os
import pytest

from unittest.mock import patch
from app.test.fixtures import client, app, async_client
from app.utils.app_exceptions import AppException
from app.settings import basedir

async def fake_handle_import(self, file, background_tasks):
    return {"message": "there you go!"}

@pytest.mark.anyio
@patch('app.task.service.TaskService.handle_data_upload')
async def test_import_data_success(handle_data_upload_mock, async_client):
    expected_msg = 'upload successfully'
    handle_data_upload_mock.return_value = expected_msg
    _test_upload_file = os.path.join(basedir, 'task/mock_data/test_us-census-income.csv')
    _files = {'file': open(_test_upload_file, 'rb')}

    resp = await async_client.post(
        "/api/v1/tasks/uploaddata",
        files=_files,
    )
    assert resp.status_code == 202
    assert resp.json()["message"] == expected_msg

@pytest.mark.anyio
@patch('app.task.service.TaskService.handle_data_upload', autospec=True)
async def test_import_data_invalid_file(handle_data_upload_mock, async_client):
    expected_exception_msg = 'failed to process, invalid file'
    handle_data_upload_mock.side_effect = AppException(expected_exception_msg)
    _test_upload_file = os.path.join(basedir, 'task/mock_data/test_us-census-income.csv')
    _files = {'file': open(_test_upload_file, 'rb')}

    resp = await async_client.post(
        "/api/v1/tasks/uploaddata",
        files=_files,
    )
    assert resp.status_code == 400
    assert resp.json()["message"] == expected_exception_msg

@patch('app.task.service.TaskService.retrieve_data')
def test_get_task_success(retrieve_data_mock, client):
    test_task_data = {
        "index": [1, 2],
        "columns": ["1", "2"],
        "data": ["a", "b"],
    }
    retrieve_data_mock.return_value = test_task_data
    with client.websocket_connect("/api/v1/tasks/test") as ws:
        ws.send_text("hello")
        data = ws.receive_json()
        
        assert data == test_task_data

@patch('app.task.service.TaskService.retrieve_data')
def test_get_task_not_available_and_hang(retrieve_data_mock, client):
    exception_msg = 'file not found'
    retrieve_data_mock.side_effect = AppException(exception_msg)
    try:
        with client.websocket_connect('/api/v1/tasks/test') as ws:
            ws.send_text("hello")
            data = ws.receive_json()
            assert data["message"] == exception_msg
    except:
        pass
    
