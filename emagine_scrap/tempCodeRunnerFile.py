





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