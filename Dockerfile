FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

#ENV INVENTORY_URL=inventory_url

COPY batch_job.py .

CMD ["python", "batch_job.py"]