# Sherlock AI Testing Project

A lightweight test project for validating and experimenting with **Sherlock AI** logging, observability, performance monitoring, and background insight generation in a FastAPI application.

This project simulates:

* API request tracing
* Performance monitoring
* Error capturing
* Background insight execution
* Mock service/database instrumentation

The application uses FastAPI together with `sherlock_ai` to test automatic logging and observability workflows. 

---

# Project Structure

```bash
sherlockai-testing/
│
├── src/
│   ├── __pycache__/
│   └── mock_db.py              # Simulated database/service operations
│
├── logs/                       # Generated logs
│
├── .env                        # Environment variables
├── .gitignore
├── .python-version
├── main.py                     # Main FastAPI application
├── pyproject.toml              # Project dependencies/config
├── README.md
├── TESTING_CHECKLIST.md        # Manual testing checklist
├── test_background.py          # Background execution tester
└── uv.lock
```

---

# Features

## Request Tracking

Each incoming request gets:

* Unique request ID
* Response timing
* Automatic request logging

Implemented using FastAPI middleware. 

---

## Error Monitoring

The `/error` endpoint intentionally triggers an exception to test Sherlock AI error capturing.

```python
print(1/0)
```



---

## Performance Monitoring

The `/performance` endpoint simulates a slow request using:

```python
time.sleep(5)
```

This helps test:

* Slow request detection
* Performance insights
* Auto instrumentation



---

## Mock Service Instrumentation

The mock database layer simulates:

* Database connection delays
* Query execution
* Error logging

Located in:

```bash
src/mock_db.py
```



---

## Background Insight Execution

`test_background.py` validates whether Sherlock AI insights execute asynchronously without blocking API responses.

It measures API response duration and checks if background jobs continue after the response is returned. 

---

# Installation

## 1. Clone the repository

```bash
git clone <your-repo-url>
cd sherlockai-testing
```

---

## 2. Create virtual environment

Using `uv`:

```bash
uv venv
source .venv/bin/activate
```

Or using Python:

```bash
python -m venv .venv
source .venv/bin/activate
```

---

## 3. Install dependencies

```bash
uv sync
```

Or:

```bash
pip install -e .
```

---

# Running the Application

Start the FastAPI server:

```bash
python main.py
```

The application will run on:

```bash
http://127.0.0.1:8000
```

---

# API Endpoints

## `/error`

Triggers a test exception.

```bash
GET /error
```

Used for:

* Error monitoring
* Stack trace testing
* Exception instrumentation

---

## `/performance`

Simulates a slow API response.

```bash
GET /performance
```

Used for:

* Latency testing
* Performance insights
* Slow request monitoring

---

## `/connect_mongo`

Simulates:

* MongoDB connection
* Service logs
* Error generation

```bash
GET /connect_mongo
```

---

# Running Background Tests

Run:

```bash
python test_background.py
```

This script:

* Sends a request to `/connect_mongo`
* Measures response time
* Verifies non-blocking insight execution



---

# Logging

Sherlock AI automatically captures:

* API logs
* Service logs
* Performance metrics
* Errors
* Request durations

Example logger usage:

```python
logger = get_logger(LoggerNames.API)
```



---

# Example Test Flow

## Test Error Capture

```bash
curl http://127.0.0.1:8000/error
```

---

## Test Performance Monitoring

```bash
curl http://127.0.0.1:8000/performance
```

---

## Test Mock Database Monitoring

```bash
curl http://127.0.0.1:8000/connect_mongo
```

---

# Future Improvements

Possible additions:

* Structured JSON logging
* OpenTelemetry integration
* Async database simulation
* Distributed tracing
* Log persistence backends
* Real database connectors
* Dashboard integration
* CI/CD observability tests

---

# Tech Stack

* Python
* FastAPI
* Sherlock AI
* Uvicorn
* HTTPX

---

# Purpose of This Repository

This repository exists primarily for:

* Sherlock AI experimentation
* Observability testing
* Logging validation
* Performance instrumentation testing
* Background task validation
* FastAPI integration testing

It is intentionally lightweight and focused on testing core Sherlock AI capabilities rather than building a production application.
