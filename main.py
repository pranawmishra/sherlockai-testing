from sherlock_ai import SherlockAI, LoggingConfig, get_logger, LoggerNames, set_request_id
from fastapi import FastAPI, Request
# from dotenv import load_dotenv
import os
import uvicorn
import time
from src.mock_db import *


# load_dotenv()

app = FastAPI()

logging_config = LoggingConfig(
    # log_level="INFO",
    # log_format_type="json",
    auto_min_duration=4
)

sherlock = SherlockAI(
    config=logging_config
)
sherlock.setup()

logger = get_logger(LoggerNames.API)

@app.middleware("http")
async def middleware_wrapper(request: Request, call_next):
    request_id = set_request_id()
    start = time.perf_counter()
    request.state.request_id = request_id
    response = await call_next(request)
    duration = time.perf_counter() - start
    logger.info(f"Request completed in {duration:.4f} seconds")
    response.headers['X-Request-ID'] = request_id
    response.headers['X-Response-Time'] = f"{duration:.4f}"

    return response

@app.get("/error")
async def read_root():
    try:
        logger.info("Hello, World!")
        print(1/0) # This will raise a ZeroDivisionError
        return {"message": "Hello, World!"}
    except Exception as e:
        print(e)
        # logger.error(f"Error: {e}")
        # raise e


@app.get("/performance")
async def read_root():
    logger.info("Hello, World!")
    time.sleep(5)
    return {"message": "Hello, World!"}

@app.get("/connect_mongo")
async def connect_mongo():
    mock_mongo()
    mock_error()
    return {"message": "Connected to Mock MongoDB!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)