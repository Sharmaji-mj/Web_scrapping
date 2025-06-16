# from selenium import webdriver
# import pandas as pd
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# import time
# import datetime
# import os
# from tabulate import tabulate

# # Get today's date and yesterday's date
# t_day = datetime.datetime.now()
# yesterday = (t_day - datetime.timedelta(days=1)).date()

# # Set up Selenium driver for Linux headless
# chrome_options = Options()
# chrome_options.add_argument("--headless")  # headless mode for Linux
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--window-size=1920,1080")

# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# yr = t_day.strftime("%Y")
# mt = t_day.strftime("%m")

# # Open the URL
# driver.get(f"https://ted.europa.eu/en/search/result?search-scope=ACTIVE&scope=ACTIVE&onlyLatestVersions=false&facet.cpv=comp%2C72000000&facet.contract-nature=services&facet.place-of-performance=SPCY%2CDEU&facet.publication-date={yr}%2C{mt}&sortColumn=publication-number&sortOrder=DESC&page=1")

# time.sleep(10)

# # Extract rows
# rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")

# # Prepare data
# data = []
# for row in rows:
#     cols = row.find_elements(By.TAG_NAME, "td")
#     if cols and len(cols) >= 5:
#         notice_elem = cols[1].find_element(By.TAG_NAME, "a")
#         notice_number = notice_elem.text.strip()
#         notice_link = notice_elem.get_attribute("href")
#         description = cols[2].text.strip()
#         country = cols[3].text.strip()
#         publication_date_str = cols[4].text.strip()
#         try:
#             deadline = cols[5].text.strip()
#         except IndexError:
#             deadline = ""

#         # Convert publication date string to datetime
#         publication_date = datetime.datetime.strptime(publication_date_str, "%d/%m/%Y").date()

#         # Filter at row level
#         if publication_date == yesterday:
#             data.append({
#                 "Notice Number": notice_number,
#                 "Link": notice_link,
#                 "Description": description,
#                 "Country": country,
#                 "Publication Date": publication_date_str,
#                 "Deadline": deadline
#             })

# # Quit Selenium
# driver.quit()

# df = pd.DataFrame(data)


# # See all columns
# pd.set_option('display.max_columns', None)

# # See wide rows
# pd.set_option('display.width', None)

# # See all text in each column
# pd.set_option('display.max_colwidth', None)

# print(tabulate(df, headers='keys', tablefmt='grid', showindex=False))
# # print(df) 


# # print(df.iloc[16])

# # # Create folder if not exist
# # os.makedirs("tender_records", exist_ok=True)



# # # Append to master Excel history file
# # history_file = "tender_records/tender_history.xlsx"

# # if not os.path.isfile(history_file):
# #     # If history file not exists → create new Excel file
# #     df.to_excel(history_file, index=False, engine='openpyxl')
# # else:
# #     # Read existing file
# #     history_df = pd.read_excel(history_file, engine='openpyxl')
    
# #     # Avoid duplicates
# #     merged_df = pd.merge(df, history_df, on=["Notice Number", "Publication Date"], how='left', indicator=True)
# #     new_rows = merged_df[merged_df['_merge'] == 'left_only'].drop(columns=['_merge'])
    
# #     if not new_rows.empty:
# #         # Append new rows
# #         updated_df = pd.concat([history_df, new_rows], ignore_index=True)
# #         updated_df.to_excel(history_file, index=False, engine='openpyxl')
# #         print(f"{new_rows.shape[0]} new rows appended to history.")
# #     else:
# #         print("No new records to append. History file already up-to-date.")

# # # Prepare HTML file for email sending
# # df.to_html("tender_records/tender_email.html", index=False, encoding='utf-8')



# # print("df columns:", df.columns.tolist())
# # print("history_df columns:", history_df.columns.tolist())





















# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////

from selenium import webdriver
import pandas as pd
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import datetime
import os

# Get today's and yesterday's date
t_day = datetime.datetime.now()
yesterday = (t_day - datetime.timedelta(days=1)).date()

# Set up Selenium headless for Linux
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Date for filtering
yr = t_day.strftime("%Y")
mt = t_day.strftime("%m")

# Open TED search results
driver.get(f"https://ted.europa.eu/en/search/result?search-scope=ACTIVE&scope=ACTIVE&onlyLatestVersions=false&facet.cpv=comp%2C72000000&facet.contract-nature=services&facet.place-of-performance=SPCY%2CDEU&facet.publication-date={yr}%2C{mt}&sortColumn=publication-number&sortOrder=DESC&page=1")
time.sleep(10)

# Extract rows
rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
data = []

for row in rows:
    cols = row.find_elements(By.TAG_NAME, "td")
    if cols and len(cols) >= 5:
        notice_elem = cols[1].find_element(By.TAG_NAME, "a")
        notice_number = notice_elem.text.strip()
        notice_link = notice_elem.get_attribute("href")
        description = cols[2].text.strip()
        country = cols[3].text.strip()
        publication_date_str = cols[4].text.strip()
        try:
            deadline = cols[5].text.strip()
        except IndexError:
            deadline = ""

        # Convert and compare publication date
        publication_date = datetime.datetime.strptime(publication_date_str, "%d/%m/%Y").date()

        if publication_date == yesterday:
            data.append({
                "Notice Number": notice_number,
                "Link": notice_link,
                "Description": description,
                "Country": country,
                "Publication Date": publication_date_str,
                "Deadline": deadline
            })

# Close browser
driver.quit()

# Create DataFrame
df = pd.DataFrame(data)

# Custom clean print
for index, row in df.iterrows():
    print("=" * 100)
    print(f"Notice Number   : {row['Notice Number']}")
    print(f"Link            : {row['Link']}")
    print(f"Description     : {row['Description']}")
    print(f"Country         : {row['Country']}")
    print(f"Publication Date: {row['Publication Date']}")
    print(f"Deadline        : {row['Deadline']}")
    print("=" * 100)
    print("\n")



# Create folder if not exist
os.makedirs("tender_records", exist_ok=True)



# Append to master Excel history file
history_file = "tender_records/tender_history.xlsx"

if not os.path.isfile(history_file):
    # If history file not exists → create new Excel file
    df.to_excel(history_file, index=False, engine='openpyxl')
else:
    # Read existing file
    history_df = pd.read_excel(history_file, engine='openpyxl')
    
    # Avoid duplicates
    merged_df = pd.merge(df, history_df, on=["Notice Number", "Publication Date"], how='left', indicator=True)
    new_rows = merged_df[merged_df['_merge'] == 'left_only'].drop(columns=['_merge'])
    
    if not new_rows.empty:
        # Append new rows
        updated_df = pd.concat([history_df, new_rows], ignore_index=True)
        updated_df.to_excel(history_file, index=False, engine='openpyxl')
        print(f"{new_rows.shape[0]} new rows appended to history.")
    else:
        print("No new records to append. History file already up-to-date.")

# Prepare HTML file for email sending
df.to_html("tender_records/tender_email.html", index=False, encoding='utf-8')