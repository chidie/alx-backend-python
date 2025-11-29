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

## 🧑‍💻 Author  
Chidiebere Emmanuel Onuoha

