import asyncio
from playwright.async_api import async_playwright

async def get_product_price(product_url: str, price_selector: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # Run in headless mode
        page = await browser.new_page()
        await page.goto(product_url)
        
        try:
            # Wait for the price element to load
            await page.wait_for_selector(price_selector, timeout=10000)
            # Extract the text of the price element
            price = await page.text_content(price_selector)
            print(f"The price of the product is: {price}")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            await browser.close()

# Usage
product_url = input("Enter the product URL: ")
price_selector = input("Enter the CSS selector for the price element: ")

asyncio.run(get_product_price(product_url, price_selector))
