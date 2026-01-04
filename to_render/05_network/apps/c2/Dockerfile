FROM python:3.11-slim
WORKDIR /app
RUN pip install fastapi uvicorn requests
COPY consumer_api.py .
CMD ["uvicorn", "consumer_api:app", "--host", "0.0.0.0", "--port", "8001"]