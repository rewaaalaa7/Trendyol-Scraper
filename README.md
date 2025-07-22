# Trendyol Web Scraper & Automation Bot

A Selenium-based Python project that scrapes product information from multiple categories on [Trendyol](https://www.trendyol.com) and automates adding items to the cart. The project covers:

- Female Fashion
- Male Fashion
- Kids Fashion
- Cosmetics

Additionally, it includes an **automation script** to simulate adding a product to the cart via the UI.

---

## Project Structure

```
trendyol/
├── add-to-cart.py               # Automates adding an item to the cart
├── one-item.py                  # Test script for scraping a single product
├── test-cosmetics.py           # Scraper for cosmetics category
├── test-fashion-female.py      # Scraper for female fashion category
├── test-fashion-kids.py        # Scraper for kids fashion category
├── test-fashion-male.py        # Scraper for male fashion category
├── outputs/                     # Folder for scraped CSV outputs
│   ├── fashion_female.csv
│   ├── fashion_male.csv
│   ├── fashion_kids.csv
│   └── cosmetics.csv
├── README.md                    
```

---

## Features

- Scrapes product name, old price, price, image URL, product URL, product details and rating
- Saves outputs into structured `.csv` files
- Automates web interaction to add an item to cart
- Headless browser support (optional)
- Easy-to-edit category selectors

---

## Requirements

Install required Python libraries:

```bash
pip install selenium pandas
```

You'll also need to download [ChromeDriver](https://sites.google.com/chromium.org/driver/) and ensure it matches your Chrome version.

---

## How to Use

### 1. Run Category Scrapers

Each file targets a different category. Run the one you need:

```bash
python test-fashion-female.py
python test-fashion-male.py
python test-fashion-kids.py
python test-cosmetics.py
```

Scraped data will be saved in `outputs/`.

### 2. Add Product to Cart (Automation)

This script navigates to a product page and simulates adding it to the cart:

```bash
python add-to-cart.py
```

You can modify the product URL inside `add-to-cart.py`.

---

## Sample Output

Each CSV file contains:

![output](https://github.com/rewaaalaa7/Trendyol-Scraper/blob/master/sample-output.jpg)
---

## Notes

- Error handling is included for missing elements and pages with different layouts.
- Customize XPath/CSS selectors if Trendyol updates their layout.
- ChromeDriver path and options can be adjusted as needed.

