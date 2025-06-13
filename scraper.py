import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import quote_plus


# This is now a function that takes a search term
def scrape_newegg(search_term):
    """
    Scrapes Newegg.ca based on a dynamic search term.
    Extracts title, price, image URL, and returns a list of dictionaries.
    """
    # Use quote_plus to safely encode the search term for the URL
    # e.g., "rtx 4070 super" -> "rtx+4070+super"
    encoded_search_term = quote_plus(search_term)
    URL = f"https://www.newegg.ca/p/pl?d={encoded_search_term}"

    print(f"Scraping URL: {URL}")  # For debugging

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    }

    try:
        page = requests.get(URL, headers=HEADERS)
        page.raise_for_status()

        soup = BeautifulSoup(page.content, "lxml")
        items = soup.find_all("div", class_="item-container")
        parts_list = []
        part_id_counter = 0

        for item in items:
            title_element = item.find("a", class_="item-title")
            title = title_element.text.strip() if title_element else "Title not found"

            price_element = item.find("li", class_="price-current")
            price_str = "N/A"
            price_float = 0.0
            if price_element and price_element.strong:
                raw_price = price_element.strong.text + price_element.sup.text
                price_str = f"${raw_price}"
                price_float = float(re.sub(r'[^\d.]', '', raw_price))

            image_element = item.find("a", class_="item-img")
            image_url = ""
            if image_element and image_element.img:
                image_url = image_element.img.get('src', '')  # Use .get for safety

            # We need all three pieces of info to consider it a valid product listing
            if title != "Title not found" and price_str != "N/A" and image_url:
                parts_list.append({
                    "id": f"part-{part_id_counter}",
                    "title": title,
                    "price_str": price_str,
                    "price_float": price_float,
                    "imageUrl": image_url
                })
                part_id_counter += 1

        return parts_list

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return []
    except Exception as e:
        print(f"An error occurred during scraping: {e}")
        return []


if __name__ == "__main__":
    # Example of how to use the new function
    test_parts = scrape_newegg("RTX 4070")
    if test_parts:
        for part in test_parts:
            print(part)