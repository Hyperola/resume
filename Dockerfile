FROM python:3.11-slim
RUN apt-get update && apt-get install -y libmagic1 && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY en_core_web_sm-3.8.0-py3-none-any.whl .
RUN pip install --no-cache-dir en_core_web_sm-3.8.0-py3-none-any.whl
COPY . .
CMD ["python", "app.py"]