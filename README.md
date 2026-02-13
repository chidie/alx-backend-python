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



# Python Unit Testing Project
### Testing `access_nested_map`, `get_json`, and `memoize` utilities

This project contains a suite of **unit tests** for utility functions defined in the `utils` module.  
Tests are written using:

- `unittest`
- `parameterized`
- `unittest.mock`
- Python's standard testing patterns

The goal is to validate functionality, raise proper exceptions, and ensure memoization works as intended.

---

## Project Structure

```
project/
├── utils.py
├── test_utils.py   # Your test file
└── README.md
```

---

## Features Tested

### 1. `access_nested_map`
A helper function used to retrieve values deep inside nested dictionaries.

#### **Tests include:**
- Returning correct values for valid paths  
- Raising `KeyError` when path is invalid  
- Verifying exception messages  

---

### 2. `get_json`
Fetches JSON from a URL using `requests.get`.

#### **Tests include:**
- Mocking external HTTP calls using `unittest.mock.patch`  
- Ensuring `requests.get` is called exactly once  
- Returning the expected JSON payload  

No real HTTP request is made during the tests.

---

### 3. `memoize`
A decorator used to cache results of a method call inside an instance.

#### **Tests include:**
- Mocking the underlying method  
- Ensuring the memoized property only calls the actual method **once**  
- Ensuring repeated accesses return the cached value  

---

## Installation

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

## Running Tests

From the project root:

```bash
python3 -m unittest test_utils.py
```

Or run all tests automatically:

```bash
python3 -m unittest discover
```

---

## Example Tested Utilities

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
    docker compose exec app python Django-signals_orm-0x04/manage.py makemigrations messaging # To generate migrations for the messaging app
    docker compose exec app python Django-signals_orm-0x04/manage.py makemigrations           # For all apps
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

>NOTE: To use kubernetes deployments, create one as in deployment.yml
- Create a deployment file
- Start minikube or kind
- Run your deployment
```bash
    minikube start
    kubectl get nodes
    kubectl apply -f deployment.yml
    kubectl get nodes
    kubectl get pods
    kubectl config use-context minikube # optional if you had kind already running and need to switch to minikube
    kubectl get nodes
    kind delete cluster # optional to delete cluster created by kind.
    kubectl get deployments
    kubectl get svc

    # Rebuild your image INSIDE Minikube (this is mandatory)
    minikube image build -t messaging-app:latest . # Build the image inside the minikube
    kubectl get pods

    # If target image is not inside minikube, this may result
    image: messaging-app:latest
    imagePullPolicy: Never

    minikube image ls   # Confirm the image exists inside Minikube -> Confirm the image exists inside Minikube
    kubectl delete pod -l app=messaging-app # Delete old pods so they restart with the new image

    # Restart your deployment
    kubectl delete pod -l app=messaging-app

    # If the image is still found in docker registry instead of minikube, then Switch your shell to use Minikube’s Docker daemon
    minikube -p minikube docker-env | Invoke-Expression # This rewires the powershell so that 'docker build' and 'minikube image build' both build inside minikube not docker desktop
    docker images
    
    # Rebuild image inside minikube
    docker build -t messaging-app:latest .

    To convert string to base64:
    [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes("PASTE_YOUR_SECRET_HERE"))

    # Best way to troubleshoot this:
    - restart Docker desktop
    - delete all containers or containers related to minikube
    
    minikube stop
    minikube delete --all --purge
    minikube start --driver=docker
    minikube update-context
    & minikube -p minikube docker-env | Invoke-Expression
    echo $Env:DOCKER_HOST
    docker build -t messaging-app:latest .
    minikube image ls | Select-String "messaging-app"
    kubectl apply -f django-secret.yaml
    kubectl apply -f service.yaml
    kubectl apply -f postgres-secret.yaml
    kubectl apply -f postgres.yaml
    kubectl apply -f deployment.yaml
    kubectl rollout restart deployment messaging-app-deployment
    kubectl get nodes
    kubectl get svc
    kubectl get pods

    # verify the app is present 
    minikube ssh
    docker images | grep messaging-app

    ##### TROUBLESHOOTING TIPS ####
    # If messaging-app is not found in the list of docker images it means
    # that you built your Docker image on your host machine, not inside Minikube’s Docker daemon. Minikube runs its own internal Docker engine.
    # Kubernetes can only see images built inside that engine.
    #- Switch your terminal to use Minikube’s Docker daemon
    eval $(minikube docker-env) 
    # The above command rewires Docker CLI so that 'docker build', 'docker images' and 'docker run' all operate inside Minikube, not on your host.
    # Now build Django image inside Minikube
    docker build -t messaging-app:latest .
    docker images
    kubectl rollout restart deployment messaging-app-deployment
    kubectl get pods
    # Expected ErrImageNeverPull changes to ContainerCreating → Running
    # A reliable option to see your app is via port-forwarding or minikube service command
    kubectl port-forward svc/messaging-app-service 8080:8000

    ##### After updating the deployment or service, apply it and restart the deployment
    kubectl apply -f deployment.yml
    kubectl rollout restart deployment messaging-app-deployment
    kubectl get pods
    kubectl logs postgres-<pod-name>
    kubectl describe pod -l app=postgres
    kubectl logs -l app=messaging-app


    # To access Django app on local browser, use nodePort instead of clusterIP in the service.yaml file.
    http://localhost:30080
    # Option2 is to use minikube service
    minikube service messaging-app-service
    # Option3: Port-forward
    kubectl port-forward svc/messaging-app-service 8080:8000
    http://localhost:8080

```

## To install the NGINX ingress controller on minikube:
```bash
    minikube addons enable ingress
    kubectl get pods -n ingress-nginx
    kubectl get svc -n ingress-nginx
```

# To add a host entry so the browser can resolve the domain name to the minikube IP:

```bash
    # Open Powershell in Administrator mode and 
    notepad C:\Windows\System32\drivers\etc\hosts
    minikube ip
    # Add the following line to your /etc/hosts file (replace <minikube-ip> with the actual IP address):
    <minikube-ip> messaging-app.local
```bash
- 
## Author  
Chidiebere Emmanuel Onuoha

