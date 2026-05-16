# Save as test_background.py
import asyncio
import httpx
import time
from sherlock_ai import LoggerNames
from logging import getLogger

background_test_logger = getLogger(LoggerNames.PERFORMANCEINSIGHTS)

async def test_background_execution():
    url = "http://127.0.0.1:8000/connect_mongo"
    
    print("Testing if insights run in background...")
    print(f"Calling: {url}")
    
    start = time.time()
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(url)
    
    duration = time.time() - start
    
    print(f"\n✓ Response received in: {duration:.2f}s")
    print(f"✓ Status: {response.status_code}")
    print(f"✓ Response: {response.json()}")
    
    if duration < 8:  # Should be ~6s for sleep, not 6s + LLM time
        print("\n✅ SUCCESS! Background execution is working.")
        print("   API responded quickly without waiting for LLM insights.")
    else:
        print("\n❌ PROBLEM! Response took too long.")
        print("   The LLM insight job might be blocking the response.")
    
    print("\nNow check your logs for 'Running insight job' message")
    print("It should appear AFTER this script completes.")
    background_test_logger.info("it should appear AFTER this script completes.")

if __name__ == "__main__":
    asyncio.run(test_background_execution())