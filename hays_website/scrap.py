# import requests
# from bs4 import BeautifulSoup
# from datetime import datetime, timedelta

# # Get yesterday's date in required format
# yesterday = (datetime.now() - timedelta(days=1)).strftime("%d.%m.%y")

# headers = {"User-Agent": "Mozilla/5.0"}

# # Base URLs for both categories
# urls = {
#     "IT Jobs": "https://www.hays.de/en/jobsearch/job-offers/s/IT/1/c/Germany/D1641BCE-D56C-11D3-AFB2-00105AB00B48/p/{page}?q=&e=false&pt=false",
#     "Finance Jobs": "https://www.hays.de/en/jobsearch/job-offers/s/Finance/3/c/Germany/D1641BCE-D56C-11D3-AFB2-00105AB00B48/p/{page}?q=&e=false&pt=false"
# }

# total_jobs = 0
# found_any = False

# for category, base_url in urls.items():
#     print(f"\n🔍 Scanning {category}...\n")
#     page = 1
#     job_count = 0

#     while True:
#         url = base_url.format(page=page)
#         response = requests.get(url, headers=headers)
#         soup = BeautifulSoup(response.content, "html.parser")

#         jobs = soup.find_all("div", class_="search__result")
#         if not jobs:
#             break

#         for job in jobs:
#             # Posted date
#             posted_text = "N/A"
#             for div in job.find_all("div", class_="row"):
#                 if "Online since:" in div.text:
#                     posted_text = div.text.strip().replace("Online since:", "").strip()
#                     break

#             if posted_text != yesterday:
#                 continue

#             found_any = True

#             # Title
#             title_tag = job.find("h4", class_="search__result__header__title")
#             title = title_tag.get_text(strip=True) if title_tag else "N/A"

#             # Link
#             link_tag = job.find("a", class_="search__result__link")
#             link = link_tag['href'] if link_tag and 'href' in link_tag.attrs else "N/A"

#             # Company
#             company_tag = job.find("div", class_="search__result__job__attribute__type")
#             company = company_tag.find("div", class_="info-text").get_text(strip=True) if company_tag else "N/A"

#             # Location
#             location_tag = job.find("div", class_="search__result__job__attribute__location")
#             location = location_tag.find("div", class_="info-text").get_text(strip=True) if location_tag else "N/A"

#             # Bullet points
#             bullets = job.select("div.h-text ul li")
#             bullet_points = [li.get_text(strip=True) for li in bullets]

#             # Print
#             print("=" * 80)
#             print(f"Title     : {title}")
#             print(f"Company   : {company}")
#             print(f"Location  : {location}")
#             print(f"Posted on : {posted_text}")
#             print("Details   :")
#             for b in bullet_points:
#                 print(f"  - {b}")
#             print(f"Link      : {link}")
#             print("=" * 80 + "\n")

#             job_count += 1

#         page += 1

#     if job_count == 0:
#         print(f"❌ No new job postings in {category} for {yesterday}.")
#     else:
#         print(f"✅ Done. {job_count} new jobs found in {category}.\n")
#         total_jobs += job_count

# # Final message
# if not found_any:
#     print("📭 No new job postings for yesterday in both categories.")
# else:
#     print(f"🎉 Total {total_jobs} new job(s) posted on {yesterday}.")




# import requests
# from bs4 import BeautifulSoup
# from datetime import datetime, timedelta

# category = "IT Jobs"
# base_url = (
#     "https://www.hays.de/en/jobsearch/job-offers/"
#     "s/IT/1/c/Germany/D1641BCE-D56C-11D3-AFB2-00105AB00B48/p/{page}?q=&e=false&pt=false"
# )

# yesterday = (datetime.now() - timedelta(days=1)).date()
# headers = {"User-Agent": "Mozilla/5.0"}

# found = False
# count = 0
# page = 1

# print(f"🔍 Scanning {category} for postings from {yesterday}...\n")

