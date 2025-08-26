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
COPY tgbot.py .
COPY test.py .

# use venv python by default
ENV PATH="/venv/bin:$PATH"

CMD ["python", "tgbot.py"]
