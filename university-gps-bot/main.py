from fastapi import FastAPI, Request
from geopy.distance import geodesic
import requests
import os

app = FastAPI()

# UBIT k cords
UNI_LAT, UNI_LON = 24.94557432346588, 67.115382

# WhatsApp Cloud API credentials
WHATSAPP_API_URL = "https://graph.facebook.com/v22.0/715095305022325/messages"
MOM_PHONE = "whatsapp:+923403553839"
DAD_PHONE = "whatsapp:+923332329158"

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
        # Use template message
        template_message = {
            "messaging_product": "whatsapp",
            "to": MOM_PHONE,
            "type": "template",
            "template": {
                "name": "hello_world", 
                "language": {
                    "code": "en_US"  # or 'ur' if your template is in Urdu
                }
            }
        }

        response1 = requests.post(WHATSAPP_API_URL, json=template_message, headers=HEADERS)
        print("Mom response:", response1.status_code, response1.text)

        template_message["to"] = DAD_PHONE
        response2 = requests.post(WHATSAPP_API_URL, json=template_message, headers=HEADERS)
        print("Dad response:", response2.status_code, response2.text)

        return {
            "status": "Template message sent to both",
            "mom_response": response1.json(),
            "dad_response": response2.json()
        }

    return {"status": f"Distance is {distance:.2f} meters"}