# while True:
#     url = base_url.format(page=page)
#     resp = requests.get(url, headers=headers)
#     soup = BeautifulSoup(resp.content, "html.parser")
#     jobs = soup.find_all("div", class_="search__result")
#     if not jobs:
#         break

#     for job in jobs:
#         div = next((d for d in job.select("div.row") if "Online since:" in d.text), None)
#         if not div:
#             continue

#         raw = div.text.replace("Online since:", "").strip()

#         posted_date = None
#         # Handle "dd.MM.yy" format like "17.06.25"
#         try:
#             posted_date = datetime.strptime(raw, "%d.%m.%y").date()
#         except ValueError:
#             # Fallback to full timestamps
#             for fmt in ("%a %b %d %H:%M:%S %Z %Y", "%a %b %d %H:%M:%S %Y"):
#                 try:
#                     posted_date = datetime.strptime(raw, fmt).date()
#                     break
#                 except ValueError:
#                     continue

        
        
#         if not posted_date or posted_date != yesterday:
#             continue

#         found = True
#         count += 1

#         title = job.find("h4", class_="search__result__header__title")
#         title = title.get_text(strip=True) if title else "N/A"
#         link = job.find("a", class_="search__result__link")
#         link = link["href"] if link and link.get("href") else "N/A"
#         comp_blk = job.find("div", class_="search__result__job__attribute__type")
#         company = comp_blk.find("div", class_="info-text").get_text(strip=True) if comp_blk else "N/A"
#         loc_blk = job.find("div", class_="search__result__job__attribute__location")
#         location = loc_blk.find("div", class_="info-text").get_text(strip=True) if loc_blk else "N/A"
#         bullets = [li.get_text(strip=True) for li in job.select("div.h-text ul li")]

#         print("=" * 80)
#         print(f"Title     : {title}")
#         print(f"Company   : {company}")
#         print(f"Location  : {location}")
#         print(f"Posted on : {posted_date}")
#         if bullets:
#             print("Details   :")
#             for b in bullets:
#                 print(f"  - {b}")
#         print(f"Link      : {link}")
#         print("=" * 80 + "\n")

#     page += 1

# if not found:
#     print(f"❌ No new IT job postings on {yesterday}.")
# else:
#     print(f"✅ Done. {count} new IT job(s) found on {yesterday}.")


# import requests
# from bs4 import BeautifulSoup
# from datetime import datetime, timedelta

# # Get yesterday's date in required format
# yesterday = (datetime.now() - timedelta(days=1)).strftime("%d.%m.%y")

# headers = {"User-Agent": "Mozilla/5.0"}

# # Base URLs for both categories
# urls = {
#     "IT Jobs": "https://www.hays.de/en/jobsearch/job-offers/s/IT/1/c/Germany/D1641BCE-D56C-11D3-AFB2-00105AB00B48/p/{page}?q=&e=false&pt=false",
#     "Finance Jobs": "https://www.hays.de/en/jobsearch/job-offers/s/Finance/3/c/Germany/D1641BCE-D56C-11D3-AFB2-00105AB00B48/p/{page}?q=&e=false&pt=false"
# }

# total_jobs = 0
# found_any = False

# for category, base_url in urls.items():
#     print(f"\n🔍 Scanning {category}...\n")
#     page = 1
#     job_count = 0

#     while True:
#         url = base_url.format(page=page)
#         response = requests.get(url, headers=headers)
#         soup = BeautifulSoup(response.content, "html.parser")

#         jobs = soup.find_all("div", class_="search__result")
#         if not jobs:
#             break

#         for job in jobs:
#             # Posted date
#             posted_text = "N/A"
#             for div in job.find_all("div", class_="row"):
#                 if "Online since:" in div.text:
#                     posted_text = div.text.strip().replace("Online since:", "").strip()
#                     break

#             if posted_text != yesterday:
#                 continue

