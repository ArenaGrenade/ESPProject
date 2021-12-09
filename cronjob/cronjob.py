#!/usr/bin/env python3
import smtplib
import requests
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import hashlib
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
from dotenv import load_dotenv

def decrypt_and_hash(value_string):
    try:
        encrypted, hashed = value_string.split()
        decrypted = unpad(cipher.decrypt(bytes.fromhex(encrypted)), 16)
        current_hash = hashlib.sha256(decrypted).hexdigest()
        if current_hash != hashed:
            print("Something's Wrong")
        else:
            return float(decrypted)
    except:
        return None    
    
def send_email(msg):
    sender = "ews@smart_farming_management.com"
    receiver = "bruh@gmail.com"
    message = f"""\
Subject: Regarding Plant Health
To: {receiver}
From: {sender}

Hey! Just a regular update about your smart farming systems. Looks like there are a couple of issues.

{msg}"""

    with smtplib.SMTP("smtp.mailtrap.io", 2525) as server:
        server.login("c111f6f266825e", "f1147d24788f79")
        server.sendmail(sender, receiver, message)
        
def send_tg_msg(msg):
    TOKEN = os.getenv("TG_KEY")
    chat_id = os.getenv("TG_CHAT_ID")
    
    msg_formatted = f"Hey! Just a regular update about your smart farming systems. Looks like there are a couple of issues.\n\n\n{msg}"
    
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={msg_formatted}"
    _ = requests.get(url)


if __name__ == "__main__":
    load_dotenv()
    Nodes = ["Node-1", "Node-2"]
    Sensors = [("Temperature", "C degrees"), ("Humidity", "%"), ("Moisture", "")]
    Threshold = {
        "Temperature": (15, 30),
        "Humidity": (65, 90),
        "Moisture": (0.65, 0.80)
    }
    host = "https://esw-onem2m.iiit.ac.in/~/in-cse/in-name/Team-29/"
    headers = {
        "X-M2M-Origin": os.getenv("OM2M_KEY"),
        "accept": "application/xml"
    }
    key = os.getenv("AES_KEY")
    cipher = AES.new(key.encode("utf8"), AES.MODE_ECB)

    email_alerts = []
    for Node in Nodes:
        for Sensor, unit in Sensors:
            res = requests.get(f"{host}{Node}/{Sensor}?rcn=4", headers=headers)
            xml_tree = ET.fromstring(res.content)
            match_elements = xml_tree.findall("cin", namespaces={'': xml_tree.tag[1:xml_tree.tag.index('}')]})
            time, value = max([
                (datetime.strptime(elem.findtext("lt"), "%Y%m%dT%H%M%S"), decrypt_and_hash(elem.findtext("con")))
                for elem in match_elements
            ], key=lambda x: x[0])
            if datetime.now() - time < timedelta(hours=1) and value is not None:
                if value <= Threshold[Sensor][0]:
                    email_alerts.append(f"{time} | Plant {Node[-1]} | {Sensor} | Low | {value:.2f}{unit}.\n\n")
                elif Threshold[Sensor][1] <= value:
                    email_alerts.append(f"{time} | Plant {Node[-1]} | {Sensor} | High | {value:.2f}{unit}.\n\n")
    
    if email_alerts:
        send_email("".join(email_alerts))
        send_tg_msg("".join(email_alerts))