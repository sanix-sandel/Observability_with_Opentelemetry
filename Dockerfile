FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

ENV INVENTORY_URL=http://localhost:5001

COPY grocery_store.py .
COPY common.py .
COPY local_machine_resource_detector.py .

CMD ["python", "grocery_store.py"]