#             found_any = True

#             # Title
#             title_tag = job.find("h4", class_="search__result__header__title")
#             title = title_tag.get_text(strip=True) if title_tag else "N/A"

#             # Link
#             link_tag = job.find("a", class_="search__result__link")
#             link = link_tag['href'] if link_tag and 'href' in link_tag.attrs else "N/A"

#             # Company
#             company_tag = job.find("div", class_="search__result__job__attribute__type")
#             company = company_tag.find("div", class_="info-text").get_text(strip=True) if company_tag else "N/A"

#             # Location
#             location_tag = job.find("div", class_="search__result__job__attribute__location")
#             location = location_tag.find("div", class_="info-text").get_text(strip=True) if location_tag else "N/A"

#             # Bullet points
#             bullets = job.select("div.h-text ul li")
#             bullet_points = [li.get_text(strip=True) for li in bullets]

#             # Print
#             print("=" * 80)
#             print(f"Title     : {title}")
#             print(f"Company   : {company}")
#             print(f"Location  : {location}")
#             print(f"Posted on : {posted_text}")
#             print("Details   :")
#             for b in bullet_points:
#                 print(f"  - {b}")
#             print(f"Link      : {link}")
#             print("=" * 80 + "\n")

#             job_count += 1

#         page += 1

#     if job_count == 0:
#         print(f"❌ No new job postings in {category} for {yesterday}.")
#     else:
#         print(f"✅ Done. {job_count} new jobs found in {category}.\n")
#         total_jobs += job_count

# # Final message
# if not found_any:
#     print("📭 No new job postings for yesterday in both categories.")
# else:
#     print(f"🎉 Total {total_jobs} new job(s) posted on {yesterday}.")

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////




# import requests
# from bs4 import BeautifulSoup
# from datetime import datetime, timedelta
# import re

# # Get yesterday's date in required format (e.g., "17.06.25")
# yesterday = (datetime.now() - timedelta(days=1)).strftime("%d.%m.%y")

# headers = {"User-Agent": "Mozilla/5.0"}

# # Updated URLs with industry filters
# urls = {
#     "IT Jobs": "https://www.hays.de/en/jobsearch/job-offers/s/IT/1/c/Germany/D1641BCE-D56C-11D3-AFB2-00105AB00B48/i/Software-DP-IT-services/D2361F07-89E8-DE11-BAE0-0007E92E2CEA/p/{page}?q=&e=false&pt=false",
#     "Finance Jobs": "https://www.hays.de/en/jobsearch/job-offers/s/Finance/3/c/Germany/D1641BCE-D56C-11D3-AFB2-00105AB00B48/i/Banks-saving-banks-financial-service-providers/6E7A1D11-89E8-DE11-BAE0-0007E92E2CEA/p/{page}?q=&e=false&pt=false"
# }

# total_jobs = 0
# found_any = False

# for category, base_url in urls.items():
#     print(f"\n🔍 Scanning {category}...\n")
#     page = 1
#     job_count = 0

#     while True:
#         url = base_url.format(page=page)
#         response = requests.get(url, headers=headers)
#         soup = BeautifulSoup(response.content, "html.parser")

#         jobs = soup.find_all("div", class_="search__result")
#         if not jobs:
#             break

#         for job in jobs:
#             # Extract 'Online since' date
#             posted_text = "N/A"
#             for div in job.find_all("div", class_="row"):
#                 text = div.get_text(strip=True)
#                 match = re.search(r"online since[:\s]*(\d{2}\.\d{2}\.\d{2})", text.lower())
#                 if match:
#                     posted_text = match.group(1)
#                     break

#             # Debug print to check if date is being captured
#             # print(f"📅 Found job posted on: {posted_text}")

#             if posted_text != yesterday:
#                 continue

#             found_any = True

#             # Job title
#             title_tag = job.find("h4", class_="search__result__header__title")
#             title = title_tag.get_text(strip=True) if title_tag else "N/A"

