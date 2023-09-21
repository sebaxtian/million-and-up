# Owner Service
This microservice is created following the requirements from the data model defined by Million and Up.

## How to use

Please read and execute each step below:

### Step 1

Create and use Python Virtual Environment:

```bash
$promt> python -m venv .venv
$promt> source .venv/bin/activate
```

### Step 2

Install all Python Requirements:

```bash
$promt> python -m pip install -U pip
$promt> pip install -r requirements.txt
```

### Optional

Generate a requirements file and then install from it in another environment:

```bash
$promt> pip freeze > requirements.txt
```

## Settings Management

Before running you should create the environment variables file and the secrets files.

### Environment Variables

Create a new **.env** file inside the owner directory and use the environment variables as you can see in the [example.env](example.env) file just change the values. This file will be ignored and never will be committed to the repository.

### Secret Files

Create secret files inside the **secrets** directory, those files will be ignored and never will be committed to the repository.

The secret files below are required:

- mongodb_url
    - [Default: mongodb://admin:admin@localhost:27017/auth?authSource=admin]
- jwt_secret_key
    - [Default: to get a string run: openssl rand -hex 32]
- jwt_algorithm
    - [Default: HS256]

## Testing

```bash
$promt> pytest -v -s -W ignore::DeprecationWarning --cov=apps/backend/owner/src
```

## How to run

> **Development Mode**

```bash
$promt> python run.py
```
