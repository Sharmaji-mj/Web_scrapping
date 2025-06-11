from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import datetime
t_day=datetime.datetime.now()
# Set up the driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
yr=t_day.strftime("%Y")
mt=t_day.strftime("%m")
# Open the website
driver.get(f"https://ted.europa.eu/en/search/result?search-scope=ACTIVE&scope=ACTIVE&onlyLatestVersions=false&facet.cpv=comp%2C72000000&facet.contract-nature=services&facet.place-of-performance=SPCY%2CDEU&facet.publication-date={yr}%2C{mt}&sortColumn=publication-number&sortOrder=DESC&page=1")


# print("loading page")
# t_find=WebDriverWait(driver, 30,poll_frequency=.2).until(
#     lambda d: d.find_elements(By.CSS_SELECTOR, "table tbody tr")[0].find_elements(By.TAG_NAME, "td").is_displayed()
# )
time.sleep(10)

# Find all rows in the tender results table
rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")

# Prepare data
data = []
for row in rows:
    cols = row.find_elements(By.TAG_NAME, "td")
    if cols and len(cols) >= 5:
        notice_elem = cols[1].find_element(By.TAG_NAME, "a")
        notice_number = notice_elem.text.strip()
        notice_link = notice_elem.get_attribute("href")
        description = cols[2].text.strip()
        country = cols[3].text.strip()
        publication_date = cols[4].text.strip()
        try:
            deadline = cols[5].text.strip()
        except IndexError:
            deadline = ""

        data.append({
            "Notice Number": notice_number,
            "Link": notice_link,
            "Description": description,
            "Country": country,
            "Publication Date": publication_date,
            "Deadline": deadline
        })
print(data[0])
# Quit driver
driver.quit()

# Convert to DataFrame
df = pd.DataFrame(data)
df['Publication Date']=pd.to_datetime(df["Publication Date"],format="%d/%m/%Y")
df2=df[df["Publication Date"]==(t_day-datetime.timedelta(days=1))]

t_1day=(t_day-datetime.timedelta(days=1)).date()

df2=df[df['Publication Date'].dt.date==t_1day]

if df2.size==0:
    print("no new tenders")
else:
    print(df2.shape[0], "number of tenders present")

df2.to_csv("tender.csv", index=False,encoding='utf-8')



