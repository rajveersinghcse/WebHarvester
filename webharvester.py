import os
import asyncio
import aiohttp
import logging
import json
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

OUTPUT_FILE = os.getenv("OUTPUT_FILE", "scraped_content.json")
USER_AGENT = os.getenv("USER_AGENT", "Mozilla/5.0 (compatible; MyScraper/1.0)")
RATE_LIMIT = float(os.getenv("RATE_LIMIT", "1.0"))


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

scraped_content_cache = {}


async def fetch_url(session, url):
    try:
        headers = {"User-Agent": USER_AGENT}
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                return await response.text()
            else:
                logging.warning(f"Failed to fetch {url}: Status {response.status}")
    except Exception as e:
        logging.error(f"Error fetching {url}: {e}")


async def get_all_urls(base_url):
    urls = set()
    async with aiohttp.ClientSession() as session:
        html = await fetch_url(session, base_url)
        if html:
            soup = BeautifulSoup(html, "html.parser")
            for link in soup.find_all("a", href=True):
                url = link["href"]
                full_url = urljoin(base_url, url)
                parsed_url = urlparse(full_url)
                if parsed_url.netloc == urlparse(base_url).netloc:
                    normalized_url = (
                        f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
                    )
                    urls.add(normalized_url)
    return urls


async def extract_text_from_url(session, url):
    try:
        html = await fetch_url(session, url)
        if html:
            soup = BeautifulSoup(html, "html.parser")
            for script in soup(["script", "style"]):
                script.decompose()
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            return " ".join(chunk for chunk in chunks if chunk)
    except Exception as e:
        logging.error(f"Error extracting text from {url}: {e}")


async def scrape_all_content(base_url):
    global scraped_content_cache

    if scraped_content_cache:
        logging.info("Using cached content.")
        return scraped_content_cache

    urls = await get_all_urls(base_url)
    content = {}

    async with aiohttp.ClientSession() as session:
        for url in urls:
            page_content = await extract_text_from_url(session, url)
            if page_content:
                content[url] = page_content
            await asyncio.sleep(RATE_LIMIT)

    scraped_content_cache = content
    save_content_to_json(OUTPUT_FILE, content)
    logging.info("Scraping completed and saved.")
    return content


def save_content_to_json(filename, content):
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(content, file, indent=4)
        logging.info(f"Content saved to {filename}")
    except Exception as e:
        logging.error(f"Error saving content to file {filename}: {e}")


def main():
    try:
        print("Please Enter the full url of website.\nExample: https://www.example.com")
        baseurl = input("Please give your URL: ").strip()
        logging.info("Starting the scraper...")
        asyncio.run(scrape_all_content(baseurl))
    except KeyboardInterrupt:
        logging.info("Scraper stopped by user.")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
