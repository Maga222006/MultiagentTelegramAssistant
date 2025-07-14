FROM python:3.11

LABEL authors="magomedpatahov"

WORKDIR /app

COPY . .

RUN pip install -U -r requirements.txt

CMD ["python", "main.py"]