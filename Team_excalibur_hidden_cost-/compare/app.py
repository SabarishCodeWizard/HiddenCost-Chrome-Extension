import asyncio
from playwright.async_api import async_playwright
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Function to scrape Flipkart prices
async def get_flipkart_price(product_titles):
    flipkart_prices = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        for product_title in product_titles:
            product_title_encoded = product_title.replace(' ', '+')
            flipkart_url = f"https://www.flipkart.com/search?q={product_title_encoded}"
            
            try:
                await page.goto(flipkart_url)
                
                # Wait for the product container to appear (use a more specific wait)
                await page.wait_for_selector('//div[contains(@class, "_1AtVbE")]', timeout=45000)
                
                # Try to extract the first product price
                product_cards = await page.query_selector_all('//div[contains(@class, "_1AtVbE")]')

                # Iterate through the product cards to find price and title
                for card in product_cards:
                    title_element = await card.query_selector('a > div:nth-child(3) > div:nth-child(1)')
                    price_element = await card.query_selector('a > div:nth-child(3) > div:nth-child(2) > div:nth-child(1)')
                    
                    if title_element and price_element:
                        title_text = await title_element.text_content()
                        price_text = await price_element.text_content()
                        
                        # Clean and extract the price
                        price = price_text.strip().replace('₹', '').replace(',', '')
                        
                        flipkart_prices.append(price)
                        break  # Exit after finding the first valid product
                
                if not flipkart_prices:
                    flipkart_prices.append('Error: No price found for this product.')
                
            except Exception as e:
                flipkart_prices.append(f"Error fetching price: {str(e)}")
        
        await browser.close()
    
    return flipkart_prices





# # New endpoint to fetch Flipkart prices only
# @app.route('/fetch_flipkart', methods=['POST'])
# def fetch_flipkart_prices():
#     request_data = request.json
#     product_titles = request_data.get('product_titles')

#     # Fetch Flipkart prices using Playwright
#     flipkart_prices = asyncio.run(get_flipkart_price(product_titles))

#     response_data = {
#         'flipkart_prices': flipkart_prices
#     }

#     return jsonify(response_data)

# Comparison endpoint (remains unchanged)
@app.route('/compare', methods=['POST'])
def compare_prices():
    request_data = request.json
    amazonProductTitles = request_data.get('amazon_product_title')
    amazonProductPrices = request_data.get('amazon_product_price')

    # Fetch Flipkart prices
    flipkart_prices = asyncio.run(get_flipkart_price(amazonProductTitles))

    comparison_results = []
    for flipkart_price, amazon_price in zip(flipkart_prices, amazonProductPrices):
        if amazon_price is None:
            comparison_result = "Unable to compare. Amazon price not available."
        elif flipkart_price == "Product not available on Flipkart":
            comparison_result = "Price not available on Flipkart."
        else:
            try:
                flipkart_price_float = float(flipkart_price.replace(',', ''))
                if flipkart_price_float < amazon_price:
                    comparison_result = "Flipkart price is lower than Amazon price."
                elif flipkart_price_float > amazon_price:
                    comparison_result = "Flipkart price is higher than Amazon price."
                else:
                    comparison_result = "Flipkart price is the same as Amazon price."
            except ValueError:
                comparison_result = "Error: Unable to convert Flipkart price to float."

        comparison_results.append(comparison_result)

    response_data = {
        'flipkart_prices': flipkart_prices,
        'amazon_prices': amazonProductPrices,
        'comparison_results': comparison_results
    }

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True, port=5010)
