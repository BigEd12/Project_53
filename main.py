import json
import time
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

GOOGLE_FORM_LINK = "https://docs.google.com/forms/d/e/1FAIpQLSfUIL67ShcwT3-_XFwp0tgkVLbVM5IUbIAUYy4wgdLyfz11nw/viewform?usp=sf_link"
ZILLOW_LINK = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A-122.30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D"
CHROME_DRIVER_PATH = "C:\Dev\chromedriver.exe"

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}

response = requests.get(ZILLOW_LINK, headers=header)
webpage = response.text

soup = BeautifulSoup(webpage, "html.parser")

script_data = soup.select_one("script[data-zrr-shared-data-key]").contents[0].strip("!<>-")
data = json.loads(script_data)

address, price, link = [], [], []
for item in data["cat1"]["searchResults"]["listResults"]:
    address.append(item["address"])
    price.append(item["units"][0]["price"].strip("$+").replace(",", "") if "units" in item else item["unformattedPrice"])
    link.append(item["detailUrl"] if item["detailUrl"].startswith("http") else f"https://www.zillow.com{item['detailUrl']}")

print(len(address), len(price), len(link))
print(address)
print(price)
print(link)

total_listings = len(address)

driver = webdriver.Chrome(CHROME_DRIVER_PATH)
driver.get(GOOGLE_FORM_LINK)

time.sleep(2)

for listing in range(0, total_listings):

    address_input = driver.find_element(By.XPATH, '/html/body/div/div[2]/form/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    address_input.send_keys(address[listing])

    price_input = driver.find_element(By.XPATH, '/html/body/div/div[2]/form/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_input.send_keys(price[listing])

    link_input = driver.find_element(By.XPATH, '/html/body/div/div[2]/form/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_input.send_keys(link[listing])

    send_button = driver.find_element(By.XPATH, '/html/body/div/div[2]/form/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    send_button.click()

    send_another = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    send_another.click()

time.sleep(5)
driver.quit()

