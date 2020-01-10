import time
import csv
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

# Match chrome 79 to chromedriver 79.0.3495

# Enter in our chosen list of locations to search
location_list = ("Dunrossness", "Orkney", "Lochbroom", "Aberfeldy", "Ford", "Kinnaird",
                   "Springside", "Moffat", "Linton", "Ibrox")

# Define direct path to the chromedriver.exe file
driver = webdriver.Chrome(executable_path=r"/Users/richardhaigh/Downloads/chromedriver")

for i in location_list:
    filename = (i + "_fuel_prices.csv")
    csv_writer = csv.writer(open(filename, 'w'))

    # Driver.get navigates to a given url
    driver.get("https://www.allstarcard.co.uk/tools/uk-fuel-prices/")
    # Open up developer mode in chrome to identify the html tag required. Here we are looking for the text entry box
    element = driver.find_element_by_css_selector("#postcode")
    element.send_keys(i)
    # Followed by the search button. We will find both by their css tag. We could also use class or id find functions
    element = driver.find_element_by_css_selector("#find-my-nearest-station > button")
    element.send_keys(Keys.RETURN)
    time.sleep(5)

    # Hand over Selenium results to BS
    soup = BeautifulSoup(driver.page_source, 'lxml')
    # Identify results table
    table = soup.find_all('table')[2]
    # Select all entries within this table with the html tag <tr>
    rows = table.select('tbody > tr')
    # Identify rows with tag <th> to be used as headers in our csv table
    header = [th.text.rstrip() for th in table.find_all('th')]

    # Write header as first row then iterate over body results
    with open(filename, 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(header)
        # Iterate over subsequent rows below each header with the tag <td> to write our table
        for row in rows[0:]:
            data = [th.text.rstrip() for th in row.find_all('td')]
            writer.writerow(data)

