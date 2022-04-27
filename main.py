from time import sleep
from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests


class GoogleSheets:

    def __init__(self, path):
        s = Service(path)
        self.driver = webdriver.Chrome(service=s)
        self.driver.get(google_form_url)


CHROME_DRIVER_PATH = r"C:\Users\User\Desktop\Development\chromedriver.exe"

google_form_url = "https://docs.google.com/forms/d/e/1FAIpQLSdOstueSfct36Vojky4XsNcKAjSS4lq4Q2v3tboUbInx_QoHg" \
                  "/viewform?usp=sf_link"

zillow_url = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C" \
             "%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A" \
             "-122.30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C" \
             "%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A" \
             "%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse" \
             "%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B" \
             "%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D" \
             "%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min" \
             "%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D "

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

response = requests.get(url=zillow_url, headers=header)

soup = BeautifulSoup(response.text, "html.parser")

prices_tag = soup.find_all(name="div", class_="list-card-price")

price_list = [tag.getText() for tag in prices_tag]

price_list_clean = []

for price in price_list:
    if "+" in price:
        text = price.split("+")
        price_list_clean.append(text[0])
    else:
        text = price.split("/")
        price_list_clean.append(text[0])

address_tags = soup.find_all(name="address", class_="list-card-addr")

address_list_clean = [addr.getText() for addr in address_tags]

link_tags = soup.find_all(name="a", class_="list-card-link")

link_list = [link.get("href") for link in link_tags]

link_list_clean = []
for link in link_list:
    if "zillow" not in link:
        link_list_clean.append(f"https://www.zillow.com{link}")
    else:
        link_list_clean.append(link)


sheet = GoogleSheets(CHROME_DRIVER_PATH)

sleep(3)


for n in range(len(address_list_clean)):
    first_input = sheet.driver.find_element(By.XPATH,
                                            value="/html/body/div/div[2]/form/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input")
    second_input = sheet.driver.find_element(By.XPATH,
                                             value="/html/body/div/div[2]/form/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input")
    third_input = sheet.driver.find_element(By.XPATH,
                                            value="/html/body/div/div[2]/form/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input")
    submit = sheet.driver.find_element(By.XPATH,
                                       value="/html/body/div/div[2]/form/div[2]/div/div[3]/div[1]/div[1]/div/span")

    first_input.send_keys(address_list_clean[n])
    second_input.send_keys(price_list_clean[n])
    third_input.send_keys(link_list_clean[n])
    sleep(2)
    submit.click()
    sleep(3)
    submit_another = sheet.driver.find_element(By.XPATH, value="/html/body/div[1]/div[2]/div[1]/div/div[4]/a")
    submit_another.click()


