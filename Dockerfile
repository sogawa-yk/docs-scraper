FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY oracle_docs_scraper.py .

CMD ["python", "oracle_docs_scraper.py"]
