import os
import pytest
import pandas as pd

from fastapi import UploadFile
from unittest.mock import patch
from starlette.background import BackgroundTasks

from app.utils.app_exceptions import AppException

from .service import TaskService
from app.settings import basedir

"""
upload file and process data successfully
"""
def test_handle_data_upload():
    _file_name = 'test_us-census-income.csv'
    _mock_file = mock_file(_file_name)

    mock_background_tasks = BackgroundTasks()
    with patch.object(BackgroundTasks, 'add_task', wraps=mock_background_tasks.add_task) as mock:
        message = TaskService().handle_data_upload(_mock_file, mock_background_tasks)
        mock.assert_called_once
    
    assert message == f"File {_file_name} upload successfully"

"""
expect to raise exception if data is not valid.
such as: 
1. not column separated 
2. expected columns not exist
"""
def test_handle_data_upload_invalid_file():
    _file_name = 'test_invalid-file.txt'
    _mock_file = mock_file(_file_name)

    mock_background_tasks = BackgroundTasks()
    with patch.object(BackgroundTasks, 'add_task', wraps=mock_background_tasks.add_task) as mock:
        with pytest.raises(AppException) as ex:
            message = TaskService().handle_data_upload(_mock_file, mock_background_tasks)
            mock.assert_not_called
            assert message == {}


@patch('pandas.read_csv')
def test_retrieve_data_success(pd_read_mock):
    expected_df = pd.DataFrame({
        "education": ["Bachelors","HS-grad","Masters","11th","9th"],
        "percentage": [0.4, 0.2, 0.2, 0.1, 0.1],
    })
    pd_read_mock.return_value = expected_df
    task = TaskService().retrieve_data('1')

    assert expected_df.to_dict('split') == task

@patch('pandas.read_csv')
def test_retrieve_data_not_found(pd_read_mock):
    pd_read_mock.side_effect = FileNotFoundError('not found')
    with pytest.raises(AppException) as ex:
        task = TaskService().retrieve_data('3')
        assert task == {}

def mock_file(filename: str) -> UploadFile:
    _test_upload_file = os.path.join(basedir, f'task/mock_data/{filename}')
    input_file = open(_test_upload_file, 'rb')
    return UploadFile(filename=filename, file=input_file)

