from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
import os

def is_page_blank(driver):
    return driver.execute_script("return document.body.innerText.trim()") == ""

def scroll_to_bottom_until_loaded(driver, wait_time=2):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(wait_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


options = Options()
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Start driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.set_page_load_timeout(60)
driver.set_script_timeout(60)
wait = WebDriverWait(driver, 30)

product_url = 'https://www.trendyol.com/ar/trendyol-collection/pink-frilly-printed-shorts-knitted-pajamas-set-thmss22pt0422-p-208838522'
driver.get(product_url)
time.sleep(5)

if is_page_blank(driver):
    print("Blank page detected. Refreshing...")
    driver.refresh()
    time.sleep(5)


try:
    cookie_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept')]")))
    cookie_button.click()
    print("Cookies accepted.")
    time.sleep(2)
except Exception as e:
    print("No cookie popup found or already accepted:", e)


try:
    country_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'country-select')))
    country_button.click()
    time.sleep(1)

    select_element = wait.until(EC.visibility_of_element_located((By.TAG_NAME, 'select')))
    select = Select(select_element)
    select.select_by_value('SA')  

    confirm_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'country-actions')))
    confirm_button.click()
    time.sleep(3)
    print("Country set to Saudi Arabia.")
except Exception as e:
    print("Country selection skipped or failed:", e)

try:
    lang_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'selected-country-code')))
    lang_button.click()
    time.sleep(1)

    lang_section = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'language-selection')))
    lang_options = lang_section.find_elements(By.CLASS_NAME, 'radio-button')

    for option in lang_options:
        label = option.find_element(By.CLASS_NAME, "radio")
        if label.get_attribute("for") == "ar":
            input_el = option.find_element(By.CLASS_NAME, "input")
            driver.execute_script("arguments[0].click();", input_el)
            print("Arabic selected.")
            break

    save_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@role='button' and contains(@class, 'submit-btn')]")))
    save_button.click()
    print("Language set to Arabic.")
    time.sleep(3)

    driver.get(product_url)  
    time.sleep(5)
except Exception as e:
    print("Language selection failed or skipped:", e)


try:
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'product-name')))
    print("Arabic product page loaded.")
except Exception as e:
    print("Arabic product page failed to load:", e)


data = []

try:
    name = driver.find_element(By.CLASS_NAME, 'product-info-product-name').text
    price = driver.find_element(By.CLASS_NAME, 'p-sale-price-wrapper').text
    image_url = driver.find_element(By.TAG_NAME, 'img').get_attribute('src')

    bullet_items = "N/A"
    try:
        bullet_elements = driver.find_elements(By.CSS_SELECTOR, ".items.items--bullets .item")
        bullets = [b.text.strip() for b in bullet_elements if b.text.strip()]
        bullet_items = " | ".join(bullets)
    except:
        pass

    rating = "N/A"
    try:
        rating = driver.find_element(By.CLASS_NAME, "average-rating").text
    except:
        pass

    old_price = "N/A"
    try:
        old_price = driver.find_element(By.CLASS_NAME, "p-strikethrough-price").text
    except:
        pass

    shipped_from = "N/A"
    try:
        shipped_from = driver.find_element(By.CSS_SELECTOR, ".shipped-from-info .shipped-from-country .country-name").text
    except:
        pass

    data.append({
        "name": name,
        "price": price,
        "old_price": old_price,
        "rating": rating,
        "bullet_items": bullet_items,
        "image_url": image_url,
        "product_link": product_url,
        "shipped_from": shipped_from
    })

    print(f"Scraped: {name}")

except Exception as e:
    print(f" Failed to extract product info: {e}")



try:
    df = pd.DataFrame(data)
    output_file = "tt.csv"
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"Data saved successfully to {output_file}")
except Exception as e:
    print(f"Failed to save CSV: {e}")

driver.quit()
