# noto

A simple Flask TODO list application with user authentication (registration/login), route protection, and session management.

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running

Start the application:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

## Usage

1. Navigate to `/register` to create a new account.
2. Login at `/login`.
3. Manage your TODO list at `/`.
4. Logout using the "Logout" button.