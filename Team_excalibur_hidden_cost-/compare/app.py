from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def get_flipkart_price(product_titles):
    flipkart_prices = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        for title in product_titles:
            # Search for the product on Flipkart
            page.goto(f"https://www.flipkart.com/search?q={title}")
            page.wait_for_selector('div._1AtVbE')  # Wait for the main search results container
            
            # Now, select the first product listed
            first_product = page.query_selector('div._1AtVbE div._2kHMtA')
            if first_product:
                first_product.click()
                
                # Wait for the product page to load and the price to be visible
                page.wait_for_selector('div.Nx9bqj.CxhGGd')  # Updated price class
                price_element = page.query_selector('div.Nx9bqj.CxhGGd')
                
                if price_element:
                    price = price_element.inner_text()  # Extract the price text
                    flipkart_prices.append(price)
                else:
                    flipkart_prices.append("Price not found")
            else:
                flipkart_prices.append("Product not found")
        
        browser.close()
    
    return flipkart_prices


@app.route('/compare', methods=['POST'])
def compare_prices():
    # Retrieve data from the request JSON
    request_data = request.json
    amazonProductTitles = request_data.get('amazon_product_title')
    amazonProductPrices = request_data.get('amazon_product_price')

    # Fetch the Flipkart prices for the stored Amazon product titles
    flipkart_prices = get_flipkart_price(amazonProductTitles)

    # Initialize lists to store comparison results
    comparison_results = []

    # Compare each Flipkart price with the corresponding Amazon price
    for flipkart_price, amazon_price in zip(flipkart_prices, amazonProductPrices):
        if amazon_price is None:
            comparison_result = "Unable to compare. Amazon price not available."
        elif flipkart_price == "Product not available on Flipkart":
            comparison_result = "Price not available on Flipkart"
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
