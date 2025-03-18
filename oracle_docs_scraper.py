import os
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class OracleDocsScraper:
    def __init__(self, base_url, output_dir):
        self.base_url = base_url
        self.output_dir = output_dir
        self.visited_urls = set()
        self.session = requests.Session()
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

    def is_valid_url(self, url):
        """Check if the URL is within the OCI documentation domain"""
        parsed_url = urlparse(url)
        return (
            parsed_url.netloc == 'docs.oracle.com' and
            '/iaas/Content/' in parsed_url.path and
            not any(ext in url for ext in ['.pdf', '.zip', '.png', '.jpg', '.jpeg', '.gif'])
        )

    def save_page(self, url, html_content):
        """Save HTML content to a file"""
        try:
            # Create a file path based on the URL structure
            parsed_url = urlparse(url)
            path_parts = parsed_url.path.strip('/').split('/')
            
            # Remove 'iaas' and 'Content' from path if present to avoid deep nesting
            if 'iaas' in path_parts:
                path_parts.remove('iaas')
            if 'Content' in path_parts:
                path_parts.remove('Content')
            
            # Create the file path
            rel_path = '/'.join(path_parts)
            if not rel_path:
                rel_path = 'index'
            if not rel_path.endswith('.html'):
                rel_path += '.html'
            
            file_path = os.path.join(self.output_dir, rel_path)
            
            # Create necessary directories
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # Save the content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            logging.info(f"Saved: {file_path}")
            
        except Exception as e:
            logging.error(f"Error saving {url}: {str(e)}")

    def get_links(self, url, html_content):
        """Extract valid links from HTML content"""
        soup = BeautifulSoup(html_content, 'html.parser')
        links = set()
        
        for a in soup.find_all('a', href=True):
            href = a['href']
            absolute_url = urljoin(url, href)
            
            if self.is_valid_url(absolute_url) and absolute_url not in self.visited_urls:
                links.add(absolute_url)
        
        return links

    def scrape(self):
        """Main scraping method"""
        urls_to_visit = {self.base_url}
        
        while urls_to_visit:
            url = urls_to_visit.pop()
            if url in self.visited_urls:
                continue
                
            try:
                logging.info(f"Scraping: {url}")
                response = self.session.get(url)
                response.raise_for_status()
                
                # Add delay to be polite
                time.sleep(1)
                
                # Save the page
                self.save_page(url, response.text)
                
                # Mark as visited
                self.visited_urls.add(url)
                
                # Get new links and add them to the queue
                new_links = self.get_links(url, response.text)
                urls_to_visit.update(new_links)
                
            except Exception as e:
                logging.error(f"Error processing {url}: {str(e)}")

def main():
    base_url = "https://docs.oracle.com/ja-jp/iaas/Content/home.htm"
    output_dir = "htmls"
    
    scraper = OracleDocsScraper(base_url, output_dir)
    scraper.scrape()

if __name__ == "__main__":
    main()
