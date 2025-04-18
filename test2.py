import requests
from bs4 import BeautifulSoup
import pandas as pd

# Define the base URL and page range for web scraping
base_url = "https://www.trendyol.com/cep-telefonu-x-c103498?pi="
start_page = 1
end_page = 117

# Create an empty list to store the scraped data
data = []

# Data Collection
for page_number in range(start_page, end_page + 1):
    url = base_url + str(page_number)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser", from_encoding="utf-8")
    products = soup.find_all("div", attrs={"class": "p-card-wrppr with-campaign-view"})
    
    for product in products:
        # Extract product name and price
        product_name_div = product.find("div", attrs={"class": "prdct-desc-cntnr"})
        product_name = product_name_div.find("span", attrs={"class": "prdct-desc-cntnr-name hasRatings"})
        product_name_clear = product_name_div.text.strip() if product_name_div else None
        product_name_1_clear = product_name.text.strip() if product_name else None
        
        product_price_div = product.find("div", attrs={"class": "prc-box-dscntd"})
        original_price = product_price_div.text.strip() if product_price_div else None
        
        # Extract product link
        product_link_tag = product.find("a", href=True)
        product_link = f"https://www.trendyol.com{product_link_tag['href']}" if product_link_tag else None
        
        # Scrape product details (specifications)
        details_text = []
        if product_link:
            detail_response = requests.get(product_link)
            detail_soup = BeautifulSoup(detail_response.content, "html.parser")
            product_specifications = detail_soup.find_all("ul", class_="detail-attr-container")
            
            for specific in product_specifications:
                details = specific.find_all("li", class_="detail-attr-item")
                for i in details:
                    label = i.find("span").text.strip()
                    value = i.find("b").text.strip()
                    details_text.append(f"{label} = {value}")
        
        # Append product data to the list
        products_data = {
            "Link": product_link,
            "Brand": product_name_clear,
            "Product": product_name_1_clear,
            "Original Price": original_price,
            "Details": details_text
        }
        data.append(products_data)

# Convert dataset to a DataFrame
df = pd.DataFrame(data)
print(df)

# Save the DataFrame to a CSV file
df.to_csv('trendyol_all_data.csv', encoding="utf-8-sig", index=False)