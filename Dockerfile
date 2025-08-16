FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt && pip install gunicorn
COPY . /app
RUN useradd -m appuser
USER appuser
ENV PORT=8000
EXPOSE 8000
CMD ["gunicorn","-w","2","-k","gthread","-b","0.0.0.0:8000","app:app","--threads","4","--timeout","60"]
