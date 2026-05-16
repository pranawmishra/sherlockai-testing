# SherlockAI Testing Checklist

Testing app: `main.py` (FastAPI on `http://127.0.0.1:8000`)  
Run server: `python main.py`

---

## 0. Setup

- [ ] `.env` is populated (API keys for LLM provider if testing insights)
- [ ] `sherlock-ai` is installed in the virtual environment (`pip show sherlock-ai`)
- [ ] Server starts without errors: `python main.py`
- [ ] Server is reachable: `curl http://127.0.0.1:8000/docs`

---

## 1. SherlockAI Initialization

Checks that `SherlockAI` sets up correctly with `LoggingConfig`.

- [ ] Server starts with no import or config errors
- [ ] `LoggingConfig(auto_min_duration=4)` is accepted without exception
- [ ] `sherlock.setup()` completes silently
- [ ] `get_logger(LoggerNames.API)` returns a usable logger (no `None` / error on first request)
- [ ] All 6 log files are created under `logs/` on first request:
  - [ ] `logs/api.json`
  - [ ] `logs/app.json`
  - [ ] `logs/services.json`
  - [ ] `logs/performance.json`
  - [ ] `logs/monitoring.json`
  - [ ] `logs/performance_insights.json`

---

## 2. Middleware — Request ID & Headers

Every request must pass through the `middleware_wrapper`.

```bash
curl -i http://127.0.0.1:8000/connect_mongo
```

- [ ] Response contains `X-Request-ID` header (8-char hex string, e.g. `5902f570`)
- [ ] Response contains `X-Response-Time` header (float in seconds, e.g. `6.0143`)
- [ ] Two consecutive requests produce **different** `X-Request-ID` values
- [ ] The `X-Request-ID` in the response header **matches** the `request_id` field in `logs/api.json` for that request
- [ ] `logs/api.json` contains a line: `"message": "Request completed in X.XXXX seconds"`

---

## 3. Route — `/error`

Tests error logging when an unhandled exception occurs.

```bash
curl -i http://127.0.0.1:8000/error
```

- [ ] Response returns HTTP `500`
- [ ] `logs/api.json` contains a log line for this request with the correct `request_id`
- [ ] `logs/app.json` contains the `ZeroDivisionError` traceback or error message
- [ ] `X-Request-ID` is still present in the response headers (middleware ran to completion)

> **Note:** The route has `print(1/0)` — check that the error surfaces in logs, not just the terminal stdout.

---

## 4. Route — `/performance`

Tests the `auto_min_duration=4` filter. This route sleeps for 5 seconds, which exceeds the threshold.

```bash
curl http://127.0.0.1:8000/performance
```

- [ ] Response returns `{"message": "Hello, World!"}` after ~5 seconds
- [ ] `logs/api.json` shows request duration ≥ 5s for this request
- [ ] `logs/performance_insights.json` receives a new LLM-generated insight entry for this request (contains `request_id` from the headers)
- [ ] The insight entry appears **after** the HTTP response is received (background execution, not blocking)

**Contrast test — fast route (below threshold):**

```bash
curl http://127.0.0.1:8000/error  # fast, ~0ms
```

- [ ] `logs/performance_insights.json` does **not** get a new entry for requests faster than 4s
- [ ] `auto_min_duration=4` is correctly filtering out fast requests

---

## 5. Route — `/connect_mongo`

Tests `ServiceLogger` in a synchronous function called from an async route, plus background insight execution.

```bash
curl -i http://127.0.0.1:8000/connect_mongo
```

- [ ] Response returns `{"message": "Connected to Mock MongoDB!"}` after ~6 seconds
- [ ] `logs/services.json` contains two entries with the same `request_id`:
  - [ ] `"Mock MongoDB connecting."`
  - [ ] `"Mock MongoDB connected."`
- [ ] The `request_id` in `logs/services.json` matches the `X-Request-ID` response header (context propagation works)
- [ ] `logs/api.json` shows request duration ≥ 6s
- [ ] `logs/performance_insights.json` receives a new LLM insight entry after the response (background job)

---

## 6. Background Execution — LLM Insight Jobs

Verifies that LLM insight generation does not block HTTP responses.  
Use the provided script (requires server to be running):

```bash
python test_background.py
```

- [ ] Script prints `SUCCESS! Background execution is working.` (response in < 8s)
- [ ] Script does **not** hang waiting for LLM response
- [ ] After the script finishes, a new entry appears in `logs/performance_insights.json`
- [ ] The insight entry's `request_id` matches what was printed during the run
- [ ] `logs/performance_insights.json` entry appears **after** `test_background.py` exits, not before

---

## 7. Request ID Context Propagation

Verifies that the same `request_id` flows through all loggers for a single request.

Run `/connect_mongo` and note the `X-Request-ID` from the response header.

- [ ] `logs/api.json` has an entry with that `request_id`
- [ ] `logs/services.json` has entries with that same `request_id`
- [ ] `logs/performance_insights.json` (if insight was generated) has the same `request_id`
- [ ] A second request produces a **completely different** `request_id` across all log files

---

## 8. Logger Channels — Correct Log File Routing

Confirms each `LoggerNames` constant writes to the right file.

| Logger | Expected file |
|--------|--------------|
| `LoggerNames.API` (`ApiLogger`) | `logs/api.json` |
| `LoggerNames.SERVICES` (`ServiceLogger`) | `logs/services.json` |
| `LoggerNames.PERFORMANCEINSIGHTS` (`PerformanceInsightsLogger`) | `logs/performance_insights.json` |

- [ ] `ApiLogger` messages only appear in `logs/api.json`, not `logs/services.json`
- [ ] `ServiceLogger` messages only appear in `logs/services.json`
- [ ] `PerformanceInsightsLogger` messages only appear in `logs/performance_insights.json`
- [ ] `logs/app.json` catches root-level / unhandled log messages

---

## 9. `mock_db.py` — Unused Functions

These functions exist in `src/mock_db.py` but are not wired to any route yet.

- [ ] `mock_query()` — simulates a 7s DB query with `ServiceLogger`
- [ ] `mock_error()` — simulates a `ZeroDivisionError` caught and logged as `ERROR`

**To test manually**, temporarily call them from `/connect_mongo` or a new route and verify:

- [ ] `mock_query()`: `logs/services.json` gets `"Mock MongoDB querying."` and `"Mock MongoDB query completed."` entries
- [ ] `mock_error()`: `logs/services.json` gets an `ERROR`-level entry with the exception message

---

## 10. Edge Cases

- [ ] Sending two concurrent requests to `/connect_mongo` — each gets a unique `request_id` in logs
- [ ] Restarting the server — new requests append to existing log files (logs are not wiped)
- [ ] Server handles a request to an undefined route (`/nonexistent`) — returns 404; `logs/api.json` logs it with a `request_id`

---

## Quick Reference — How to Check Logs

```bash
# Watch api.json live
tail -f logs/api.json

# Pretty-print last entry in any log
tail -1 logs/performance_insights.json | python -m json.tool

# Count entries per log file
wc -l logs/*.json
```
