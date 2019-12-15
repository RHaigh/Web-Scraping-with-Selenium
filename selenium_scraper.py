import time
import csv
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

# Match chrome 79 to chromedriver 79.0.3495
location_list = ("Dunrossness", "Orkney", "Lochbroom", "Aberfeldy", "Ford", "Kinnaird",
                   "Springside", "Moffat", "Linton", "Ibrox")

driver = webdriver.Chrome(executable_path=r"/Users/richardhaigh/Downloads/chromedriver")

for i in location_list:
    filename = (i + "_fuel_prices.csv")
    csv_writer = csv.writer(open(filename, 'w'))

    driver.get("https://www.allstarcard.co.uk/tools/uk-fuel-prices/")
    element = driver.find_element_by_css_selector("#postcode")
    element.send_keys(i)
    element = driver.find_element_by_css_selector("#find-my-nearest-station > button")
    element.send_keys(Keys.RETURN)
    time.sleep(5)

    # Selenium handover to BS
    soup = BeautifulSoup(driver.page_source, 'lxml')
    # Identify results table
    table = soup.find_all('table')[2]
    rows = table.select('tbody > tr')
    header = [th.text.rstrip() for th in table.find_all('th')]

    # Write header as first row then iterate over body results
    with open(filename, 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(header)
        for row in rows[0:]:
            data = [th.text.rstrip() for th in row.find_all('td')]
            writer.writerow(data)

