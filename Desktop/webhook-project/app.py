from flask import Flask, request
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Connect to MongoDB
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client["webhook_db"]
collection = db["github_events"]

@app.route("/", methods=["GET"])
def home():
    return "Webhook Receiver is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    event = request.headers.get('X-GitHub-Event')
    payload = request.json
    if event and payload:
        collection.insert_one({"event": event, "payload": payload})
        return {"status": "saved"}, 200
    return {"status": "ignored"}, 400

if __name__ == "__main__":
    app.run(debug=True)
