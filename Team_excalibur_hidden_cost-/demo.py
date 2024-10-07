from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options as EdgeOptions
import time

# Initialize Edge WebDriver
edge_options = EdgeOptions()
edge_options.add_argument("--start-maximized")
driver = webdriver.Edge(options=edge_options)

# URL of the Amazon product page (replace with the product's link)
amazon_product_url = "https://www.amazon.in/gp/product/B0B2WQFHB2/ref=ewc_pr_img_1?smid=AJ6SIZC8YQDZX&psc=1"

try:
    # Step 1: Open the product page
    driver.get(amazon_product_url)
    time.sleep(5)  # Wait for the page to load

    # Step 2: Click on the 'Buy Now' button
    buy_now_button = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.ID, "buy-now-button"))
    )
    buy_now_button.click()

    # Step 3: Wait for checkout page to load and select 'Cash on Delivery' payment method
    time.sleep(5)  # Adjust if necessary for page load time

    # Switch to iframe if necessary (check if element is in iframe)
    # Uncomment the next line if element is inside an iframe
    # driver.switch_to.frame(driver.find_element(By.XPATH, "//iframe[@id='desired-iframe-id']"))

    # Debug: Print page source to verify if page loaded correctly
    # print(driver.page_source)  # Use this to inspect if elements are loaded properly

    # Find and click on 'Cash on Delivery/Pay on Delivery'
    cod_payment_option = WebDriverWait(driver, 40).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='pp-QPHVev-161']/div/div/div/div/div[2]/div[1]/div/span[1]"))
    )
    cod_payment_option.click()

    # Step 4: Click 'Use this payment method'
    use_this_payment_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='pp-QPHVev-164']/span/input"))
    )
    use_this_payment_button.click()

    time.sleep(3)  # Allow page to update

    # Step 5: Scrape delivery and total order amounts
    delivery_amount = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "#subtotals-marketplace-table > tbody > tr:nth-child(2) > td.a-text-right.aok-nowrap.a-nowrap"))
    ).text

    order_total = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "#subtotals-marketplace-table > tbody > tr:nth-child(4) > td.a-color-price.a-size-medium.a-text-right.grand-total-price.aok-nowrap.a-text-bold.a-nowrap"))
    ).text

    # Step 6: Print the scraped amounts
    print(f"Delivery Amount: {delivery_amount}")
    print(f"Order Total Amount: {order_total}")

    # Optional: Return these values in your response to be handled in Chrome Extension
    result = {
        'Delivery:': delivery_amount,
        'Total:': order_total
    }

except Exception as e:
    print(f"An error occurred: {str(e)}")
    # Optionally print the page source for debugging
    print(driver.page_source)

finally:
    # Close the browser
    driver.quit()
