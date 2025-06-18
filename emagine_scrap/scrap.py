# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from bs4 import BeautifulSoup
# import time
# import requests

# # Set up headless Chrome
# chrome_options = Options()
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--log-level=3")  # Suppress logs

# driver = webdriver.Chrome(options=chrome_options)

# BASE_URL = "https://emagine.de"
# LISTING_URL = f"{BASE_URL}/fuer-consultants/projekte/"

# # Step 1: Load the listing page
# driver.get(LISTING_URL)
# time.sleep(3)  # Let JS load

# soup = BeautifulSoup(driver.page_source, "html.parser")
# driver.quit()

# jobs = []

# # Step 2: Parse job listings
# articles = soup.find_all("article", class_="job-teaser")
# print(f"Total Jobs Found: {len(articles)}\n")

# for article in articles:
#     try:
#         heading_tag = article.select_one("h2.title")
#         heading = heading_tag.get_text(strip=True)
#         link = heading_tag.find_parent("a")["href"]
#         full_link = BASE_URL + link if link.startswith("/") else link

#         location = article.select_one(".address-name").get_text(strip=True)
#         start_date = article.select_one("div:contains('Start')").text.strip().replace("Start", "").strip()
#         duration = article.select_one("div:contains('Duration')").text.strip().replace("Duration", "").strip()
#         unique_id = article.select_one(".job_id").text.strip().lstrip("#")

#         # Step 3: Fetch summary from job detail page
#         resp = requests.get(full_link)
#         detail_soup = BeautifulSoup(resp.text, "html.parser")
#         summary_tag = detail_soup.select_one(".job-offer-description")
#         summary = summary_tag.get_text(strip=True) if summary_tag else "No summary available."

#         # Store result
#         jobs.append({
#             "heading": heading,
#             "link": full_link,
#             "location": location,
#             "start_date": start_date,
#             "duration": duration,
#             "unique_id": unique_id,
#             "summary": summary
#         })

#     except Exception as e:
#         print(f"Error parsing job: {e}")
#         continue

# # Step 4: Print in newsletter format
# for job in jobs:
#     print(f"- **{job['heading']}** (ID: {job['unique_id']})")
#     print(f"  📍 Location: {job['location']}")
#     print(f"  ⏳ Start: {job['start_date']} | Duration: {job['duration']}")
#     print(f"  🔗 Link: {job['link']}")
#     print(f"  📝 Summary: {job['summary']}\n")
#     print("-" * 100)








from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set up Chrome driver
options = Options()
# options.add_argument("--headless")  # Turn OFF headless to see what browser sees
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=Service(), options=options)

# Open the website
url = "https://emagine.de/fuer-consultants/projekte/"
driver.get(url)
driver.maximize_window()

# Wait for job results container
try:
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, "job-result"))
    )
except:
    print("❌ Job result container not found.")
    driver.quit()
    exit()

# Scroll to load all jobs
for _ in range(10):
    driver.execute_script("window.scrollBy(0, 500);")
    time.sleep(1)

# Find job articles
articles = driver.find_elements(By.CSS_SELECTOR, "#job-result article")
print(f"🔍 Total jobs found: {len(articles)}")

# Extract data from each job card
for article in articles:
    try:
        link_tag = article.find_element(By.CSS_SELECTOR, "a.single-job")
        job_link = link_tag.get_attribute("href")

        title = article.find_element(By.CSS_SELECTOR, "h2.title").text.strip()
        location = article.find_element(By.CSS_SELECTOR, ".address-name").text.strip()
        job_id = article.find_element(By.CSS_SELECTOR, ".job_id").text.strip()

        # Start date and duration (optional fields)
        try:
            start_date = article.find_element(By.XPATH, ".//div[contains(text(),'Start')]/following-sibling::div").text.strip()
        except:
            start_date = "Not mentioned"

        try:
            duration = article.find_element(By.XPATH, ".//div[contains(text(),'Duration')]/following-sibling::div").text.strip()
        except:
            duration = "Not mentioned"

        # Open job detail page in new tab
        driver.execute_script("window.open(arguments[0]);", job_link)
        driver.switch_to.window(driver.window_handles[1])

        # Wait for page to load and grab summary
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".project-description"))
            )
            summary = driver.find_element(By.CSS_SELECTOR, ".project-description").text.strip()
        except:
            summary = "Summary not found."

        # Close tab and return
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

        # Print newsletter-style output
        print("="*80)
        print(f"🔹 {title}")
        print(f"📍 Location: {location}")
        print(f"🆔 Job ID: {job_id}")
        print(f"🗓️ Start Date: {start_date}")
        print(f"⏳ Duration: {duration}")
        print(f"🔗 Link: {job_link}")
        print(f"📝 Summary:\n{summary}")
        print("="*80)

    except Exception as e:
        print(f"❌ Error parsing job card: {e}")
        continue

