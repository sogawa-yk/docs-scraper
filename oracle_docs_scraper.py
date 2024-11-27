import requests
from bs4 import BeautifulSoup
import os
import urllib.parse
import sys

# 再帰の深さの制限を設定
sys.setrecursionlimit(1000)

# ベースURLの設定
base_url = "https://docs.oracle.com/ja-jp/iaas/Content/home.htm"
# ベースURLからドメインとベースパスを取得
parsed_base = urllib.parse.urlparse(base_url)
base_domain = f"{parsed_base.scheme}://{parsed_base.netloc}"

visited_links = set()

# HTMLファイルの保存ディレクトリ
save_dir = "/mnt/htmls"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

def is_valid_url(url, current_section):
    """URLが現在のセクション内のものかチェックする"""
    if not url.startswith(base_domain):
        return False
    
    # 現在のセクションのパスを取得（例：/ja-jp/iaas/Content/APIGateway/）
    if current_section:
        return url.startswith(current_section)
    return True

def get_section_base(url):
    """URLからセクションのベースパスを取得する"""
    parsed = urllib.parse.urlparse(url)
    path_parts = parsed.path.split('/')
    
    # Content/の次の部分までをセクションとして扱う
    try:
        content_index = path_parts.index('Content')
        if content_index + 1 < len(path_parts):
            section_parts = path_parts[:content_index + 2]
            return f"{base_domain}{'/'.join(section_parts)}/"
    except ValueError:
        return None
    return None

def scrape_links(url, depth=0, current_section=None):
    if depth > 10:
        print(f"Warning: Maximum depth reached for {url}")
        return
    
    try:
        response = requests.get(url)
        if response.status_code == 404:
            print(f"Warning: Page not found - {url}")
            return
        
        response.raise_for_status()
        
        try:
            soup = BeautifulSoup(response.content.decode('utf-8', errors='ignore'), "html.parser")
            
            # 最初のページの場合
            if depth == 0:
                # 最初のページのリンクを取得して処理
                initial_links = soup.find_all("a")
                for link in initial_links:
                    href = link.get("href")
                    if href:
                        full_url = urllib.parse.urljoin(url, href)
                        section_base = get_section_base(full_url)
                        if section_base:
                            print(f"Found section: {section_base}")
                            if full_url not in visited_links:
                                visited_links.add(full_url)
                                print(f"Processing initial link: {full_url}")
                                # 各セクションのベースURLから再帰的に処理開始
                                scrape_links(full_url, depth=1, current_section=section_base)
            else:
                # 2階層目以降の処理
                if is_valid_url(url, current_section):
                    links = soup.find_all("a")
                    for link in links:
                        href = link.get("href")
                        if href:
                            full_url = urllib.parse.urljoin(url, href)
                            if (is_valid_url(full_url, current_section) and 
                                full_url not in visited_links):
                                visited_links.add(full_url)
                                print(f"Found link: {full_url}")
                                scrape_links(full_url, depth + 1, current_section)
                
        except Exception as e:
            print(f"Warning: Failed to parse HTML from {url}: {e}")
            return

        save_html(url, response.content)
        
    except requests.RequestException as e:
        print(f"Error accessing {url}: {e}")

# HTMLファイルを保存する関数は変更なし
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
scrape_links(base_url, depth=0)
