import os
import requests
from datetime import date
from pymongo import MongoClient
import uuid

### setup env variables
GITHUB_PAT = os.getenv("TRAFFIC_ACTION_TOKEN")
GITHUB_OWNER = os.getenv("TRAFFIC_ACTION_OWNER")
GITHUB_REPO = os.environ["TRAFFIC_ACTION_REPO"]

MONGO_USER = os.environ["MONGO_USER"]
MONGO_PASS = os.environ["MONGO_PASS"]
MONGO_URL = os.environ["MONGO_URL"]
MONGO_DATABASE_NAME = os.getenv("MONGO_DATABASE_NAME", "superknowa-app")

current_date = str(date.today())

# Owner and repo details
owner = GITHUB_OWNER
repo = GITHUB_REPO

# Create necessary directories

# Define API endpoint URLs
endpoints = [
    "/repos/{}/{}/traffic/clones".format(owner, repo),
    "/repos/{}/{}/traffic/popular/paths".format(owner, repo),
    "/repos/{}/{}/traffic/popular/referrers".format(owner, repo),
    "/repos/{}/{}/traffic/views".format(owner, repo)
]

# Function to fetch data from GitHub API
def fetch_data(endpoint):
    url = "https://api.github.com" + endpoint
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {GITHUB_PAT}"
    }
    response = requests.get(url, headers=headers)
    return response.json()

track_id = str(uuid.uuid4())

history = {}
history["track_id"] = track_id
history["date"] = current_date
history["data"] = {}

# Loop through the endpoints and fetch traffic data
for endpoint in endpoints:
    data = fetch_data(endpoint)
    file_name = endpoint.split('/')[-1]
    history["data"][file_name] = data
    
summary = {
    "track_id": track_id,
    "day": current_date,
    "clone_count": history["data"]["clones"]["count"],
    "clone_unique": history["data"]["clones"]["uniques"],
    "views_count": history["data"]["views"]["count"],
    "views_unique": history["data"]["views"]["uniques"]
}

print("======================================================")
print(history)
print("======================================================")
print(summary)
print("======================================================")

dbclient = MongoClient(f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_URL}",ssl=True,tlsCAFile="cert/mongo.crt")

mongo_db = dbclient[MONGO_DATABASE_NAME]

history_collection = mongo_db["traffic_history"]
summary_collection = mongo_db["traffic_summary"]


history_collection.insert_one(history)
summary_collection.insert_one(summary)

print("Saved on ", current_date)