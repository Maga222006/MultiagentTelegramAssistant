FROM python:3.11

LABEL authors="magomedpatahov"

WORKDIR /app

COPY . .

# Set permissions for SQLite database and containing directory
RUN mkdir -p /app/database && \
    chmod 775 /app/database && \
    touch /app/database/main.db && \
    chmod 664 /app/database/main.db

RUN pip install -U -r requirements.txt

CMD ["python", "main.py"]