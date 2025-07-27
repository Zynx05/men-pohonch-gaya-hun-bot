from fastapi import FastAPI, Request
from math import radians, cos, sin, asin, sqrt
from datetime import datetime
import requests

app = FastAPI()
last_sent = None

# WhatsApp Credentials
WHATSAPP_TOKEN = "EAARtn5xSbEsBPCkVdZA3TMP3thg1YNP6QYUxcfRBYveWRgIjwge7lvVbkFrDLwtj5CoLMu4b0jQqbpS8FsM1ZAiZAhKccgDs0RzWSuPgVXmMlrtXqufc4MNxg0638SJnyPRLfu0sLPZAZCk9Du9dZC52WZAXOHPiv2dRaZAtEZCDrCd8w90uSIcesbkvD937ZBQYLN6LkmK4FZC9GH6ErmL9FYXgWSuAyBsQTQ12JuzHeTrgdnKTAZDZD"
PHONE_NUMBER_ID = "715095305022325"
MOM = "whatsapp:+923403553839"
DAD = "whatsapp:+923709203252"

# Campus Coordinates
UNI_LAT, UNI_LON = 24.9456521247406, 67.11538199559921

def haversine(lat1, lon1, lat2, lon2):
    R = 6371000
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1))*cos(radians(lat2))*sin(dlon/2)**2
    return R * 2 * asin(sqrt(a))

def send_whatsapp(text):
    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    for recipient in [MOM, DAD]:
        payload = {
            "messaging_product": "whatsapp",
            "to": recipient,
            "type": "text",
            "text": {"body": text}
        }
        requests.post(url, headers=headers, json=payload)

@app.post("/location")
async def receive_location(request: Request):
    global last_sent
    data = await request.json()
    lat = data.get("lat")
    lon = data.get("lon")

    if not lat or not lon:
        return {"status": "No coordinates received"}

    dist = haversine(float(lat), float(lon), UNI_LAT, UNI_LON)
    print(f"Distance to university: {dist}m")

    today = datetime.now().date()
    if dist < 200 and last_sent != today:
        send_whatsapp("I’ve reached university 🎓")
        last_sent = today
        return {"status": "Message sent"}

    return {"status": f"Distance is {int(dist)} meters, not close enough"}
