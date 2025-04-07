import sys
sys.stdout.reconfigure(encoding='utf-8')  # Forces UTF-8 encoding for printing emojis

import csv
import time
import random
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def normalize_title(title):
    """
    Normalize the title by:
    - Converting to lowercase
    - Removing all non-alphanumeric characters (including spaces and punctuation)
    """
    title = title.lower().strip()
    # Remove punctuation and spaces
    title = re.sub(r'[^a-z0-9]', '', title)
    return title

class IMDbScraper:
    def __init__(self, driver_path):
        self.driver_path = driver_path
        self.movie_data = []
        self.scraped_titles = set()  # This will hold normalized titles

        self.genres = [
            "action", "adventure", "animation", "biography", "comedy", "crime",
            "documentary", "drama", "family", "fantasy", "history", "horror",
            "music", "mystery", "romance", "sci-fi", "sport", "thriller", "war", "western"
        ]

    def setup_webdriver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

        service = Service(self.driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        return driver

    def scrape_movies(self, movies_per_genre=70, max_attempts=3):
        driver = self.setup_webdriver()

        try:
            for genre in self.genres:
                start = 1  
                movies_scraped = 0  
                attempts = 0  # Track the number of attempts

                print(f"\n📌 Scraping movies for genre: {genre.upper()}")

                while movies_scraped < movies_per_genre and attempts < max_attempts:
                    url = f"https://www.imdb.com/search/title/?year=2024&title_type=feature&genres={genre}&start={start}&ref_=adv_nxt"
                    print(f"🔗 Scraping URL: {url}")
                    driver.get(url)

                    try:
                        WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "h3.ipc-title__text"))
                        )
                    except TimeoutException:
                        print(f"⚠️ No more movies found for {genre}. Stopping.")
                        break  

                    title_elements = driver.find_elements(By.CSS_SELECTOR, "h3.ipc-title__text")
                    storyline_elements = driver.find_elements(By.CSS_SELECTOR, ".ipc-html-content-inner-div")

                    if not title_elements:
                        print(f"⚠️ No more movies found for {genre}. Stopping.")
                        break  

                    for i in range(len(title_elements)):
                        raw_title = title_elements[i].text.strip()
                        normalized = normalize_title(raw_title)
                        storyline = (
                            storyline_elements[i].text.strip()
                            if i < len(storyline_elements) and storyline_elements[i].text
                            else "No storyline available."
                        )

                        # Check if normalized title is already scraped
                        if normalized and normalized not in self.scraped_titles:
                            self.movie_data.append({
                                "title": raw_title,  # Preserve original formatting for output
                                "storyline": storyline,
                                "genre": genre
                            })
                            self.scraped_titles.add(normalized)
                            movies_scraped += 1

                        if movies_scraped >= movies_per_genre:
                            break

                    print(f"✅ Total movies scraped for {genre}: {movies_scraped}")

                    if movies_scraped >= movies_per_genre:
                        break  

                    start += 50  
                    attempts += 1  # Increase the number of attempts
                    time.sleep(random.uniform(2, 4))  

        except Exception as e:
            print(f"❌ Scraping error: {e}")

        finally:
            driver.quit()

        return self.movie_data

    def save_to_csv(self, filename="imdb_movies_by_genre.csv"):
        if not self.movie_data:
            print("⚠️ No movie data to save.")
            return

        try:
            with open(filename, "w", newline="", encoding="utf-8") as csvfile:
                fieldnames = ["title", "storyline", "genre"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                writer.writerows(self.movie_data)

            print(f"✅ Movie data saved to {filename}")
            print(f"📌 Total movies scraped: {len(self.movie_data)}")

        except Exception as e:
            print(f"❌ Error saving to CSV: {e}")

def main():
    driver_path = r"C:\Users\Raji\OneDrive\Desktop\chromedriver-win64\chromedriver-win64\chromedriver.exe"
    scraper = IMDbScraper(driver_path)
    scraper.scrape_movies(movies_per_genre=70)
    scraper.save_to_csv("Title_of_CSV")
    main()
