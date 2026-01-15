FROM python:3.10

RUN apt update && apt install -y ffmpeg

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

CMD ["uvicorn","main:app","--host","0.0.0.0","--port","10000"]
