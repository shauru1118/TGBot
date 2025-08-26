FROM python:3.13-slim

# set working directory
WORKDIR /tgbot

# copy requirements first (for caching)
COPY requirements.txt .

# install deps directly into a venv and update PATH
RUN python -m venv /venv \
    && /venv/bin/pip install --upgrade pip setuptools \
    && /venv/bin/pip install -r requirements.txt

# copy bot code
COPY new_tgbot.py .
COPY .env .

# use venv python by default
ENV PATH="/venv/bin:$PATH"

CMD ["python3", "new_tgbot.py"]
