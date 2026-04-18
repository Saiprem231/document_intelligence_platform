import os
import sys
import time
import django
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Setup Django environment to allow database access from this standalone script
# Assuming 'core' is the name of your main Django project folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from api.models import Book

def run_scraper():
    print("Starting Selenium Scraper in headless mode...")
    options = webdriver.ChromeOptions()
    options.add_argument('--headless') # Runs browser invisibly
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # We will scrape the standard test site: books.toscrape.com
    driver.get("http://books.toscrape.com/")
    time.sleep(2) # Wait for page to load

    # Grab the links for the first 5 books to test the pipeline
    book_elements = driver.find_elements(By.CSS_SELECTOR, "h3 a")
    book_links = [elem.get_attribute("href") for elem in book_elements][:5]

    for link in book_links:
        driver.get(link)
        time.sleep(1) # Polite delay

        try:
            # Extract Metadata
            title = driver.find_element(By.CSS_SELECTOR, "div.product_main h1").text
            
            # books.toscrape.com does not list authors, so we use a fallback
            author = "Unknown Author" 
            
            # Extract rating (class name contains the rating like 'star-rating Three')
            rating_elem = driver.find_element(By.CSS_SELECTOR, "p.star-rating")
            rating = rating_elem.get_attribute("class").split()[-1] + " Stars"
            
            # Extract description
            try:
                description = driver.find_element(By.CSS_SELECTOR, "#product_description + p").text
            except:
                description = "No description available."

            # Save to MySQL Database via Django ORM
            book, created = Book.objects.update_or_create(
                book_url=link,
                defaults={
                    'title': title,
                    'author': author,
                    'rating': rating,
                    'description': description
                }
            )
            
            if created:
                print(f"Added new book: {title}")
            else:
                print(f"Updated existing book: {title}")

        except Exception as e:
            print(f"Error scraping {link}: {e}")

    driver.quit()
    print("Data collection completed successfully!")

if __name__ == "__main__":
    run_scraper()