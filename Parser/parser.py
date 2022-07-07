from selenium import webdriver
from selenium.webdriver.common.by import By
import os


def parser(driver: webdriver.Chrome):
    data = []
    table = driver.find_element(By.TAG_NAME, "table")
    table_body = table.find_element(By.TAG_NAME, "tbody")
    table_data = table_body.find_elements(By.TAG_NAME, "tr")
    for row in table_data:
        row_values = row.find_elements(By.TAG_NAME, "td")
        name = row_values[1].find_element(By.TAG_NAME, "a").text
        link = row_values[1].find_element(By.TAG_NAME, "a").get_attribute("href")
        people = int(row_values[4].get_attribute("data-sort-value"))
        data.append({"city_name": name, "city_url": link, "city_population": people})
    return data


def loader(url: str):
    driver = webdriver.Chrome(os.path.join(os.getcwd(), "Parser", "Driver", "chromedriver.exe"))
    driver.get(url)
    return parser(driver)


