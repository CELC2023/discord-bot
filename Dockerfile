FROM python:3.10-slim

ENV PYTHONPATH = /

WORKDIR /discord

COPY ./.env .

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 3006

CMD ["python", "main.py"]