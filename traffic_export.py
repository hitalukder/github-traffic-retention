import os
import json
import requests
from datetime import date

### setup env variables
GITHUB_PAT = os.getenv("TRAFFIC_ACTION_TOKEN")
GITHUB_OWNER = os.getenv("TRAFFIC_ACTION_OWNER")
GITHUB_REPO = os.environ["TRAFFIC_ACTION_REPO"]

# output directory
output_dir = "traffic"
output_file = "output.csv"

current_date = str(date.today())

# Create a directory with the current date as the directory name
if(os.path.exists(output_dir) is False):
    os.mkdir(output_dir)

# path would be traffic/<current_date>
if(os.path.exists(os.path.join(output_dir, current_date)) is False):
    os.mkdir(os.path.join(output_dir, current_date))


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

# Loop through the endpoints and fetch traffic data
for endpoint in endpoints:
    data = fetch_data(endpoint)
    with open(os.path.join(output_dir, current_date, endpoint.split('/')[-1] + ".json"), "w") as f:
        json.dump(data, f)


# Write summary to a CSV file
with open(os.path.join(output_dir, "summary.csv"), "a") as summary_file:
    summary_file.write(
        "{},{},{},{},{}\n".format(
            current_date,
            json.loads(open(os.path.join(output_dir, current_date, "clones.json")).read())["count"],
            json.loads(open(os.path.join(output_dir, current_date, "clones.json")).read())["uniques"],
            json.loads(open(os.path.join(output_dir, current_date, "views.json")).read())["count"],
            json.loads(open(os.path.join(output_dir, current_date, "views.json")).read())["uniques"]
        )
    )
