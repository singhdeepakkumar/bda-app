FROM python:3.9-alpine
COPY . /app
COPY app_model /app/app_model
RUN apt-get update && apt-get install -y gcc
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app:app"]

