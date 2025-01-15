    FROM python:3.9-slim-buster

    WORKDIR /app

    COPY requirements.txt .
    RUN pip install -r requirements.txt 
        pip install black
        black app.py


    COPY . .

    CMD ["python", "app.py"]
