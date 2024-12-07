from fastapi import FastAPI, HTTPException
import requests
from fastapi.middleware.cors import CORSMiddleware
from config import GITHUB_API_URL, FE_DOMAIN

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    # allow_origins=[FE_DOMAIN],  # Replace with your frontend domain
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/projects")
async def get_projects():
    if GITHUB_API_URL is None:
        raise HTTPException(status_code=500, detail="GITHUB_API_URL is not configured.")

    response = requests.get(GITHUB_API_URL)
    if response.status_code == 200:
        data = response.json()
        projects = [
            {
                "name": project["name"],
                "html_url": project["html_url"],
                "description": project.get("description"),
                "language": project.get("language") if project.get("language") else "N/A",
                "updated_at": project["updated_at"]
            }
            for project in data
        ]
        return {"projects": projects}
    else:
        raise HTTPException(status_code=response.status_code, detail="Unable to fetch projects.")
