from fastapi import FastAPI
import subprocess, os, uuid
import openai

app = FastAPI()

openai.api_key = os.getenv("OPENAI_KEY")

def download(url):
    out = f"video_{uuid.uuid4()}.mp4"
    subprocess.run(["yt-dlp", "-o", out, url])
    return out

def transcribe(video):
    subprocess.run(["whisper", video, "--model", "base"])
    return video.replace(".mp4", ".txt")

def find_clips(text):
    prompt = "Find 3 viral short segments from this transcript. Format: start,end,title\n" + text
    r = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}]
    )
    return r.choices[0].message.content.split("\n")

def cut(video, clips):
    out = []
    for c in clips:
        s,e,t = c.split(",")
        name = f"clip_{uuid.uuid4()}.mp4"
        subprocess.run([
            "ffmpeg","-i",video,
            "-ss",s,"-to",e,
            "-vf","scale=1080:1920",
            name
        ])
        out.append((name,t))
    return out

@app.post("/create")
def create(data:dict):
    video = download(data["url"])
    txt = transcribe(video)
    text = open(txt).read()
    segments = find_clips(text)
    clips = cut(video, segments)
    return {"clips":[{"title":t,"file":f} for f,t in clips]}
