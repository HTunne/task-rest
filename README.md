# task-rest
Restful API for taskwarrior built with flask and tasklib.

## Dependancies
* python3
* pipenv
* [taskwarrior](https://github.com/GothenburgBitFactory/taskwarrior)
### Python dependancies (see Pipfile)
* flask
* flask-restful
* flask-cors
* marshmallow
* tasklib
* pyjwt

## Setup
Run `pipenv install` to install all python dependencies.
Then `pipenv run add_user` and follow the instruction to configure a user.
Test the server in development mode with `pipenv run serve`.
See https://flask.palletsprojects.com/en/2.0.x/deploying/index.html for information on deploying flask apps.

## Testing
`pipenv run tests` runs the test suite.

## Schemas
```
taskAnnotation {
    "description": string,

    # read-only
    "entry": date
}

task {
    "description": string,
    "due": date,
    "priority": string,
    "project": string,
    "recur": string,
    "scheduled": date,
    "start": date,
    "tags": list(strings)
    "until": date,

    # read-only
    "annotations": list[taskAnnotation],
    "depends": list[task],
    "end": date,
    "entry": date,
    "id": int,
    "imask": int,
    "mask": string,
    "modified": date,
    "parent": task,
    "status": string,
    "urgency": float,
    "uuid": string
}
```

## API
### `/auth` endpoint
#### GET
With correct username and password as basic authentication headers.
#### Response
JWT required for all other requests.
```
{
  "token": JWT
}
```
`x-access-tokens` must be set to JWT for all other endpionts.

### `/` endpoint
#### GET
Get list of all tasks.
#### Response
```
{
  "tasks": [
    LIST OF ALL TASKS
  ]
}
```
#### POST
Add a new task.
Body:
```
{
# required
  "description": "DESCRIPTION",

# optional
  "due": date,
  "project": "PROJECT",
  "tags": ["TAG_1", "TAG_2"]
  "hide": date,
  "scheduled": date,
  "start": date
}
```

### `/<string:uuid>` endpoint
#### GET
#### PUT
#### DELETE

## `/<string:task_uuid>/<string:command>` endpoint
#### PUT
