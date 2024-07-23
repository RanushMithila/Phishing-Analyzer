import asyncio
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import base64
import time
from fastapi.openapi.utils import get_openapi

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

class URLItem(BaseModel):
    url: str

def extract_content(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    text_content = soup.get_text(separator=' ', strip=True)
    return html_content, text_content

async def take_screenshot(page, screenshot_path):
    await page.screenshot(path=screenshot_path)

@app.post("/scrape/")
async def scrape(url_item: URLItem):
    url = url_item.url
    screenshot_path = 'screenshot-' + str(time.time()) +'.png'

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)
        
        # Wait until the page is fully loaded
        await page.wait_for_selector('body')
        
        # Extract HTML content and text without HTML tags
        html_content = await page.content()
        html_content, text_content = extract_content(html_content)
        
        # Take a screenshot of the webpage
        await take_screenshot(page, screenshot_path)

        await browser.close()
    screenshot_url = f"/static/{screenshot_path}"
    print(screenshot_url)
    
    return {
        "html_content": html_content,
        "text_content": text_content,
        "downloadable_screenshot_path": screenshot_url
    }
