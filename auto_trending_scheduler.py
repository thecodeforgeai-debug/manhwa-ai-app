#!/usr/bin/env python3
import schedule
import time
import subprocess
from datetime import datetime

def run_trending_tracker():
    print(f"\n🕐 Running trending tracker: {datetime.now()}")
    subprocess.run(['python3', 'social_trending_tracker.py'])

def run_auto_discovery():
    print(f"\n🕐 Running auto-discovery: {datetime.now()}")
    subprocess.run(['python3', 'auto_add_trending.py'])

schedule.every().day.at("02:00").do(run_trending_tracker)
schedule.every().day.at("02:30").do(run_auto_discovery)

print("🤖 Scheduler started")
run_trending_tracker()
run_auto_discovery()
print("\n⏳ Running...")

while True:
    schedule.run_pending()
    time.sleep(60)
