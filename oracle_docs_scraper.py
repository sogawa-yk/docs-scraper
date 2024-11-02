import requests
from bs4 import BeautifulSoup
import os
import urllib.parse

# ベースURLの設定
base_url = "https://docs.oracle.com/ja-jp/iaas/Content/ContEng/"
visited_links = set()

# HTMLファイルの保存ディレクトリ
save_dir = "/mnt/htmls"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# リンクの取得と保存を行う関数
def scrape_links(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        # 現在のURLのHTMLを保存
        save_html(url, response.content)

        # aタグからリンクを取得
        links = soup.find_all("a")
        for link in links:
            href = link.get("href")
            if href:
                full_url = urllib.parse.urljoin(url, href)
                if full_url.startswith(base_url) and full_url not in visited_links:
                    visited_links.add(full_url)
                    scrape_links(full_url)
    except requests.RequestException as e:
        print(f"Error accessing {url}: {e}")

# HTMLファイルを保存する関数
def save_html(url, content):
    parsed_url = urllib.parse.urlparse(url)
    file_name = parsed_url.path.strip("/").replace("/", "_")
    if not file_name:
        file_name = "index"
    file_path = os.path.join(save_dir, f"{file_name}.html")
    with open(file_path, "wb") as file:
        file.write(content)
    print(f"Saved: {file_path}")

# スクレイピング開始
scrape_links(base_url)
