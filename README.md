## Requirements
- All your files will be interpreted/compiled on Ubuntu 18.04 LTS using python3 (version 3.7)
- All your files should end with a new line
- The first line of all your files should be exactly #!/usr/bin/env python3
- A README.md file, at the root of the folder of the project, is mandatory
Your code should use the pycodestyle style (version 2.5)
- All your files must be executable
- All your modules should have a documentation (python3 -c 'print(__import__("my_module").__doc__)')
- All your classes should have a documentation (python3 -c 'print(__import__("my_module").MyClass.__doc__)')
- All your functions (inside and outside a class) should have a documentation (python3 -c 'print(__import__("my_module").my_function.__doc__)' and python3 -c 'print(__import__("my_module").MyClass.my_function.__doc__)')
- A documentation is not a simple word, it’s a real sentence explaining what’s the purpose of the module, class or method (the length of it will be verified)
- All your functions and coroutines must be type-annotated.



# 🧪 Python Unit Testing Project
### Testing `access_nested_map`, `get_json`, and `memoize` utilities

This project contains a suite of **unit tests** for utility functions defined in the `utils` module.  
Tests are written using:

- `unittest`
- `parameterized`
- `unittest.mock`
- Python's standard testing patterns

The goal is to validate functionality, raise proper exceptions, and ensure memoization works as intended.

---

## 📁 Project Structure

```
project/
├── utils.py
├── test_utils.py   # Your test file
└── README.md
```

---

## 🧰 Features Tested

### ✅ 1. `access_nested_map`
A helper function used to retrieve values deep inside nested dictionaries.

#### **Tests include:**
- Returning correct values for valid paths  
- Raising `KeyError` when path is invalid  
- Verifying exception messages  

---

### ✅ 2. `get_json`
Fetches JSON from a URL using `requests.get`.

#### **Tests include:**
- Mocking external HTTP calls using `unittest.mock.patch`  
- Ensuring `requests.get` is called exactly once  
- Returning the expected JSON payload  

No real HTTP request is made during the tests.

---

### ✅ 3. `memoize`
A decorator used to cache results of a method call inside an instance.

#### **Tests include:**
- Mocking the underlying method  
- Ensuring the memoized property only calls the actual method **once**  
- Ensuring repeated accesses return the cached value  

---

## 📦 Installation

Install dependencies:

```bash
pip install parameterized
```

(Optional) If using a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## ▶️ Running Tests

From the project root:

```bash
python3 -m unittest test_utils.py
```

Or run all tests automatically:

```bash
python3 -m unittest discover
```

---

## 📝 Example Tested Utilities

### `access_nested_map`
```python
result = access_nested_map({"a": {"b": 2}}, ("a", "b"))
# result → 2
```

### `get_json`
```python
data = get_json("http://example.com")
```

### `memoize`
```python
class MyClass:
    @memoize
    def value(self):
        return expensive_operation()
```

---

test_client is for mocking a property.

### Django setup.py should contain:
``` bash
    # REST Framework configuration
    REST_FRAMEWORK = {
        "DEFAULT_PERMISSION_CLASSES": [
            "rest_framework.permissions.AllowAny",
        ],
        "DEFAULT_AUTHENTICATION_CLASSES": [
            "rest_framework.authentication.SessionAuthentication",
            "rest_framework.authentication.BasicAuthentication",
        ],
    }
```

### To check query your sqlite3 database, keep this in mind.
```bash
    sqlite3 database_name
    .tables
    .schema # (optional)
    SELECT * FROM table_name LIMIT 10
    .exit # To exit
```

### Core Django Project Files
> manage.py - Serves as a command-line utility for interacting with the project. With it, commands like 'runserver', 'migrate', 'createsuperuser' can be run. It also acts as the entry point for Django's administrative tasks. Overall, it wraps django admin with project's settings to avoid manually specifying them.

> settings.py - This is the central configuration file for your project. Defines database connections, installed apps, middleware, templates, static files, authentication, etc. Ensures consistency across the project by centralizing configuration. Without it, Django wouldn't know how to connect to your database or which apps to load.

> urls.py - URL dispatcher (routing system). It maps incoming HTTP requests to the correct views. It keeps routing logic seperate from business logic. Without it, Django wouldn't know which view to call when a user visit a URL.

> wsgi.py - Entry point for WSGI-compatible web servers (eng., Gunicorn, uWSGI). It defines how the project communicates with production web servers. It is required for deployment in most environments. Without it, the app couldn't run on a standard web server.

> asgi.py - Entry point for ASGI-compatible servers (e.g., Daphne, Uvicorn). It must be present because it enables asynchronous features like WebSockets and long-lived connections. It is required for modern Django apps that use async views or real-time communication. It complements wsgi.py for async deployments.

### Key Files Inside Each App
>models.py - Defines database schema via Django ORM. It must be present because it maps Python classes to database tables. Without it, you couldn't persist or query data.

>views.py - Contains request-handling logic. It defines how the data is processed and returned (HTML, JSON, etc,). Without it, URLs would have no logic to execute.

>admin.py - Registers models with Django Admin. Allows for the management of data via the built-in admin interface. Without it, your models wouldn't appear in the admin dashboard.

>apps.py - App configuration file. It defines metadata about the app (name, signals, etc.) and it ensures Django can discover and initialize the app correctly.

>tests.py - Contains unit tests for the app. It ensures your code works as expected. While not strictly required, it's best practice for maintainability.

>NOTE:
```bash
    python manage.py makemigrations # only when there has been changes in the model (added/removed fields, new models, alteres)
    python manage.py migrate        # run after makemigrations to apply those changes to the database.
    python manage.py runserver      # run to start the development server and test the routes
    python manage.py check          # runs Django system checks to ensure the  project configuration is valid
```
How to set users info from the shell:
(project_venv) PS C:\Users\chidi\OneDrive\Documents\ALX\SE\alx-backend-python\messaging_app> python manage.py shell

```bash
    >>> from chats.models import User
    >>> u = User.objects.get(id="cc3efacd-7b31-4f2b-88cf-b4d7ab6118a2")
    >>> print(u.first_name)

    >>> u.first_name = "Alice"
    >>> u.last_name = "Onuoha"
    >>> u.role = "guest"
    >>> u.save()
```

>NOTE: If you delete your migrations folder, you can create a new one
```bash
    docker compose exec app python Django-signals_orm-0x04/manage.py showmigrations messaging
    docker compose exec app python Django-signals_orm-0x04/manage.py migrate

    # To test for signals:
    from messaging.models import User, Conversation, Message, Notification
    >>>
    >>> sender = User.objects.create_user(email="sender@test.com", password="pass123")
    er@test.com", password="pass123")
    >>> receiver = User.objects.create_user(email="receiver@test.com", password="pass123")
    >>> conv = Conversation.objects.create()
    ants.set([sender, receiver])
    >>> conv.participants.set([sender, receiver])
    >>> msg = Message.objects.create(
    ...     sender=sender,
    ...     receiver=receiver,
    ...     conversation=conv,
    ...     message_body="Hello!"
    ... )
    >>> Notification.objects.filter(user=receiver, message=msg).exists()
    True
    >>> msg.message_body = "Edited message"
    >>> msg.save()
    >>> Notification.objects.filter(message=msg).count()
    1
    >>>
```
## 🧑‍💻 Author  
Chidiebere Emmanuel Onuoha

