from logging import getLogger
from sherlock_ai import LoggerNames
import time

mock_mongo_logger = getLogger(LoggerNames.SERVICES)

def mock_mongo():
    mock_mongo_logger.info("Mock MongoDB connecting.")
    # mock_query()
    time.sleep(6)  # Simulate connection delay
    mock_mongo_logger.info("Mock MongoDB connected.")

def mock_query():
    mock_mongo_logger.info("Mock MongoDB querying.")
    time.sleep(7)  # Simulate query delay
    mock_mongo_logger.info("Mock MongoDB query completed.")

def mock_error():
    mock_mongo_logger.info("Mock MongoDB error simulation started.")
    try:
        1 / 0  # This will raise a ZeroDivisionError
    except ZeroDivisionError as e:
        mock_mongo_logger.error("Mock MongoDB encountered an error: %s", str(e))