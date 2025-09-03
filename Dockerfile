FROM python:3.13-slim

WORKDIR /tgbot

COPY requirements.txt .

RUN python -m venv /venv \
    && /venv/bin/pip install --upgrade pip setuptools \
    && /venv/bin/pip install -r requirements.txt

COPY new_tgbot.py .
COPY .env .
COPY tgbot.py .

ENV PATH="/venv/bin:$PATH"

CMD ["python3", "new_tgbot.py"]
