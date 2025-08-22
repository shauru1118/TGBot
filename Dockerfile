FROM python:3.13

WORKDIR /tgbot

COPY . .

RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt

CMD ["python3", "./main.py"]