#             # Link
#             link_tag = job.find("a", class_="search__result__link")
#             link = link_tag['href'] if link_tag and 'href' in link_tag.attrs else "N/A"

#             # Company
#             company_tag = job.find("div", class_="search__result__job__attribute__type")
#             company = company_tag.find("div", class_="info-text").get_text(strip=True) if company_tag else "N/A"

#             # Location
#             location_tag = job.find("div", class_="search__result__job__attribute__location")
#             location = location_tag.find("div", class_="info-text").get_text(strip=True) if location_tag else "N/A"

#             # Bullet points
#             bullets = job.select("div.h-text ul li")
#             bullet_points = [li.get_text(strip=True) for li in bullets]

#             # Print result
#             print("=" * 80)
#             print(f"Title     : {title}")
#             print(f"Company   : {company}")
#             print(f"Location  : {location}")
#             print(f"Posted on : {posted_text}")
#             print("Details   :")
#             for b in bullet_points:
#                 print(f"  - {b}")
#             print(f"Link      : {link}")
#             print("=" * 80 + "\n")

#             job_count += 1

#         page += 1

#     if job_count == 0:
#         print(f"❌ No new job postings in {category} for {yesterday}.")
#     else:
#         print(f"✅ Done. {job_count} new jobs found in {category}.\n")
#         total_jobs += job_count

# # Final summary
# if not found_any:
#     print("📭 No new job postings for yesterday in both categories.")
# else:
#     print(f"🎉 Total {total_jobs} new job(s) posted on {yesterday}.")


# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# import requests
# from bs4 import BeautifulSoup

# headers = {"User-Agent": "Mozilla/5.0"}

# url = "https://www.hays.de/en/jobsearch/job-offers/s/IT/1/c/Germany/D1641BCE-D56C-11D3-AFB2-00105AB00B48/i/Software-DP-IT-services/D2361F07-89E8-DE11-BAE0-0007E92E2CEA/p/1?q=&e=false&pt=false"

# response = requests.get(url, headers=headers)

# print(f"✅ Status Code: {response.status_code}\n")

# if response.ok:
#     soup = BeautifulSoup(response.content, "html.parser")
#     job_cards = soup.find_all("div", class_="search__result")

#     if not job_cards:
#         print("⚠️ No job cards found. Site may be using JavaScript or cookie wall.")
#     else:
#         print(f"🔍 Found {len(job_cards)} job(s) on page 1.")
#         print("\n📌 Job Titles Preview:\n")

#         for i, job in enumerate(job_cards[:5], 1):  # Show first 5 jobs
#             title_tag = job.find("h4", class_="search__result__header__title")
#             title = title_tag.get_text(strip=True) if title_tag else "N/A"
#             print(f"{i}. {title}")
# else:
#     print("❌ Failed to load page. Possible block or network issue.")
    
    
    #//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    
    








# import requests
# from bs4 import BeautifulSoup

# headers = {"User-Agent": "Mozilla/5.0"}

# url = "https://www.hays.de/en/jobsearch/job-offers/s/IT/1/c/Germany/D1641BCE-D56C-11D3-AFB2-00105AB00B48/i/Software-DP-IT-services/D2361F07-89E8-DE11-BAE0-0007E92E2CEA/p/1?q=&e=false&pt=false"

# response = requests.get(url, headers=headers)
# soup = BeautifulSoup(response.content, "html.parser")
# job_cards = soup.find_all("div", class_="search__result")

# for job in job_cards:
#     # Title
#     title_tag = job.find("h4", class_="search__result__header__title")
#     title = title_tag.get_text(strip=True) if title_tag else "N/A"

#     # Link
#     link_tag = job.find("a", class_="search__result__link")
#     link = "https://www.hays.de" + link_tag['href'] if link_tag and 'href' in link_tag.attrs else "N/A"

