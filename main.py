from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import os

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

class URLItem(BaseModel):
    url: str

def extract_content(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    text_content = soup.get_text(separator=' ', strip=True)
    return html_content, text_content

@app.on_event("startup")
async def startup_event():
    os.makedirs("static", exist_ok=True)

@app.post("/scrape/")
async def scrape(url_item: URLItem):
    url = url_item.url
    screenshot_path = 'static/screenshot-' + str(time.time()) + '.png'

    options = Options()
    options.headless = True
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920x1080")
    service = ChromeService(executable_path='/usr/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=options)
    
    driver.get(url)
    
    # Wait until the page is fully loaded
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    
    # Extract HTML content and text without HTML tags
    html_content = driver.page_source
    html_content, text_content = extract_content(html_content)
    
    # Take a screenshot of the webpage
    driver.save_screenshot(screenshot_path)
    driver.quit()
    
    return {
        "html_content": html_content,
        "text_content": text_content,
        "downloadable_screenshot_path": screenshot_path
    }
