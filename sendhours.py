#!/usr/bin/env python3

from datetime import datetime
import smtplib
import subprocess
import json
import regex as re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from erpwarrior import getLastMonthDate, timeToDec, getTimeSummary

def getPass(pw):
    proc = subprocess.run(["pass", "show", pw], capture_output=True)
    return proc.stdout.decode("utf-8")

def sendHours(config, to, unit, name, hours, numhours):
    message = MIMEMultipart("alternative")
    message["Subject"] = f"{unit} TA Hours for {getLastMonthDate()}"
    message["From"] = f"\"{config['sender_name']}\" <{config['sender_email']}>"
    if config["reply_to"] != "":
        message["Reply-To"] = config["reply_to"]
    message["To"] = to

    text = "HTML email with summary of hours"
    html = f"""<html> <body><p>Hi {name},</p><p>The following are my hours for {getLastMonthDate()}</p> {hours} <p>This totals {numhours} hours</p><p>Kind regards,</p><p>Daniel Jones</p><br/><br/><p style="font-size: 0.75em;">This email was generated via a script as part of my <a href="https://github.com/danjones1618/erp-warrior">erp-warrior</a> project</p></body> </html> """

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    message.attach(part1)
    message.attach(part2)

    # send your email with smtplib.SMTP("smtp.mailtrap.io", 2525) as server: server.login(login, password)
    with smtplib.SMTP(config["smtp_server"], config["smtp_port"]) as server:
        server.starttls()
        server.login(config["smtp_login"], getPass(config["smtp_password_pass_identity"]))
        server.sendmail(config["sender_email"], to, message.as_string())
    print('Sent')

def getHTMLTables(times):
    res = """
        <table style="border: 1px solid #1d1b1e; border-collapse: collapse;">
            <thead>
                <tr>
                    <th style="padding: 0px 16px; border-bottom: 1px solid #1d1b1e;">ID</th>
                    <th style="padding: 0px 16px; border-bottom: 1px solid #1d1b1e;">Date</th>
                    <th style="padding: 0px 16px; border-bottom: 1px solid #1d1b1e;">Start</th>
                    <th style="padding: 0px 16px; border-bottom: 1px solid #1d1b1e;">End</th>
                    <th style="padding: 0px 16px; border-bottom: 1px solid #1d1b1e;">Tags</th>
                </tr>
            </thead>
        <tbody>
    """

    for (i, t) in enumerate(times):
        date = t["start"][0:4] + "-" + t["start"][4:6] + "-" + t["start"][6:8]
        start = t["start"][9:11] + ":" + t["start"][11:13] + ":" + t["start"][13:15]
        end = t["end"][9:11] + ":" + t["end"][11:13] + ":" + t["end"][13:15]
        tags = str(list(filter(lambda x: re.match(r'^Uni\..*$', x) == None, t["tags"])))
        res += f"""
            <tr>
                <td style="padding: 0px 16px;">{str(i)}</td>
                <td style="padding: 0px 16px;">{date}</td>
                <td style="padding: 0px 16px;">{start}</td>
                <td style="padding: 0px 16px;">{end}</td>
                <td style="padding: 0px 16px;">{tags}</td>
            </tr>
        """

    res += "</tbody></table>"
    return res


if __name__ == "__main__":
    with open("/home/dan/.config/erp-warrior/config.json", "r") as cfg:
        config = json.load(cfg)

    for subject in config["categories"]:
        daterange = ":lastmonth"
        ts = getTimeSummary(daterange, subject["tag"])
        totalTime = timeToDec(ts.split("\n")[-3].strip())

        if ts == None:
            print(f"No hours for subject['tag']")
            continue

        proc = subprocess.run(["timew", "export", daterange, ":ids", subject['tag']], capture_output=True)
        times = json.loads(proc.stdout.decode("utf-8"))
        if subject["email"] != "":
            sendHours(config, subject["email"], subject["code"], subject["name"], getHTMLTables(times), totalTime)
