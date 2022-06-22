FROM python:3.9-slim


RUN mkdir /code
WORKDIR /code
RUN mkdir -p config

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000
ENTRYPOINT [ "python3", "main.py"]
