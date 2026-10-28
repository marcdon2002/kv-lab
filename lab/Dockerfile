FROM python:3.12-slim

RUN pip install --no-cache-dir redis==5.2.1

WORKDIR /app
COPY demos.py .

ENTRYPOINT ["python", "-u", "/app/demos.py"]
CMD ["help"]
