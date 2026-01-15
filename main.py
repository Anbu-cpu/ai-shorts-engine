from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
import subprocess, os, uuid
import openai
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

app = FastAPI()

openai.api_key = os.getenv("OPENAI_KEY")

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

REDIRECT_URI = "https://ai-shorts-engine-7.onrender.com/oauth2callback"

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

@app.get("/")
def home():
    return {"status": "AI Shorts Engine is running"}

@app.get("/login")
def login():
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [REDIRECT_URI]
            }
        },
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )

    auth_url, _ = flow.authorization_url(prompt="consent")
    return RedirectResponse(auth_url)

@app.get("/oauth2callback")
def callback(request: Request):
    return {"status": "YouTube connected successfully"}
