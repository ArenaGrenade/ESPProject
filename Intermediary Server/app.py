from flask import Flask, request
import requests
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import hashlib
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
host = "https://esw-onem2m.iiit.ac.in/~/in-cse/in-name/Team-29/"
headers = {
    "X-M2M-Origin": os.getenv("OM2M_KEY"),
    "accept": "application/xml"
}
key = os.getenv("AES_KEY")
cipher = AES.new(key.encode("utf8"), AES.MODE_ECB)

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

@app.route("/<Node>/<Sensor>")
def decryptData(Node, Sensor):
    res = requests.get(f"{host}{Node}/{Sensor}?rcn=4", headers=headers)
    xml_tree = ET.fromstring(res.content)
    match_elements = xml_tree.findall("cin", namespaces={'': xml_tree.tag[1:xml_tree.tag.index('}')]})
    return json.dumps([
        {"time": str(datetime.strptime(elem.findtext("lt"), "%Y%m%dT%H%M%S")), "value": decrypt_and_hash(elem.findtext("con"))}
        for elem in match_elements
    ]), 200, {'ContentType':'application/json'}

@app.route("/")
def root():
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route("/search", methods = ['GET', 'POST'])
def search():
    target = request.json["target"]
    valid_nodes = ["Temperature", "Humidity", "Light", "Moisture", "VOC1", "VOC2"]
    return json.dumps([x for x in valid_nodes if x[:min(len(target), len(x))] == target])

@app.route("/query", methods = ['GET', 'POST'])
def query():
    responses = []
    for target_data in request.json["targets"]:
        target = target_data["target"]
        node = target_data["refId"]
        query_type = target_data["type"]
        
        res = requests.get(f"{host}{node}/{target}?rcn=4", headers=headers)
        xml_tree = ET.fromstring(res.content)
        match_elements = xml_tree.findall("cin", namespaces={'': xml_tree.tag[1:xml_tree.tag.index('}')]})
        
        a = datetime.strptime(match_elements[-1].findtext("lt"), "%Y%m%dT%H%M%S")
        print(a)
        print(a)
        
        responses.append({
            "target": target,
            "datapoints": [
                (decrypt_and_hash(elem.findtext("con")), int((datetime.strptime(elem.findtext("lt"), "%Y%m%dT%H%M%S") - timedelta(hours=5, minutes=30)).timestamp() * 1000))
                for elem in match_elements
            ]
        })
        
    return json.dumps(responses), 200, {'ContentType':'application/json'}


@app.route("/annotations", methods = ['GET', 'POST'])
def annotations():
    print(request.json)
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}


if __name__ == "__main__":
    app.run(debug=True)