driver.quit()



# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import time

# # Setup Chrome driver
# options = Options()
# # options.add_argument("--headless")  # You can enable this if you want to run headless
# options.add_experimental_option("detach", True)  # Keeps the browser open after script ends

# driver = webdriver.Chrome(service=Service(), options=options)

# # URL to scrape
# url = "https://emagine.de/fuer-consultants/projekte/"
# driver.get(url)
# driver.maximize_window()

# # ✅ Accept German cookie popup ("Alle zulassen")
# try:
#     accept_btn = WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Alle zulassen')]"))
#     )
#     accept_btn.click()
#     print("✅ Cookie popup accepted.")
# except:
#     print("⚠️ No cookie popup found or already accepted.")

# # ✅ Wait for job listings to appear
# try:
#     WebDriverWait(driver, 15).until(
#         EC.presence_of_element_located((By.ID, "job-result"))
#     )
# except:
#     print("❌ Job container not found.")
#     driver.quit()
#     exit()

# # ✅ Scroll to load more jobs (if needed)
# for _ in range(10):
#     driver.execute_script("window.scrollBy(0, 500);")
#     time.sleep(1)

# # ✅ Extract job cards
# articles = driver.find_elements(By.CSS_SELECTOR, "#job-result article")
# print(f"🔍 Total jobs found: {len(articles)}")

# # ✅ Loop through job entries
# for article in articles:
#     try:
#         link_tag = article.find_element(By.CSS_SELECTOR, "a.single-job")
#         job_link = link_tag.get_attribute("href")

#         title = article.find_element(By.CSS_SELECTOR, "h2.title").text.strip()
#         location = article.find_element(By.CSS_SELECTOR, ".address-name").text.strip()
#         job_id = article.find_element(By.CSS_SELECTOR, ".job_id").text.strip()

#         # Optional fields
#         try:
#             start_date = article.find_element(By.XPATH, ".//div[contains(text(),'Start')]/following-sibling::div").text.strip()
#         except:
#             start_date = "Not mentioned"

#         try:
#             duration = article.find_element(By.XPATH, ".//div[contains(text(),'Duration')]/following-sibling::div").text.strip()
#         except:
#             duration = "Not mentioned"

#         # Open job detail in a new tab
#         driver.execute_script("window.open(arguments[0]);", job_link)
#         driver.switch_to.window(driver.window_handles[1])

#         # Wait for summary and extract
#         try:
#             WebDriverWait(driver, 10).until(
#                 EC.presence_of_element_located((By.CSS_SELECTOR, ".project-description"))
#             )
#             summary = driver.find_element(By.CSS_SELECTOR, ".project-description").text.strip()
#         except:
#             summary = "Summary not found."

#         # Close tab and switch back
#         driver.close()
#         driver.switch_to.window(driver.window_handles[0])

#         # 📰 Print in newsletter format
#         print("\n" + "=" * 100)
#         print(f"🔹 {title}")
#         print(f"📍 Location   : {location}")
#         print(f"🆔 Job ID     : {job_id}")
#         print(f"🗓️  Start Date: {start_date}")
#         print(f"⏳ Duration   : {duration}")
#         print(f"🔗 Link       : {job_link}")
#         print(f"📝 Summary    :\n{summary}")
#         print("=" * 100 + "\n")

#     except Exception as e:
#         print(f"❌ Error parsing job card: {e}")
#         continue

# driver.quit()
