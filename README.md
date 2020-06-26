# Dynamic Webscraper Using Selenium WebDriver & BeautifulSoup
A guide for analysts who require data from dynamic web pages where traditional url webscraping cannot be used.  

Author: Richard Haigh SG with help from Alex Betts of DEFRA

Date of Intial Upload: 15/12/2019

# Python Version

Written: Python 3.7 

Environment: PyCharm Community Ed 2019.3  

Packages: time, random, string, csv, pandas v0.25.3, beautifulsoup4 v4.8.1, selenium v3.141.0

# R Version

Written: R 3.6.3

Environment: RStudio 1.2.1335

Packages: RSelenium v1.7.7, stringr v1.4.0, purrr v0.3.3, readr v1.3.1

# Software Alignment

Software Requirements: Selenium Webdriver 

The most difficult and important task is initially aligning your browser, driver and selenium versions. Any mismatch here
will result in failure to execute. 

Note that selenium allows you to use the following browsers but each must be matched with a specific webdriver:
- Chrome and Chromedriver
- Firefox and GeckoDriver
- Internet Explorer and IEDriver

Links to download each browsers relevent driver:

Chrome:	https://sites.google.com/a/chromium.org/chromedriver/downloads
Edge:	https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
Firefox:	https://github.com/mozilla/geckodriver/releases
Safari:	https://webkit.org/blog/6900/webdriver-support-in-safari-10/

The driver version MUST match the version of the browser. You may then install Selenium Webdriver Java dependencies. Simply follow the instructions at: https://selenium-python.readthedocs.io/installation.html

Once you have successfully aligned and installed the correct versions and dependencies, you are ready to go.

Many traditional web-scraping methods rely on feeding in a particular url. For example, a beautifulsoup or scrapy based tool to collect info would be given a url something like: "https://www.amazon.co.uk/{item_to_search_for}". We typically see our desired search criteria is present within the url and can be given as a clear destination. With this, you could then instruct your scraper to collect the html on this newly rendered search results page. 

BUT some websites are dynamic and built using advanced javascript. These websites have a static url while the html rendering 
is programmed to dynamincally render based on user input. How do you program a web-scraper to enter set data for you then collect the results on such a page? 

With selenium WebDriver. 

Selenium is a tool meant for testing web applications. You program it to execute a wide range of commands on your webpage to
test for vulnerabilities that may be exploited through ignorance or malice. We can use this to enter in paticular values into search bars, press buttons and enter commands, then pass our session to BeautifulSoup to scrape the resulting dynamic html. Finally, we pass the results to the csv library and write to csv in our project folder. 

In this tutorial, we have used selenium webdriver to collect data regarding fuel prices from a major price comparison website. 

There is an R and Python version. 

Follow the guide to see how to enter a range of commands but note that this code will not work if the html of your desired page is different (as it very likely is). Use this as a tutorial on how to find the html tags you require. Many websites actively change their html on a regular basis to hinder web scraping activity that lets users access their websites without viewing ads. At the time of upload, this code is correct and functioning but if during your testing, it fails, a likely culprit will be a change in the CSS of the chosen input sections we are hunting for. Make sure to check in chrome developer mode that the style and class id are unchanged. 

Finally, please use all scraping tools responsibly. 
