FROM python:3.11-slim-bullseye

WORKDIR /app

ENV TZ=Asia/Bangkok

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["fastapi", "run", "main.py" ,"--host", "0.0.0.0", "--port", "80"]