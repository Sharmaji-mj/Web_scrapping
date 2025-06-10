# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager
# import time
# import pandas as pd

# # Launch browser
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
# driver.get("https://ted.europa.eu/en/search/result?search-scope=ACTIVE")
# driver.maximize_window()
# wait = WebDriverWait(driver, 30)

# # Let React load content
# time.sleep(10)

# # Scroll to CPV section (forcefully)
# driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
# time.sleep(2)

# # NEW: Find checkbox span text and click the input instead
# try:
#     checkbox_label = wait.until(EC.presence_of_element_located(
#         (By.XPATH, "//span[contains(text(), 'Computer and Related Services')]/ancestor::label")))
    
#     driver.execute_script("arguments[0].scrollIntoView(true);", checkbox_label)
#     time.sleep(1)
#     checkbox_label.click()
#     print("✅ Checkbox clicked.")
# except Exception as e:
#     print("❌ Could not click checkbox:", e)
#     driver.quit()
#     exit()

# # Wait for results to reload
# time.sleep(6)

# # Scrape table
# rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
# data = []
# for row in rows:
#     cols = row.find_elements(By.TAG_NAME, "td")
#     if cols and len(cols) >= 5:
#         notice_elem = cols[1].find_element(By.TAG_NAME, "a")
#         notice_number = notice_elem.text.strip()
#         notice_link = notice_elem.get_attribute("href")
#         description = cols[2].text.strip()
#         country = cols[3].text.strip()
#         publication_date = cols[4].text.strip()
#         try:
#             deadline = cols[5].text.strip()
#         except IndexError:
#             deadline = ""

#         data.append({
#             "Notice Number": notice_number,
#             "Link": notice_link,
#             "Description": description,
#             "Country": country,
#             "Publication Date": publication_date,
#             "Deadline": deadline
#         })

# driver.quit()

# # Save to CSV
# df = pd.DataFrame(data)
# df.to_csv("filtered_tenders.csv", index=False)
# print("✅ Done. Data saved to filtered_tenders.csv")


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

# Setup
options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get("https://ted.europa.eu/en/search/result?search-scope=ACTIVE")

wait = WebDriverWait(driver, 20)

# Wait for CPV accordion to be present
cpv_filter = wait.until(EC.presence_of_element_located((By.ID, "cpv-accordion")))

# Scroll the accordion into view just in case
driver.execute_script("arguments[0].scrollIntoView();", cpv_filter)
time.sleep(1)

# Wait until the checkbox is present
checkbox_xpath = "//span[contains(text(),'Computer and Related Services')]/preceding::span[@class='CustomReactClasses-MuiButtonBase-root CustomReactClasses-MuiIconButton-root CustomReactClasses-MuiRadio-root CustomReactClasses-MuiRadio-colorPrimary CustomReactClasses-MuiIconButton-colorPrimary'][1]"

checkbox_element = wait.until(EC.presence_of_element_located((By.XPATH, checkbox_xpath)))

# Scroll the checkbox into view and click using JavaScript
driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", checkbox_element)
driver.execute_script("arguments[0].click();", checkbox_element)

print("✅ Checkbox clicked successfully!")

# Pause to verify
time.sleep(5)
driver.quit()
