# Basic Toy WebSocket Server
![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python&logoColor=white)
![Status](https://img.shields.io/badge/Status-Stable-success)

## Basic Setup
## Important to note, make sure your current directory in the terminal is INSIDE the project directory
Create a venv:

```bash
python -m venv venv_name
```

Activate the virtual environment.

**Windows:**
```bash
.\venv_name\Scripts\activate
```

**macOS:**
```bash
source venv_name/bin/activate
```

Install requirements:

```bash
pip install -r requirements.txt
```

---

## How to Run the Program
## Important to note, make sure your current directory in the terminal is INSIDE the project/src directory, otherwise the python scripts will not be found

In the project directory, run:

```bash
python3 server.py
```

To create a client, open a separate terminal and run:

```bash
python3 client.py
```

You can create multiple clients, but each must run in its own terminal session.