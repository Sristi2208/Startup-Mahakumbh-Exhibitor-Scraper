from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import csv
import string
import time
from bs4 import BeautifulSoup

def scrape_exhibitors_selenium(output_csv="exhibitors_selenium_pagination.csv"):
    base_url = (
        "https://startupmahakumbh.org/exhibitor_directory/"
        "exhi_list_pub.php?event_name=sm&event_year=2025&filter="
    )

    letters = list(string.ascii_uppercase)+["#"]

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Letter",
            "Name of the Organization",
            "Address",
            "Contact Person",
            "Designation",
            "Contact Details",
            "Profile",
            "Page Number"
        ])

        for letter in letters:
            if letter == "#":
                page_nums_to_scrape = [1]  
            else:
                page_nums_to_scrape = None  

            if page_nums_to_scrape is not None:
                for page_num in page_nums_to_scrape:
                    url = f"{base_url}{letter}&page={page_num}"
                    print(f"Scraping letter={letter}, page={page_num} → {url}")

                    driver.get(url)
                    time.sleep(2)  

                    html = driver.page_source
                    soup = BeautifulSoup(html, "html.parser")

                    details_blocks = soup.find_all("div", class_="details")
                    if not details_blocks:
                        print(f"No exhibitors found for letter '{letter}' on page {page_num}.")
                        break

                    # Extract data
                    for block in details_blocks:
                        p_tags = block.find_all("p")
                        name_org = address = contact_person = designation = ""
                        contact_details = profile = ""

                        for p in p_tags:
                            strong_tag = p.find("strong")
                            if not strong_tag:
                                continue

                            label = strong_tag.get_text(strip=True)
                            raw_text = p.get_text(strip=True)
                            value = raw_text.replace(label, "", 1).replace('\xa0', ' ').strip(" :")

                            if label.startswith("Name of the Organization"):
                                name_org = value
                            elif label.startswith("Address"):
                                address = value
                            elif label.startswith("Contact Person"):
                                contact_person = value
                            elif label.startswith("Designation"):
                                designation = value
                            elif label.startswith("Contact Details"):
                                contact_details = value
                            elif label.startswith("Profile"):
                                profile = value

                        writer.writerow([
                            letter,
                            name_org,
                            address,
                            contact_person,
                            designation,
                            contact_details,
                            profile,
                            page_num
                        ])
            else:
                page_num = 1
                while True:
                    url = f"{base_url}{letter}&page={page_num}"
                    print(f"Scraping letter={letter}, page={page_num} → {url}")

                    driver.get(url)
                    time.sleep(2)  

                    html = driver.page_source
                    soup = BeautifulSoup(html, "html.parser")

                    details_blocks = soup.find_all("div", class_="details")
                    if not details_blocks:
                        print(f"No exhibitors found for letter '{letter}' on page {page_num}. Stopping.")
                        break

                    for block in details_blocks:
                        p_tags = block.find_all("p")
                        name_org = address = contact_person = designation = ""
                        contact_details = profile = ""

                        for p in p_tags:
                            strong_tag = p.find("strong")
                            if not strong_tag:
                                continue

                            label = strong_tag.get_text(strip=True)
                            raw_text = p.get_text(strip=True)
                            value = raw_text.replace(label, "", 1).replace('\xa0', ' ').strip(" :")

                            if label.startswith("Name of the Organization"):
                                name_org = value
                            elif label.startswith("Address"):
                                address = value
                            elif label.startswith("Contact Person"):
                                contact_person = value
                            elif label.startswith("Designation"):
                                designation = value
                            elif label.startswith("Contact Details"):
                                contact_details = value
                            elif label.startswith("Profile"):
                                profile = value

                        writer.writerow([
                            letter,
                            name_org,
                            address,
                            contact_person,
                            designation,
                            contact_details,
                            profile,
                            page_num
                        ])

                    page_num += 1

    driver.quit()
    print(f"Done! Data saved in {output_csv}")

if __name__ == "__main__":
    scrape_exhibitors_selenium("exhibitors_selenium_pagination.csv")
