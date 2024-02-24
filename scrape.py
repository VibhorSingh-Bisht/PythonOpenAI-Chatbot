#Scrape.py
import asyncio
import logging
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from fpdf import FPDF
import os

logging.basicConfig(level=logging.INFO)

async def remove_unwanted_tags(html_content, unwanted_tags=["script", "style"]):
    """
    Remove unwanted HTML tags from the given HTML content.
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    for tag in unwanted_tags:
        for element in soup.find_all(tag):
            element.decompose()

    return str(soup)

async def extract_tags(html_content, tags, header):
    """
    Extract text content from HTML content based on provided tags and prepend a header.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    text_parts = []

    for tag in tags:
        elements = soup.find_all(tag)
        for element in elements:
            # Remove special characters using regex
            text = re.sub(r'[^\x00-\x7F]+', '', element.get_text())
            # Prepend header to text
            text_with_header = f"{header}: {text}"
            text_parts.append(text_with_header)

    return '\n'.join(text_parts)

async def scrape_page(url, tags, header):
    """
    Scrape content from a given URL based on provided tags and prepend a header.
    """
    logging.info(f"Scraping {url}...")
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    #options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument('log-level=3')
    browser = webdriver.Chrome(options=options)
    
    try:
        browser.get(url)
        page_source = browser.page_source

        cleaned_content = await remove_unwanted_tags(page_source)
        extracted_content = await extract_tags(cleaned_content, tags, header)

        logging.info(f"Content scraped from {url}")
        return extracted_content
    except Exception as e:
        logging.error(f"Error occurred while scraping {url}: {e}")
        return f"Error: {e}"
    finally:
        browser.quit()

async def search_urls(urls_and_tags, headers):
    """
    Scrape content from multiple URLs based on provided tags concurrently and prepend specific headers.
    """
    tasks = []
    for i in range(len(urls_and_tags)):
        url, tags = urls_and_tags[i]
        header = headers[i]
        tasks.append(scrape_page(url, tags, header))
    return await asyncio.gather(*tasks)

async def main():
    """
    Entry point for the script.
    """
    urls_and_tags = [
        ("https://investors.canoo.com/corporate-governance/board-of-directors", ["h1", "h2", "p", "div"]),
        ("https://www.press.canoo.com/", ["h1", "h2", "p", "div"]),
        ("https://www.wsj.com/market-data/quotes/GOEV", ["h1", "h2", "div", "span", "div"]),
        ("https://www.barrons.com/market-data/stocks/goev/company-people?amp%3Biso=XNAS&mod=quotes", ["div", "span"]),
        ("https://www.marketbeat.com/stocks/NYSE/GOEV/profile/", ["h1", "p"]),
        ("https://tracxn.com/d/companies/canoo/__HfVDFR8zT4sJ0XU0CVBHJ1P1CTyblbW8viNKwk579vE/competitors", ["h2", "ul", "p"]),
        ("https://sg.finance.yahoo.com/quote/GOEV/key-statistics/", ["h1", "p", "td"]),
        ("https://www.pwc.com/gx/en/industries/automotive/publications/eascy.html", ["h2", "p", "li"])
    ]

    headers = [
        "Key Players of Canoo",
        "Canoo Info",
        "Canoo Shares Data",
        "Canoo Stocks Data",
        "Canoo Stocks Price, News, and Analysis",
        "Canoo Competitors",
        "Canoo Statistics",
        "Market Trends"
    ]

    results = await search_urls(urls_and_tags, headers)

    pdf = FPDF('P', "mm", 'A4')
    pdf.set_auto_page_break(auto=True, margin=10)
    pdf.add_page()
    pdf.set_font('Arial', '', 16)  # Change font to Arial
    for text_with_header in results:
        paragraphs = text_with_header.split("\n")  # Split text into paragraphs

        for paragraph in paragraphs:
            # Set the starting position of the cell
            pdf.set_x(10)
            pdf.multi_cell(180, 10, paragraph)  # Specify width for the cell
    output_path = f"{os.getcwd()}\\data\\Canoo_data.pdf"
    pdf.output(output_path)

asyncio.run(main())
