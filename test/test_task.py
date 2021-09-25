import pytest
from tasklib import TaskWarrior, Task

def test_task_done(client, tmpdir, token):
    tw = TaskWarrior(data_location = tmpdir)
    Task(tw, description="Test task").save()
    rv = client.get('/', headers = {'x-access-tokens': token})
    json_data = rv.get_json()
    assert len(json_data['tasks']) == 1

