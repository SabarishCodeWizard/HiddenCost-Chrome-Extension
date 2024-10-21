# app.py
import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
from flask import Flask, request, jsonify
from flask_cors import CORS

# Define Flask app instance
app = Flask(__name__)  
CORS(app)

# Initialize SQLite Database
def init_db():
    conn = sqlite3.connect('product_comparison.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS product_comparison (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amazon_title TEXT,
            amazon_price REAL,
            flipkart_price REAL,
            flipkart_mrp REAL,
            offer_percentage TEXT,
            product_link TEXT,
            comparison_result TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Insert data into SQLite Database
def insert_into_db(amazon_title, amazon_price, flipkart_price, flipkart_mrp, offer_percentage, product_link, comparison_result):
    conn = sqlite3.connect('product_comparison.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO product_comparison (
            amazon_title, amazon_price, flipkart_price, flipkart_mrp, 
            offer_percentage, product_link, comparison_result
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (amazon_title, amazon_price, flipkart_price, flipkart_mrp, offer_percentage, product_link, comparison_result))
    conn.commit()
    conn.close()

# Fetch data from SQLite Database (optional for further use)
def fetch_data_from_db():
    conn = sqlite3.connect('product_comparison.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM product_comparison')
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_flipkart_price(product_titles):
    flipkart_data = []
    
    # Specify the path to the Edge WebDriver if not in PATH
    driver = webdriver.Edge()  # Edge WebDriver initialization
    
    for product_title in product_titles:
        flipkart_url = f"https://www.flipkart.com/search?q={product_title.replace(' ', '+')}"
        driver.get(flipkart_url)
        
        time.sleep(3)  # Allow time for the page to load
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Offered price selector
        price_element = soup.select_one('#container > div > div.nt6sNV.JxFEK3._48O0EI > div.DOjaWF.YJG4Cf > div:nth-child(2) > div:nth-child(2) > div > div > div > a > div.yKfJKb.row > div.col.col-5-12.BfVC2z > div.cN1yYO > div.hl05eU > div.Nx9bqj._4b5DiR')
        # MRP selector
        mrp_element = soup.select_one('#container > div > div.nt6sNV.JxFEK3._48O0EI > div.DOjaWF.YJG4Cf > div:nth-child(2) > div:nth-child(2) > div > div > div > a > div.yKfJKb.row > div.col.col-5-12.BfVC2z > div.cN1yYO > div.hl05eU > div.yRaY8j.ZYYwLA')
        # Offered percentage selector
        offer_percentage_element = soup.select_one('#container > div > div.nt6sNV.JxFEK3._48O0EI > div.DOjaWF.YJG4Cf > div:nth-child(2) > div:nth-child(2) > div > div > div > a > div.yKfJKb.row > div.col.col-5-12.BfVC2z > div.cN1yYO > div.hl05eU > div.UkUFwK > span')
        
        product_link_element = soup.select_one('a._1fQZEK')

        if price_element:
            flipkart_price = price_element.text.strip().replace('₹', '').replace(',', '')
        else:
            flipkart_price = "Product not available on Flipkart"

        if mrp_element:
            flipkart_mrp = mrp_element.text.strip().replace('₹', '').replace(',', '')
        else:
            flipkart_mrp = "MRP not available"

        if offer_percentage_element:
            flipkart_offer_percentage = offer_percentage_element.text.strip()
        else:
            flipkart_offer_percentage = "Offered percentage not available"
        
        # Ensure product_link is always present
        product_link = f"https://www.flipkart.com{product_link_element['href']}" if product_link_element else "Product link not available"


        flipkart_data.append({
            "price": flipkart_price,
            "mrp": flipkart_mrp,
            "offer_percentage": flipkart_offer_percentage,
            "product_link": product_link  # Add product link to the data
        })
    
    driver.quit()
    
    return flipkart_data

@app.route('/compare', methods=['POST'])
def compare_prices():
    request_data = request.json
    amazonProductTitles = request_data.get('amazon_product_title')
    amazonProductPrices = request_data.get('amazon_product_price')

    flipkart_data = get_flipkart_price(amazonProductTitles)

    comparison_results = []

    for flipkart_info, amazon_price in zip(flipkart_data, amazonProductPrices):
        if amazon_price is None:
            comparison_result = "Unable to compare. Amazon price not available."
        elif flipkart_info["price"] == "Product not available on Flipkart":
            comparison_result = "Price not available on Flipkart"
        else:
            try:
                flipkart_price_float = float(flipkart_info["price"].replace(',', ''))
                if flipkart_price_float < amazon_price:
                    comparison_result = "Flipkart price is lower than Amazon price."
                elif flipkart_price_float > amazon_price:
                    comparison_result = "Flipkart price is higher than Amazon price."
                else:
                    comparison_result = "Flipkart price is the same as Amazon price."
            except ValueError:
                comparison_result = "Error: Unable to convert Flipkart price to float."

                
        # Insert comparison data into the SQLite database
        insert_into_db(
            amazon_title=amazonProductTitles[flipkart_data.index(flipkart_info)],
            amazon_price=amazon_price,
            flipkart_price=flipkart_info["price"],
            flipkart_mrp=flipkart_info["mrp"],
            offer_percentage=flipkart_info["offer_percentage"],
            product_link=flipkart_info["product_link"],
            comparison_result=comparison_result
        )

        comparison_results.append(comparison_result)

    response_data = {
        'flipkart_data': flipkart_data,
        'amazon_prices': amazonProductPrices,
        'comparison_results': comparison_results
    }

    return jsonify(response_data)

if __name__ == '__main__':
    init_db()  # Initialize the database when the app starts
    app.run(debug=True, port=5010)
