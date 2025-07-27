# Dockerfile

FROM --platform=linux/amd64 python:3.10-slim
WORKDIR /app

COPY app /app/app
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app/pdf_extractor.py"]
