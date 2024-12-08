from datetime import datetime
import requests
import os
import yagmail
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants
GENDER = "male"
WEIGHT = 80.5
HEIGHT = 185
AGE = 23
APP_ID = os.getenv("APP_ID")
APP_KEYS = os.getenv("APP_KEYS")
email_address = "pythonyemi@gmail.com"  # Sender's email address
app_password = "docs zjgh aszw ipjt"  # App password for email
recipient_email = "receiver@gmail.com"  # Recipient's email address

# Nutritionix API endpoint and headers
natural_exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
headers = {
    "x-app-id": APP_ID,
    "x-app-key": APP_KEYS,
    "x-remote-user-id": "0",
}

# Input and request payload
params = {
    "query": input("Tell me which exercise you did: "),
    "gender": GENDER,
    "weight_kg": WEIGHT,
    "height_cm": HEIGHT,
    "age": AGE
}

# Send request to Nutritionix
response = requests.post(url=natural_exercise_endpoint, json=params, headers=headers)
exercise_data = response.json()

# Check if exercise data was fetched successfully
if "exercises" not in exercise_data:
    print("Error fetching exercise data:", exercise_data)
else:
    # Email the exercise data
    yag = yagmail.SMTP(email_address, app_password)
    email_body = "Here is the summary of your exercise data:\n\n"

    for exercise in exercise_data["exercises"]:
        email_body += (
            f"Date: {datetime.now().strftime('%d/%m/%Y')}\n"
            f"Exercise: {exercise['name'].title()}\n"
            f"Duration: {exercise['duration_min']} minutes\n"
            f"Calories Burned: {exercise['nf_calories']} kcal\n\n"
        )

    # Send email
    try:
        yag.send(to=recipient_email, subject="Your Exercise Summary", contents=email_body)
        print("Email sent successfully!")
    except Exception as e:
        print("Error sending email:", e)
