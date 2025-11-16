# ALX Backend Python - Generators 0x00

## Project Overview
This project sets up a MySQL database and provides utilities for data management using Python generators and related tools.

## Prerequisites
- Docker and Docker Compose
- Python 3.x (if running locally without Docker)
- MySQL 9.5.0

## Setup Instructions

### Using Docker (Recommended)

1. **Clone the repository** (if applicable)
   ```bash
   git clone <repository-url>
   cd alx-backend-python

2. **Build and start the Docker containers**
    ```bash
    docker-compose up -d

2. **Verify the services are running**
    ```bash
    docker-compose ps

### Local setup (Without Docker)

1. **Create a Python virtual environment**
    ```bash
    python -m venv project_venv
    source project_venv/bin/activate  or  project_venv\Scripts\activate

2. **Install dependencies**
    ````bash
    pip install -r requirements.txt

3. **Create a .env file in the project root with your MySQL credentials.**

4. **Run the seed script to initialize the database**
    ````bash
    python python-generators-0x00/seed.py