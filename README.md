# 🕸️ Startup Mahakumbh Exhibitor Scraper

This Python script scrapes exhibitor data from [Startup Mahakumbh 2025](https://startupmahakumbh.org/Exhibitor-Directory.php) for each company listed under A–Z in the directory.

It extracts the following information:

- **Name of the Organization**
- **Address**
- **Contact Person**
- **Designation**
- **Contact Details**
- **Profile**

All data is saved in a clean CSV format (`exhibitors_selenium.csv`) for further use or analysis.

---

## 📁 Files Included

- `scrape_exhibitors_selenium.py` – Main scraping script.
- `exhibitors_selenium.csv` – Output CSV with all scraped company data.
- `README.md` – This documentation file.

---

## ⚙️ Requirements

- Python 3.7+

Install required libraries:

```bash
pip install requests beautifulsoup4
pip install selenium
python scrape_exhibitors_selenium.py
```

This will:

Fetch exhibitor listings for every letter A–Z.

Parse the HTML data to extract required fields.

Save the data to exhibitors_selenium.csv.


## 🧠 How It Works
- Loops through all letters A–Z.

- Builds URLs like:
https://startupmahakumbh.org/exhibitor_directory/exhi_list_pub.php?event_name=sm&event_year=2025&filter=A

- Fetches the page content using selenium.

- Parses exhibitor blocks inside div class="details" using BeautifulSoup.

- Extracts relevant fields and uses regex to safely parse emails.

- Writes each entry into the CSV.


## 👨‍💻 Author
Built by Sristi Agrawal

Feel free to reach out for collaborations or questions!


