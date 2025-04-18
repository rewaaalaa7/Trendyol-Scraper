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

def is_page_blank(driver):
    return driver.execute_script("return document.body.innerText.trim()") == ""

def scroll_to_bottom_until_loaded(driver, wait_time=2):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(wait_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            print("🔻 Reached bottom of the page.")
            break
        last_height = new_height
        print("⬇️ Scrolling...")

# Setup
options = Options()
# options.add_argument("--headless")  # Uncomment for headless mode
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Set timeouts to handle long-running scripts
driver.set_page_load_timeout(60)  # Timeout for page load
driver.set_script_timeout(60)     # Timeout for scripts execution

# Increase WebDriver Wait Time to 30 seconds
wait = WebDriverWait(driver, 30)

url = 'https://www.trendyol.com/ar/sr?q=cosmetics&qt=cosmetics&st=cosmetics&os=1'
driver.get(url)
time.sleep(5)

if is_page_blank(driver):
    print("⚪ Blank page, refreshing...")
    driver.refresh()
    time.sleep(5)

# Handle cookies
try:
    cookie_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept')]")))
    cookie_button.click()
    print("✅ Cookies accepted.")
    time.sleep(2)
except Exception as e:
    print("⚠️ Cookie button not found or already accepted:", e)

# Country Selection
try:
    country_select_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'country-select')))
    country_select_button.click()
    print("🌍 Country selection opened.")
    time.sleep(1)

    select_element = wait.until(EC.visibility_of_element_located((By.TAG_NAME, 'select')))
    select = Select(select_element)
    select.select_by_value('SA')  # Saudi Arabia
    print("✅ Saudi Arabia selected.")

    confirm_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'country-actions')))
    confirm_button.click()
    print("✅ Country confirmed.")
    time.sleep(3)
except Exception as e:
    print("⚠️ Country selection failed or skipped:", e)

# Robust Arabic Language Selection
try:
    selected_country = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "selected-country-code")))
    selected_country.click()
    print("🌐 Language dropdown opened.")
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
                print("🈸 Arabic selected.")
                found_arabic = True
                break
            except Exception as e:
                print("⚠️ Arabic input click failed, trying label:", e)
                driver.execute_script("arguments[0].click();", label)
                found_arabic = True
                break

    if not found_arabic:
        print("❌ Arabic option not found in language selection.")

    save_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@role='button' and contains(@class, 'submit-btn')]")))
    save_button.click()
    print("✅ Language saved as Arabic.")
    time.sleep(3)

except Exception as e:
    print("⚠️ Language selection failed or skipped:", str(e))

# Navigate back to the original search URL
driver.get(url)
time.sleep(5)

# Load initial products
try:
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'product-list')))
    print("🛒 Initial products loaded.")
except:
    print("❌ Product list not found. Trying scroll fallback.")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)

# Click Discover More
try:
    discover_more_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "title-right")))
    print("➡️ Clicking on 'Discover More' button...")
    discover_more_btn.click()
    time.sleep(5)
except Exception as e:
    print("⚠️ 'Discover More' button not found or not clickable:", e)

# Scroll to load all products
scroll_to_bottom_until_loaded(driver, wait_time=3)

product_divs = driver.find_elements(By.CLASS_NAME, 'product')
print(f"📦 Total products loaded: {len(product_divs)}")

data = []

for idx, product in enumerate(product_divs, 1):
    try:
        name = product.find_element(By.CLASS_NAME, 'product-name').text
        price = product.find_element(By.CLASS_NAME, 'p-sale-price-wrapper').text
        product_link = product.find_element(By.TAG_NAME, 'a').get_attribute('href')
        image_url = product.find_element(By.TAG_NAME, 'img').get_attribute('src')

        # Open detail tab
        driver.execute_script("window.open(arguments[0]);", product_link)
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(3)

        # Collect product details
        title = "N/A"
        try:
            title = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".product-feature .title"))).text
        except:
            pass

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

        shipping_section = "N/A"
        try:
            shipping_section = driver.find_element(By.CLASS_NAME, "free-shipping-and-delevry-data").text
        except:
            pass

        shipped_from = "N/A"
        try:
            shipped_from = driver.find_element(By.CSS_SELECTOR, ".shipped-from-info .shipped-from-country .country-name").text
        except:
            pass

        # Append the data
        data.append({
            "name": name,
            "price": price,
            "old_price": old_price,
            "rating": rating,
            "title": title,
            "bullet_items": bullet_items,
            "image_url": image_url,
            "product_link": product_link,
            "shipping_delivery": shipping_section,
            "shipped_from": shipped_from
        })

        print(f"{idx}. ✅ Scraped: {name}")

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(1)

    except Exception as e:
        print(f"{idx}. ❌ Failed to extract product: {e}")
        if len(driver.window_handles) > 1:
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        continue

# Save output
df = pd.DataFrame(data)
df.to_csv("cosmetics.csv", index=False, encoding='utf-8-sig')
print("✅ All data saved to 'cosmetics.csv'")

driver.quit()
