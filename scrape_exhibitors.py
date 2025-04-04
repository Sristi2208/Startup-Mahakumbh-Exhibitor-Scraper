import requests
from bs4 import BeautifulSoup
import csv
import string

def scrape_exhibitors(output_csv="exhibitors.csv"):
    base_url = (
        "https://startupmahakumbh.org/exhibitor_directory/"
        "exhi_list_pub.php?event_name=sm&event_year=2025&filter="
    )
    # Letters A through Z
    letters = list(string.ascii_uppercase)  # ['A','B',...'Z']
    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Letter",
            "Name of the Organization",
            "Address",
            "Contact Person",
            "Designation",
            "Profile"
        ])

        for letter in letters:
            url = base_url + letter
            print(f"Scraping {url} ...")
            response = requests.get(url)
            if response.status_code != 200:
                print(f"Failed to retrieve page for letter {letter}, status: {response.status_code}")
                continue

            soup = BeautifulSoup(response.text, "html.parser")
            details_blocks = soup.find_all("div", class_="details")
            if not details_blocks:
                print(f"No exhibitors found for letter {letter}")
            
            for block in details_blocks:
                p_tags = block.find_all("p")
                name_org = address = contact_person = designation  = profile = ""
                
                for p in p_tags:
                    strong_tag = p.find("strong")
                    if not strong_tag:
                        continue
                    label = strong_tag.get_text(strip=True)
                    raw_text = p.get_text(strip=True)
                    value = raw_text.replace(label, "", 1).replace('\xa0', ' ').strip(" :").encode('latin1', errors='ignore').decode('utf-8', errors='ignore')

                    if label.startswith("Name of the Organization"):
                        name_org = value
                    elif label.startswith("Address"):
                        address = value
                    elif label.startswith("Contact Person"):
                        contact_person = value
                    elif label.startswith("Designation"):
                        designation = value
                    elif label.startswith("Profile"):
                        profile = value

                writer.writerow([
                    letter,
                    name_org,
                    address,
                    contact_person,
                    designation,
                    profile
                ])

if __name__ == "__main__":
    scrape_exhibitors("exhibitors.csv")
    print("Done! The data has been saved to exhibitors.csv.")
