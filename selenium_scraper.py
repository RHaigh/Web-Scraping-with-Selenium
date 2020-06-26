import time
import pandas as pd
import csv
import random
import string
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

# As with our R script, we will look to collect a range of fuel prices from a price comparison website into a single dataframe

# As my chosen browser is chrome 79, I must match this to chromedriver 79.0.3495
driver = webdriver.Chrome(executable_path=r"/Path/to/chromedriver")

#  We can also initialise browser in headless mode to speed up the process and save on memory
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options, executable_path=r"/Users/path_to/chromedriver")

# Custom function we will use to imitate slow typing and fool anti-bot software
def slow_typing(element, text):
    for character in text:
        element.send_keys(character)
        time.sleep(0.3)

# When first visiting the website, we will be asked to register with a name and email address
# As this anti-scraping measure does not require email address confirmation, we will enter in false details to proceed
driver.get("https://www.allstarcard.co.uk/tools/uk-fuel-prices/")

# We will find the 'Name' text box and enter in the following keys
element = driver.find_element_by_css_selector("#Name")
element.send_keys('MyName')

# Next we find the 'Email' text box. As each email only allows a limited number of searches, we will need to create a new one everytime
# We will generate a random string and enter it in email format using string interpolation
def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

email = randomString(8)

element = driver.find_element_by_css_selector("#Email")
element.send_keys(f'{email}@gmail.com')
# We now send the return key from the keyboard to initiate our search
element.send_keys(Keys.RETURN)
# Allow a brief pause for the web page to load
time.sleep(5)

# We are now presented with a new selection box where we can enter a location and view local fuel prices
element = driver.find_element_by_css_selector("#NearbySitesLocation")
element.send_keys('Edinburgh')
element.send_keys(Keys.RETURN)

# A new html table is rendered with our results. We can use BeautifulSoup to find all code with the table class
soup = BeautifulSoup(driver.page_source, 'lxml')
table = soup.find_all('table')[2] # There are several tables within the html so we must grab the correct one

# Handily, pandas contains a function for converting bs4 objects into pd dataframes
df = pd.read_html(str(table))[0]

# We will now remove unnecessary blank columns and add one to show the date of the search and area
df = df.drop(['Map', 'Diesel', 'Petrol'], axis = 1)
df['Search Date'] = pd.to_datetime('today')
df['Area'] = 'Ediburgh'

# This is all we need to collect a dataframe of our fuel prices
# If we wished to search a list of locations and collate the results, we would use a custom function to loop through our list

# Enter in our chosen list of locations to search
location_list = ("Edinburgh", "Orkney", "Glasgow", "Aberdeen", "Girvan", "Kinnaird",
                   "Stranrae", "Moffat", "Aberdeen", "Ibrox")

list_of_dataframes = []
for i in location_list:
    # The registration details are only required once per active session so we need not include this in every loop as it will result in errors
    driver.get("https://www.allstarcard.co.uk/tools/uk-fuel-prices/")

    element = driver.find_element_by_css_selector("#NearbySitesLocation")
    element.send_keys(slow_typing(i))
    element.send_keys(Keys.RETURN)

    soup = BeautifulSoup(driver.page_source, 'lxml')
    table = soup.find_all('table')[2]  # There are several tables within the html so we must grab the correct one

    df = pd.read_html(str(table))[0]
    df = df.drop(['Map', 'Diesel', 'Petrol'], axis=1)
    df['Search Date'] = pd.to_datetime('today')
    df['Area'] = i

    list_of_dataframes.append(df)

final_table = pd.concat(list_of_dataframes)


