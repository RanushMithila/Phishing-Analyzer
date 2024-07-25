import asyncio
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from PIL import Image
import time
import requests
import os
from dotenv import load_dotenv

load_dotenv()
KEY = os.getenv("BASE_URL")

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

class URLItem(BaseModel):
    url: str
    
def gpt(url, html, text, image):
    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {KEY}"
    }
    
    payload = {
    "model": "gpt-4o",
    "messages": [
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": f"""
            You are a Security Analyst and security expert tasked
            with examining a web page to determine if it is a
            phishing site or a legitimate site. To complete this
            task, follow these sub-tasks:
            1. Analyze the HTML, URL, and extracted text
            look for any SE techniques often used in
            phishing attacks. Point out any suspicious elements
            found in the HTML, URL, or text.
            2. Analyze this Screenshot image look for brand names, sucpicious content, missed alligned images... etc. which will help to identifing phishing site
            3. Identify the brand name. If the HTML appears to
            resemble a legitimate web page, verify if the URL
            matches the legitimate domain name associated with
            the brand, if known.
            4. State your conclusion on whether the site is a
            phishing site or a legitimate one, and explain your
            reasoning. If there is insufficient evidence to make
            a determination, answer "unknown".
            5. Submit your findings as JSON-formatted output with
            the following keys:
            phishing_score: int (indicates phishing risk on a
            scale of 0 to 10)
            brands: str (identified brand name or None if not
            applicable)
            phishing: boolean (whether the site is a phishing
            site or a legitimate site)
            suspicious_domain: boolean (whether the domain name
            is suspected to be not legitimate)
            Limitations:
            The HTML may be shortened and simplified.
            The OCR-extracted text may not always be accurate.
            Examples of social engineering techniques:
            Alerting the user to a problem with their account
            Offering unexpected rewards
            Informing the user of a missing package or additional
            payment required
            Displaying fake security warnings
            URL:
            {url}
            HTML:{html}Text extracted using OCR:{text}
            ScreenShot image:
            """
            },
            {
            "type": "image_url",
            "image_url": {
                "url": f"{image}"
            }
            }
        ]
        }
    ],
    "max_tokens": 1000
    }
    
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    
    return response.json()

def extract_content(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    text_content = soup.get_text(separator=' ', strip=True)
    return html_content, text_content
def image_resize(url, percentage=40):
    # Open an image file
    with Image.open(url) as img:
        # Print the original size of the image
        print("Original size:", img.size)
        
        # Resize the image
        new_size = (int(img.width * percentage / 100), int(img.height * percentage / 100))
        img_resized = img.resize(new_size)
        
        # Save the resized image
        img_resized.save(url)

        # Print the new size of the image
        print("Resized size:", img_resized.size)

async def take_screenshot(page, screenshot_path):
    await page.screenshot(path=screenshot_path)

@app.post("/scrape/")
async def scrape(url_item: URLItem, request: Request):
    url = url_item.url
    screenshot_path = 'static/screenshot-' + str(time.time()) +'.png'

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
        image_resize(screenshot_path, 40)
        scheme = request.url.scheme  # http or https
        host = request.url.hostname  # example.com
        port = request.url.port
        screenshot_path = f"{scheme}://{host}:{port}/{screenshot_path}"
        gpt_output = gpt(url, html_content, text_content, screenshot_path)
    
    return {
        "gpt_response": gpt_output,
        "html_content": html_content,
        "text_content": text_content,
        "downloadable_screenshot_path": screenshot_path
    }
