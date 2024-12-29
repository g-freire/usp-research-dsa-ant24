# uvicorn main:app --reload
import asyncio
from fastapi import FastAPI
import time

app = FastAPI()

# Simulate a long-running task
@app.get("/long-task")
async def long_task():
    print(f"Start long task at {time.strftime('%X')}")
    await asyncio.sleep(10)  # Simulate a 10-second I/O-bound task
    print(f"End long task at {time.strftime('%X')}")
    return {"message": "Long task completed"}

# Quick response endpoint
@app.get("/quick-task")
async def quick_task():
    print(f"Quick task at {time.strftime('%X')}")
    return {"message": "Quick task completed"}