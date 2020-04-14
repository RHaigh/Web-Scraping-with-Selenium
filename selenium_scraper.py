import time
import csv
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

# As my chosen browser is chrome 79, I must match this to chromedriver 79.0.3495

# Enter in our chosen list of locations to search
location_list = ("Edinburgh", "Orkney", "Glasgow", "Aberdeen", "Girvan", "Kinnaird",
                   "Stranrae", "Moffat", "Aberdeen", "Ibrox")

# Define direct path to the chromedriver.exe file
driver = webdriver.Chrome(executable_path=r"/Path/to/chromedriver")

# We could write to a table or dict object but for the practicality, we will write our table to a csv file

# As we have a list of locations, we will utilise a for loop
for i in location_list:
    filename = (i + "_fuel_prices.csv")
    csv_writer = csv.writer(open(filename, 'w'))

    # Driver.get navigates to a given url
    driver.get("https://www.allstarcard.co.uk/tools/uk-fuel-prices/")
    # Open up developer mode in Chrome or inspect element in Safari to identify the html tag required. Here we are looking for the text entry box
    element = driver.find_element_by_css_selector("#postcode")
    # Now we have found the text box, we send our string characters
    element.send_keys(i)
    # Followed by the search button. We will find both by their css tag. We could also use class or id finder functions
    element = driver.find_element_by_css_selector("#find-my-nearest-station > button")
    # We now send the return key from the keyboard to initiate our search
    element.send_keys(Keys.RETURN)
    time.sleep(5)

    # Hand over Selenium results to BS which is far better suited to hunting through our scraped results
    soup = BeautifulSoup(driver.page_source, 'lxml')
    # Identify results table
    table = soup.find_all('table')[2]
    # Select all entries within this table with the html tag <tr> as our desired data
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

