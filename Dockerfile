FROM python:3.12
WORKDIR /app

COPY src/main.py .

COPY requeriments.txt .

RUN pip install -r requeriments.txt

CMD [ "python", "main.py" ]