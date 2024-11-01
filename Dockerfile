FROM python:3.9-slim

# 作業ディレクトリを設定
WORKDIR /app

# 必要なPythonパッケージをインストール
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# スクレイピングスクリプトをコピー
COPY oracle_docs_scraper.py oracle_docs_scraper.py

# スクリプトを実行
CMD ["python", "oracle_docs_scraper.py"]
