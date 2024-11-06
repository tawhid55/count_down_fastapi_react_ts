# main.py
from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import asyncio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # List the origins you want to allow
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Countdown settings
countdown_duration = 1 * 60  # 4 minutes in seconds
repeat_count = 5
countdown_start_time = "00:42"  # Set the desired start time (24-hour format)
countdown_data = {"time_left": countdown_duration, "repeats": repeat_count, "active": False}

# Scheduler to check time
scheduler = BackgroundScheduler()
scheduler.start()

async def run_countdown():
    countdown_data["active"] = True
    for _ in range(countdown_data["repeats"]):
        countdown_data["time_left"] = countdown_duration
        while countdown_data["time_left"] > 0:
            await asyncio.sleep(1)
            countdown_data["time_left"] -= 1
        await asyncio.sleep(1)  # Delay between repetitions
    countdown_data["active"] = False

def check_and_start_countdown():
    now = datetime.now()
    
    if now.strftime("%H:%M") == countdown_start_time and now.weekday() < 5:
        print("started______________________")
        print(countdown_data["active"])
        if not countdown_data["active"]:
            print("Condition______________________")
            asyncio.run(run_countdown())

scheduler.add_job(check_and_start_countdown, "interval", seconds=6, max_instances=2)

@app.get("/countdown")
async def get_countdown_status():
    return JSONResponse(content=countdown_data)

