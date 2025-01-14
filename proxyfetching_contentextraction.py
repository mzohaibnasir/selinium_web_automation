# import cloudscraper
# import time
# from bs4 import BeautifulSoup
# import random
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options

# # Setup Chrome options
# chrome_options = Options()
# chrome_options.add_argument("--headless")  # Run in headless mode
# chrome_options.add_argument("--disable-gpu")

# # Path to your WebDriver
# webdriver_path = "/path/to/chromedriver"  # Replace with your WebDriver path

# # Initialize WebDriver
# service = Service("")
# driver = webdriver.Chrome(service=service, options=chrome_options)


# def extract_proxies():
#     # Open the website to get the proxy list
#     driver.get("https://free-proxy-list.net/")

#     # Wait for the page to load
#     time.sleep(3)

#     # Locate the proxy table using the provided selector
#     table = driver.find_element(
#         By.CSS_SELECTOR, "#list > div > div.table-responsive > div > table"
#     )

#     # Extract the table rows (excluding the header row)
#     rows = table.find_elements(By.TAG_NAME, "tr")[1:]  # Skip the header row

#     # Parse the data and collect proxies
#     proxies = []
#     for row in rows:
#         cols = row.find_elements(By.TAG_NAME, "td")
#         if len(cols) >= 8:
#             ip = cols[0].text
#             port = cols[1].text
#             https = cols[6].text
#             if https.lower() == "yes":  # Include only HTTPS proxies
#                 proxies.append(f"{ip}:{port}")

#     print(f"Fetched Proxies: \n\n {"\n\t".join(proxies)}")
#     print("-" * 50)

#     return proxies


# def create_advanced_scraper():
#     # Custom headers that make the request look more like a real browser
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
#         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
#         "Accept-Language": "en-US,en;q=0.9",
#         "Accept-Encoding": "gzip, deflate, br",
#         "Referer": "https://www.google.com/",
#         "DNT": "1",
#         "Connection": "keep-alive",
#         "Upgrade-Insecure-Requests": "1",
#         "Sec-Fetch-Dest": "document",
#         "Sec-Fetch-Mode": "navigate",
#         "Sec-Fetch-Site": "none",
#         "Sec-Fetch-User": "?1",
#     }

#     # Create scraper with custom settings
#     scraper = cloudscraper.create_scraper(
#         browser={"browser": "chrome", "platform": "windows", "desktop": True},
#         delay=10,  # Delay for solving challenges
#     )

#     # Update headers
#     scraper.headers.update(headers)

#     return scraper



# def scrape_with_retries(url, proxies, max_retries=3, selector="#root > div > main > div > div.ds-dex-table.ds-dex-table-top"):
#     scraper = create_advanced_scraper()

#     for attempt in range(max_retries):
#         try:
#             print(f"Attempt {attempt + 1} of {max_retries}")
#             proxy = random.choice(proxies)
#             print(f"Using proxy: {proxy}")
            
#             scraper.proxies = {"http": f"http://{proxy}", "https": f"https://{proxy}"}

#             if attempt > 0:
#                 delay = random.uniform(3, 7)
#                 print(f"Waiting {delay:.2f} seconds before retry...")
#                 time.sleep(delay)

#             # Disable SSL verification
#             response = scraper.get(url, verify=False)

#             if response.status_code == 200:
#                 print("Successfully retrieved page")
#                 soup = BeautifulSoup(response.text, "html.parser")
#                 target_element = soup.select_one(selector)

#                 if target_element:
#                     return target_element.text
#                 else:
#                     print("Element not found")
#                     if attempt == max_retries - 1:
#                         with open("debug_page.html", "w", encoding="utf-8") as f:
#                             f.write(response.text)
#                         print("Saved HTML content for inspection")
#             else:
#                 print(f"Request failed with status code: {response.status_code}")

#         except cloudscraper.exceptions.CloudflareChallengeError as e:
#             print(f"Cloudflare challenge error: {str(e)}")
#             if attempt == max_retries - 1:
#                 raise

#         except Exception as e:
#             print(f"Unexpected error: {str(e)}")
#             if attempt == max_retries - 1:
#                 raise

#     return None



# if __name__ == "__main__":
#     try:
#         # Extract proxies using Selenium
#         proxies = extract_proxies()
#         print(f"Found {len(proxies)} proxies.")

