import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Keys


def start_driver():
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    return webdriver.Chrome(options=options)


def get_html(driver, query):
    driver.get(query)
    time.sleep(15)
    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.END)
    time.sleep(10)
    return driver.page_source


def get_links(html):
    soup = BeautifulSoup(html, features="html.parser")
    return soup.find_all("a")
