#!/usr/bin/env python3

import datetime
import json
import subprocess
import pyperclip

def timeToDec(t):
    parts = t.split(':')
    time = float(parts[0]) + float(parts[1])/60 + float(parts[2])/3600
    n = time // 1
    r = time % 1
    if r <= 0.25:
        r = 0.25
    elif r <= 0.5:
        r = 0.5
    elif r <= 0.75:
        r = 0.75
    else:
        r = 1
    return n + r

def copyToClipboard(s):
    ans = input(f"Copy '{s}' to clipboard?").lower()
    if ans in ['y', "yes"]:
        pyperclip.copy(s)
        print(f"'{s}' coppied to clipboard")

def getTodaysDate():
    return datetime.date.today().isoformat()

def getLastMonthDate():
    now = datetime.datetime.now()
    lastMonth = now.month - 1 if now.month > 1 else 12
    year = now.year if now.month > 1 else now.year-1
    months = ["", "January", "Febuary", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December" ]
    return f"{months[lastMonth]} {year}"

def getTimeSummary(daterange, tags):
    proc = subprocess.run(["timew", "summary", daterange, ":ids", tags], capture_output=True)
    times = proc.stdout.decode("utf-8")
    if times.startswith("No"):
        print(f"\nNo hours logged for {subject['code']}\n")
        return None
    return times

if __name__ == "__main__":
    with open("/home/dan/.config/erp-warrior/config.json", "r") as cfg:
        config = json.load(cfg)

    for subject in config["categories"]:
        daterange = ":lastmonth"
        times = getTimeSummary(daterange, subject["tag"])

        print(f"Unit code: {subject['code']}")
        print(times)

        totalTime = timeToDec(times.split("\n")[-3].strip())
        print("Decimal hours:", totalTime)

        copyToClipboard(f"{subject['code']} {getLastMonthDate()}")
        copyToClipboard(totalTime)
        copyToClipboard(subject['auth'].format(getTodaysDate()))
