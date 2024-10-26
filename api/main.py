# api/main.py
from fastapi import FastAPI
import requests
from .config import GITHUB_API_URL

app = FastAPI()


@app.get("/projects")
async def get_projects():
    response = requests.get(GITHUB_API_URL)
    if response.status_code == 200:
        data = response.json()
        # Extract only relevant fields from the response
        projects = [
            {
                "name": project["name"],
                "html_url": project["html_url"],
                "description": project.get("description"),
                "language": project.get("language"),
                "updated_at": project["updated_at"]
            }
            for project in data
        ]
        return {"projects": projects}
    else:
        return {"error": "Unable to fetch projects"}, response.status_code
