FROM python:3.9
WORKDIR /app
COPY requirements.txt .  
# Install system dependencies

RUN apt-get update && apt-get install -y gcc

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