#     # Company
#     company_tag = job.find("div", class_="search__result__job__attribute__type")
#     company = company_tag.find("div", class_="info-text").get_text(strip=True) if company_tag else "N/A"

#     # Location
#     location_tag = job.find("div", class_="search__result__job__attribute__location")
#     location = location_tag.find("div", class_="info-text").get_text(strip=True) if location_tag else "N/A"

#     # Posted Date
#     posted_date = "N/A"
#     for div in job.find_all("div", class_="row"):
#         if "Online since:" in div.text:
#             posted_date = div.text.strip().replace("Online since:", "").strip()
#             break

#     # Bullet points
#     bullets = job.select("div.h-text ul li")
#     bullet_points = [li.get_text(strip=True) for li in bullets]

#     # Print formatted job info
#     print("=" * 80)
#     print(f"Title     : {title}")
#     print(f"Company   : {company}")
#     print(f"Location  : {location}")
#     print(f"Posted on : {posted_date}")
#     print("Details   :")
#     for b in bullet_points:
#         print(f"  - {b}")
#     print(f"Link      : {link}")
#     print("=" * 80)
#     print()




# import requests
# from bs4 import BeautifulSoup
# from datetime import datetime, timedelta
# import re

# # Optional: filter for yesterday's date (e.g., "17.06.25")
# yesterday = (datetime.now() - timedelta(days=1)).strftime("%d.%m.%y")

# headers = {"User-Agent": "Mozilla/5.0"}

# urls = {
#     "IT Jobs": "https://www.hays.de/en/jobsearch/job-offers/s/IT/1/"
#                "c/Germany/D1641BCE-D56C-11D3-AFB2-00105AB00B48/"
#                "i/Software-DP-IT-services/"
#                "D2361F07-89E8-DE11-BAE0-0007E92E2CEA/p/{page}?q=&e=false&pt=false",
#     "Finance Jobs": "https://www.hays.de/en/jobsearch/job-offers/s/Finance/3/"
#                     "c/Germany/D1641BCE-D56C-11D3-AFB2-00105AB00B48/"
#                     "i/Banks-saving-banks-financial-service-providers/"
#                     "6E7A1D11-89E8-DE11-BAE0-0007E92E2CEA/p/{page}?q=&e=false&pt=false"
# }

# total_jobs = 0

# for category, base_url in urls.items():
#     print(f"\n🔍 Scanning {category}...\n")
#     page = 1
#     job_count = 0

#     while True:
#         url = base_url.format(page=page)
#         resp = requests.get(url, headers=headers)
#         if not resp.ok:
#             print(f"❌ Failed to fetch page {page} — status {resp.status_code}")
#             break

#         soup = BeautifulSoup(resp.content, "html.parser")
#         jobs = soup.find_all("div", class_="search__result")

#         if not jobs:
#             break

#         for job in jobs:
#             # Extract only visible "Online since" date
#             div = job.find("div", class_="row", text=re.compile(r"Online since:"))
#             posted_on = "N/A"
#             if div:
#                 # Extract direct visible text only
#                 posted_on = re.sub(r"^Online since:\s*", "", div.get_text(strip=True))

#             # Optional filter by yesterday:
#             # if posted_on != yesterday:
#             #     continue

#             # Title
#             t = job.find("h4", class_="search__result__header__title")
#             title = t.get_text(strip=True) if t else "N/A"

#             # Link
#             a = job.find("a", class_="search__result__link")
#             link = a["href"] if (a and a.has_attr("href")) else "N/A"
#             if link != "N/A" and not link.startswith("http"):
#                 link = "https://www.hays.de" + link

#             # Company
#             ctag = job.find("div", class_="search__result__job__attribute__type")
#             company = ctag.find("div", class_="info-text").get_text(strip=True) if ctag else "N/A"

#             # Location
#             ltag = job.find("div", class_="search__result__job__attribute__location")
#             location = ltag.find("div", class_="info-text").get_text(strip=True) if ltag else "N/A"

