    FROM python:3.9-slim-buster

    WORKDIR /app

    COPY black app.py .
    RUN pip install black 
        
        


    COPY . .

    CMD ["python", "app.py"]
