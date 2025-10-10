FROM python:3.11-slim

WORKDIR /backend

ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
	&& pip install --no-cache-dir gunicorn

COPY flaskapp/ flaskapp/
COPY wsgi.py .
COPY run.py .

EXPOSE 5000

CMD ["python", "run.py"]