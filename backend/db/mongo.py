from pymongo import MongoClient
import json
from dotenv import load_dotenv
import os


load_dotenv()


client = MongoClient(os.getenv("MONGO_URI"))
db = client["venture_db"]

def seed_meeting_logs():
    json_path = os.path.join(os.getcwd(), "data", "meeting_logs_250.json")

    with open(json_path, "r") as file:
        logs = json.load(file)  # assumes it's a list of objects

    db.meetings.insert_many(logs)
    print(f"Imported {len(logs)} meeting logs into MongoDB")

def get_declined_investors(entrepreneur_id):
    declined = db.meetings.find(
        {"entrepreneur_id": entrepreneur_id, "status": "declined"},
        {"investor_id": 1, "_id": 0}
    )
    return [doc["investor_id"] for doc in declined]
