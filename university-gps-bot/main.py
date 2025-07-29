from fastapi import FastAPI, Request
from geopy.distance import geodesic
import requests
import os
from datetime import datetime, timedelta

app = FastAPI()

# WhatsApp Cloud API headers
HEADERS = {
    "Authorization": f"Bearer EAARtn5xSbEsBPDaNIAz2nhQyUwJ4cjMTtINcdy1o7IkLcLvuHFsMfk6ZBFpZAJAz5RL5Vz3lnWERTrdA4ZA2tZA85JLCwWAXsktLrSBm3KgacIHemDObEIj3gZBathVCVbvZAhbQ4TJseZAAs69Vnd9eZC2NGylC2tfpNMS4X9ATLF6jTCUfqSHmOUPrNZCvWkB5SSgZDZD",
    "Content-Type": "application/json"
}

# UBIT Coordinates
UNI_LAT, UNI_LON = 24.94557432346588, 67.115382

# WhatsApp Cloud API credentials
WHATSAPP_API_URL = "https://graph.facebook.com/v22.0/715095305022325/messages"
MOM_PHONE = "whatsapp:+923403553839"
DAD_PHONE = "whatsapp:+923709203252"

# Track last message sent time
last_sent_time = None
SEND_INTERVAL_HOURS = 5  # Don't send again within 5 hours

@app.post("/location")
async def receive_location(request: Request):
    global last_sent_time

    data = await request.json()
    lat = data.get("lat")
    lon = data.get("lon")

    if not lat or not lon:
        return {"error": "Missing lat/lon"}

    user_coords = (lat, lon)
    campus_coords = (UNI_LAT, UNI_LON)
    distance = geodesic(user_coords, campus_coords).meters
    print(f"Distance to university: {distance}m")

    # Check if already sent in the last 5 hours
    now = datetime.now()
    if last_sent_time and now - last_sent_time < timedelta(hours=SEND_INTERVAL_HOURS):
        print("Message already sent in last 5 hours. Skipping.")
        return {"status": "Message recently sent. Skipped."}

    if distance < 300:
        # Send template message
        template_message = {
            "messaging_product": "whatsapp",
            "to": MOM_PHONE,
            "type": "template",
            "template": {
                "name": "arrival_notification",
                "language": {"code": "ur"}
            }
        }

        response1 = requests.post(WHATSAPP_API_URL, json=template_message, headers=HEADERS)
        print("Mom response:", response1.status_code, response1.text)

        template_message["to"] = DAD_PHONE
        response2 = requests.post(WHATSAPP_API_URL, json=template_message, headers=HEADERS)
        print("Dad response:", response2.status_code, response2.text)

        # Update last sent time
        last_sent_time = now

        return {
            "status": "Template message sent to both",
            "mom_response": response1.json(),
            "dad_response": response2.json()
        }

    return {"status": f"Distance is {distance:.2f} meters"}
