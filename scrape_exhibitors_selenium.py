from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import csv
import string
import time

def scrape_exhibitors_selenium(output_csv="exhibitors_1.csv"):
    base_url = (
        "https://startupmahakumbh.org/exhibitor_directory/"
        "exhi_list_pub.php?event_name=sm&event_year=2025&filter="
    )
    letters = list(string.ascii_uppercase)

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
            "Profile"
        ])

        for letter in letters:
            url = base_url + letter
            print(f"Scraping with Selenium: {url}")
            driver.get(url)
            time.sleep(2)  

            html = driver.page_source

            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html, "html.parser")

            details_blocks = soup.find_all("div", class_="details")
            if not details_blocks:
                print(f"No exhibitors found for letter {letter}")

            for block in details_blocks:
                p_tags = block.find_all("p")
                name_org = address = contact_person = designation = contact_details = profile = ""

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
                    profile
                ])

    driver.quit()
    print(f"Done! Data saved in {output_csv}")


if __name__ == "__main__":
    scrape_exhibitors_selenium("exhibitors_selenium.csv")