#             # Bullet points
#             bullets = job.select("div.h-text ul li")
#             bpts = [li.get_text(strip=True) for li in bullets]

#             # Print in desired format
#             print("=" * 80)
#             print(f"Title     : {title}")
#             print(f"Company   : {company}")
#             print(f"Location  : {location}")
#             print(f"Posted on : {posted_on}")
#             print("Details   :")
#             for b in bpts:
#                 print(f"  - {b}")
#             print(f"Link      : {link}")
#             print("=" * 80 + "\n")

#             job_count += 1

#         page += 1

#     summary = f"✅ Done. {job_count} job(s) found in {category}." if job_count else f"❌ No job postings found in {category}."
#     print(summary)
#     total_jobs += job_count

# print(f"\n🎉 Total {total_jobs} job(s) extracted.\n")






















import requests
from bs4 import BeautifulSoup
import re

# User-Agent header to mimic a browser
headers = {"User-Agent": "Mozilla/5.0"}

# URLs templates for Finance and IT pages
urls = {
    "Finance": (
        "https://www.hays.de/en/jobsearch/job-offers/"
        "s/Finance/3/c/Germany/D1641BCE-D56C-11D3-AFB2-00105AB00B48/"
        "i/Banks-saving-banks-financial-service-providers/"
        "6E7A1D11-89E8-DE11-BAE0-0007E92E2CEA/p/{page}?q=&e=false&pt=false"
    ),
    "IT": (
        "https://www.hays.de/en/jobsearch/job-offers/"
        "s/IT/1/c/Germany/D1641BCE-D56C-11D3-AFB2-00105AB00B48/"
        "i/Software-DP-IT-services/"
        "D2361F07-89E8-DE11-BAE0-0007E92E2CEA/p/{page}?q=&e=false&pt=false"
    )
}

for job_type in ["Finance", "IT"]:
    print(f"\n📰 {job_type} related jobs:\n")
    page = 1

    while True:
        url = urls[job_type].format(page=page)
        resp = requests.get(url, headers=headers)
        if not resp.ok:
            print(f"❌ Failed to load {job_type} page {page} (status {resp.status_code})")
            break

        soup = BeautifulSoup(resp.content, "html.parser")
        cards = soup.find_all("div", class_="search__result")
        if not cards:
            if page == 1:
                print(f"⚠️ No {job_type} jobs found on first page.")
            break

        for job in cards:
            # Extract visible "Online since" date
            div = job.find("div", class_="row", text=re.compile(r"Online since:"))
            posted_on = div.get_text(strip=True).replace("Online since:", "").strip() if div else "N/A"

            # Title
            t = job.find("h4", class_="search__result__header__title")
            title = t.get_text(strip=True) if t else "N/A"

            # Link (ensure full URL)
            a = job.find("a", class_="search__result__link")
            link = a["href"] if (a and a.has_attr("href")) else ""
            if link and not link.startswith("http"):
                link = "https://www.hays.de" + link

            # Company and location
            ct = job.find("div", class_="search__result__job__attribute__type")
            company = ct.find("div", class_="info-text").get_text(strip=True) if ct else "N/A"
            lt = job.find("div", class_="search__result__job__attribute__location")
            location = lt.find("div", class_="info-text").get_text(strip=True) if lt else "N/A"

            # Bullet-point details
            bullets = job.select("div.h-text ul li")
            details = [b.get_text(strip=True) for b in bullets]

            # Print in requested format
            print("=" * 80)
            print(f"Type      : {job_type}")
            print(f"Title     : {title}")
            print(f"Company   : {company}")
            print(f"Location  : {location}")
            print(f"Posted on : {posted_on}")
            print("Details   :")
            for d in details:
                print(f"  - {d}")
            print(f"Link      : {link}")
            print("=" * 80 + "\n")

        page += 1
