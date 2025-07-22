from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
import time

# Function to check if the page is blank
def is_page_blank(driver):
    return driver.execute_script("return document.body.innerText.trim()") == ""

# Set up Chrome options
options = Options()
# options.add_argument("--headless")  # Uncomment for headless mode
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Initialize the WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.set_page_load_timeout(60)
driver.set_script_timeout(60)
wait = WebDriverWait(driver, 30)

# Navigate to Trendyol homepage to handle initial setup
url = 'https://www.trendyol.com'
driver.get(url)
time.sleep(5)

# Check for blank page and refresh if needed
if is_page_blank(driver):
    print("Blank page, refreshing...")
    driver.refresh()
    time.sleep(5)

# Handle cookies
try:
    cookie_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept')]")))
    cookie_button.click()
    print("Cookies accepted.")
    time.sleep(2)
except Exception as e:
    print("Cookie button not found or already accepted:", e)

# Country Selection
try:
    country_select_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'country-select')))
    country_select_button.click()
    print("Country selection opened.")
    time.sleep(1)

    select_element = wait.until(EC.visibility_of_element_located((By.TAG_NAME, 'select')))
    select = Select(select_element)
    select.select_by_value('SA')
    print("Saudi Arabia selected.")
    confirm_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'country-actions')))
    confirm_button.click()
    print("Country confirmed.")
    time.sleep(3)
except Exception as e:
    print("Country selection failed or skipped:", e)

# Arabic Language Selection
try:
    selected_country = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "selected-country-code")))
    selected_country.click()
    print("Language dropdown opened.")
    time.sleep(1)

    language_section = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "language-selection")))
    language_options = language_section.find_elements(By.CLASS_NAME, "radio-button")

    found_arabic = False
    for option in language_options:
        label = option.find_element(By.CLASS_NAME, "radio")
        input_id = label.get_attribute("for")
        if input_id == "ar":
            try:
                input_el = option.find_element(By.CLASS_NAME, "input")
                driver.execute_script("arguments[0].click();", input_el)
                print("Arabic selected.")
                found_arabic = True
                break
            except Exception as e:
                print("Arabic input click failed, trying label:", e)
                driver.execute_script("arguments[0].click();", label)
                found_arabic = True
                break

    if not found_arabic:
        print("Arabic option not found in language selection.")

    save_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@role='button' and contains(@class, 'submit-btn')]")))
    save_button.click()
    print("Language saved as Arabic.")
    time.sleep(3)
except Exception as e:
    print("Language selection failed or skipped:", str(e))

# Get user input for product links
print("Please enter the Trendyol product links (one per line). Press Enter twice to finish:")
product_links = []
while True:
    link = input()
    if link == "":
        break
    if link.startswith('https://www.trendyol.com'):
        product_links.append(link)
    else:
        print(f"Invalid link: {link}. Please provide a valid Trendyol link.")

# Process each product link and add to cart
for idx, link in enumerate(product_links, 1):
    print(f"\nProcessing product {idx}/{len(product_links)}: {link}")
    try:
        driver.get(link)
        time.sleep(5)

        # Check for blank page and refresh if needed
        if is_page_blank(driver):
            print("Blank page, refreshing...")
            driver.refresh()
            time.sleep(5)

        # Locate and click the "Add to Cart" button
        try:
            add_to_cart_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'p-button-wrapper.p-primary.p-large.default')))
            driver.execute_script("arguments[0].scrollIntoView(true);", add_to_cart_button)
            add_to_cart_button.click()
            print(f"Successfully added product {idx} to cart.")
            time.sleep(3)  # Wait for cart update
        except Exception as e:
            print(f"Failed to add product {idx} to cart: {e}")
            continue

    except Exception as e:
        print(f"Failed to process product {idx} ({link}): {e}")
        continue

# Navigate to cart
print("\nAll products added to cart. Navigating to cart...")
try:
    cart_icon = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'basket-preview-icon')))
    driver.execute_script("arguments[0].scrollIntoView(true);", cart_icon)
    cart_icon.click()
    print("Cart opened.")
    time.sleep(5)

    # Check for blank page and refresh if needed
    if is_page_blank(driver):
        print("Cart page is blank, refreshing...")
        driver.refresh()
        time.sleep(5)

    # Proceed to checkout
    try:
        checkout_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'p-button-wrapper.p-primary.p-large.p-fluid.checkout-button')))
        driver.execute_script("arguments[0].scrollIntoView(true);", checkout_button)
        checkout_button.click()
        print("Proceeding to checkout.")
        time.sleep(5)
    except Exception as e:
        print(f"Failed to proceed to checkout: {e}")

except Exception as e:
    print(f"Failed to open cart: {e}")

# Cleanup
print("\nScript execution completed.")
driver.quit()