#         if proxies:
#             url = "https://dexscreener.com/"
#             result = scrape_with_retries(url, proxies)

#             if result:
#                 print("\nExtracted content:")
#                 print(result)
#             else:
#                 print("\nFailed to extract content after all retries")
#         else:
#             print("No proxies found!")

#     except Exception as e:
#         print(f"\nScript failed with error: {str(e)}")

#     # Close the browser
#     driver.quit()




import cloudscraper
import time
from bs4 import BeautifulSoup
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import urllib3
import ssl

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")

# Initialize WebDriver
service = Service("")  # Add the path to your ChromeDriver if needed
driver = webdriver.Chrome(service=service, options=chrome_options)

def extract_proxies():
    """
    Extract HTTPS-compatible proxies from free-proxy-list.net.
    """
    driver.get("https://free-proxy-list.net/")
    time.sleep(3)  # Wait for the page to load

    # Locate the proxy table
    table = driver.find_element(
        By.CSS_SELECTOR, "#list > div > div.table-responsive > div > table"
    )
    rows = table.find_elements(By.TAG_NAME, "tr")[1:]  # Skip the header row

    proxies = []
    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        if len(cols) >= 8:
            ip = cols[0].text
            port = cols[1].text
            https = cols[6].text
            if https.lower() == "yes":  # Only use HTTPS-compatible proxies
                proxies.append(f"{ip}:{port}")

    print(f"Fetched Proxies: \n\n {'\n\t'.join(proxies)}")
    print("-" * 50)

    return proxies

def create_advanced_scraper():
    """
    Create a CloudScraper instance with custom SSL context and headers.
    """
    # Create SSL context that doesn't verify certificates and uses modern TLS
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    ssl_context.set_ciphers('DEFAULT@SECLEVEL=1')  # Lower security level to allow more ciphers

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.google.com/",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }

    scraper = cloudscraper.create_scraper(
        browser={"browser": "chrome", "platform": "windows", "desktop": True},
        delay=10,
        ssl_context=ssl_context  # Use our custom SSL context
    )

    scraper.headers.update(headers)
    return scraper

def scrape_with_retries(url, proxies, max_retries=15, selector="#root > div > main > div > div.ds-dex-table.ds-dex-table-top"):
    """
    Scrape a URL with retries and proxy rotation.
    """
    scraper = create_advanced_scraper()

    for attempt in range(max_retries):
        try:
            print(f"Attempt {attempt + 1} of {max_retries}")
            proxy = random.choice(proxies)
            print(f"Using proxy: {proxy}")

            proxies_dict = {
                "http": f"http://{proxy}",
                "https": f"https://{proxy}"
            }

            if attempt > 0:
                delay = random.uniform(3, 7)
                print(f"Waiting {delay:.2f} seconds before retry...")
                time.sleep(delay)

            # Use the proxies dictionary and don't verify SSL
            response = scraper.get(url, proxies=proxies_dict, verify=False)

            if response.status_code == 200:
                print("Successfully retrieved page")
                soup = BeautifulSoup(response.text, "html.parser")
                target_element = soup.select_one(selector)

                if target_element:
                    return target_element.text
                else:
                    print("Element not found")
                    if attempt == max_retries - 1:
                        with open("debug_page.html", "w", encoding="utf-8") as f:
                            f.write(response.text)
                        print("Saved HTML content for inspection")
            else:
                print(f"Request failed with status code: {response.status_code}")

        except cloudscraper.exceptions.CloudflareChallengeError as e:
            print(f"Cloudflare challenge error: {str(e)}")
            if attempt == max_retries - 1:
                raise
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            if attempt == max_retries - 1:
                raise

    return None

if __name__ == "__main__":
    try:
        # Extract proxies
        proxies = extract_proxies()
        print(f"Found {len(proxies)} proxies.")

        if proxies:
            url = "https://dexscreener.com/"
            result = scrape_with_retries(url, proxies)

            if result:
                print("\nExtracted content:")
                print(result)
            else:
                print("\nFailed to extract content after all retries")
        else:
            print("No proxies found!")

    except Exception as e:
        print(f"\nScript failed with error: {str(e)}")
    finally:
        # Clean up the WebDriver
        driver.quit()