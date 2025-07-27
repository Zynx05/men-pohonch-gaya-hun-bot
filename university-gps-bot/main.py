from fastapi import FastAPI, Request
from geopy.distance import geodesic
import requests
import os

app = FastAPI()

# UBIT k cords
UNI_LAT, UNI_LON = 24.94557432346588, 67.115382

# WhatsApp Cloud API credentials
WHATSAPP_API_URL = "https://graph.facebook.com/v22.0/715095305022325/messages"
ACCESS_TOKEN = "EAARtn5xSbEsBPCkVdZA3TMP3thg1YNP6QYUxcfRBYveWRgIjwge7lvVbkFrDLwtj5CoLMu4b0jQqbpS8FsM1ZAiZAhKccgDs0RzWSuPgVXmMlrtXqufc4MNxg0638SJnyPRLfu0sLPZAZCk9Du9dZC52WZAXOHPiv2dRaZAtEZCDrCd8w90uSIcesbkvD937ZBQYLN6LkmK4FZC9GH6ErmL9FYXgWSuAyBsQTQ12JuzHeTrgdnKTAZDZD"
MOM_PHONE = "whatsapp:+923403553839"
DAD_PHONE = "whatsapp:+923709203252"

@app.post("/location")
async def receive_location(request: Request):
    data = await request.json()
    lat = data.get("lat")
    lon = data.get("lon")

    if not lat or not lon:
        return {"error": "Missing lat/lon"}

    user_coords = (lat, lon)
    campus_coords = (UNI_LAT, UNI_LON)
    distance = geodesic(user_coords, campus_coords).meters
    print(f"Distance to university: {distance}m")

    if distance < 300:
    message = {
        "messaging_product": "whatsapp",
        "to": MOM_PHONE,
        "type": "text",
        "text": {"body": "Mein pohanch gaya hoon"},
    }

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    response1 = requests.post(WHATSAPP_API_URL, json=message, headers=headers)
    print("Mom response:", response1.status_code, response1.text)

    message["to"] = DAD_PHONE
    response2 = requests.post(WHATSAPP_API_URL, json=message, headers=headers)
    print("Dad response:", response2.status_code, response2.text)


    return {"status": f"Distance is {distance:.2f} meters"}
