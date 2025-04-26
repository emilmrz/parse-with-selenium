from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from openpyxl import Workbook
import time

# 1. Selenium brauzer ayarları
options = webdriver.ChromeOptions()
#options.add_argument("--headless")  # Chrome-u gizli açır (istəsən bunu silə bilərsən görünməsi üçün)

# 2. ChromeDriver avtomatik tapılır
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# 3. Saytı açırıq
url = "https://kontakt.az/telefoniya/smartfonlar?kh_stehsal[0]=Samsung"
driver.get(url)

# 4. JavaScript tam yüklənsin deyə gözləyirik
time.sleep(10)

# 5. Saytın HTML kodunu alırıq
soup = BeautifulSoup(driver.page_source, "html.parser")
#driver.quit()

# 6. Excel faylı yaradılır
wb = Workbook()
ws = wb.active
ws.title = "Samsung S21+"
ws.append(["Model", "Price"])

# 7. Məhsulları tapırıq
products = soup.find_all("div", class_="prodItem")

# 8. S21, S22, S23, S24 modelləri seçirik
target_keywords = ["S21", "S22", "S23", "S24"]

for product in products:
    title_tag = product.find("div", class_="prodItem__title")
    price_tag = product.find("div", class_="prodItem__prices--active")

    title = title_tag.get_text(strip=True) if title_tag else ""
    price = price_tag.get_text(strip=True) if price_tag else ""

    if any(keyword in title for keyword in target_keywords):
        ws.append([title, price])

# 9. Excel faylını saxlayırıq
wb.save("samsung_s21_selenium.xlsx")
print("Hazırdır: samsung_s21_selenium.xlsx")

# 10. debug html fayl
with open("page_dump.html", "w", encoding="utf-8") as f:
    f.write(driver.page_source)

