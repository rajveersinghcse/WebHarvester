# WebHarvester

WebHarvester is an advanced Python-based web scraping tool that leverages asynchronous programming to efficiently extract textual content from all internal links of a given website. The scraped data is saved in JSON format for easy manipulation and analysis.

## Features
- Asynchronous URL fetching and content extraction.
- Automatic rate-limiting to avoid overloading servers.
- JSON output for structured data storage.
- Customizable user agent and output file.

## Requirements
- Python 3.7 or later
- Required Python libraries:
  - `aiohttp`
  - `beautifulsoup4`
  - `logging`

Install the dependencies by running:
```bash
pip install -r requirements.txt
```

## Environment Variables
The scraper can be configured with the following environment variables:

- `OUTPUT_FILE`: The filename for saving the scraped content (default: `scraped_content.json`).
- `USER_AGENT`: The User-Agent header for HTTP requests (default: `Mozilla/5.0 (compatible; MyScraper/1.0)`).
- `RATE_LIMIT`: Time delay (in seconds) between successive requests (default: `1.0`).

## Usage
1. Clone the repository:
```bash
git clone https://github.com/rajveersinghcse/webharvester.git
cd webharvester
```

2. Set the environment variables (optional):
```bash
export OUTPUT_FILE="my_scraped_content.json"
export USER_AGENT="MyCustomAgent/1.0"
export RATE_LIMIT="2.0"
```

3. Run the script:
```bash
python webharvester.py
```

4. Enter the website URL when prompted.

5. Check the output file (default: `scraped_content.json`) for the scraped data.

## How It Works
1. **Asynchronous Fetching**:
   - The `fetch_url` function uses `aiohttp` to fetch HTML content asynchronously, improving performance when scraping multiple URLs.

2. **URL Discovery**:
   - The `get_all_urls` function identifies all internal links on the base website and ensures URLs are normalized.

3. **Text Extraction**:
   - The `extract_text_from_url` function removes unnecessary elements (e.g., scripts, styles) and extracts clean text from each page.

4. **Content Saving**:
   - The `save_content_to_json` function writes the extracted content to a JSON file for structured storage.

## Example Output
The JSON output might look like:
```json
{
    "https://example.com/page1": "This is the extracted content of the first page.",
    "https://example.com/page2": "This is the extracted content of the second page."
}
```

## Limitations
- The scraper is designed for static websites and does not support JavaScript-rendered content.
- It only processes internal links.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributions
Contributions are welcome! Please open an issue or submit a pull request to suggest improvements or fix bugs.

## Acknowledgments
- [aiohttp](https://docs.aiohttp.org/) for asynchronous HTTP requests.
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) for HTML parsing.

Happy Scraping! 🚀
