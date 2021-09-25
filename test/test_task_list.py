import pytest
from tasklib import TaskWarrior, Task

def test_get_empty_task_list(client, token):
    rv = client.get('/', headers = {'x-access-tokens': token})
    json_data = rv.get_json()
    assert len(json_data['tasks']) == 0

def test_get_non_empty_task_list(client, tmpdir, token):
    tw = TaskWarrior(data_location = tmpdir)
    Task(tw, description="Test task").save()
    rv = client.get('/', headers = {'x-access-tokens': token})
    json_data = rv.get_json()
    assert len(json_data['tasks']) == 1

def test_post_empty_task_list(client, tmpdir, token):
    pass

def test_post_single_task_list(client, tmpdir, token):
    pass

def test_post_multiple_task_list(client, tmpdir, token):
    pass

def test_post_malformed_task_list(client, tmpdir, token):
    pass
