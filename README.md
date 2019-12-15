# Dynamic Webscraper Using Selenium WebDriver & BeautifulSoup
A guide for analysts who require data from dynamic web pages where traditional url webscraping cannot be used.  

Author: Richard Haigh

Date of Intial Upload: 15/12/2019

Written - Python 2.7.16 (upgrade to 3)

Environment: PyCharm Community Ed 2019.3

Software Requirements: Selenium Webdriver 

The most difficult and important task is initially aligning your browser, driver and selenium versions as any mis-match here
will result in failure to execute. 

Note that selenium webdriver allows you to use the following broswer that must be matched with a specific webdriver:
- Chrome and Chromedriver
- Firefox and GeckoDriver
- Internet Explorer and IEDriver

Links to download each browsers relevent driver:

Chrome:	https://sites.google.com/a/chromium.org/chromedriver/downloads
Edge:	https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
Firefox:	https://github.com/mozilla/geckodriver/releases
Safari:	https://webkit.org/blog/6900/webdriver-support-in-safari-10/

The driver MUST match the version of the browser. You may then install Selenium Webdriver Java dependencies. Simply follow the 
instructions at: https://selenium-python.readthedocs.io/installation.html

Once you have successfully aligned and installed the correct versions and dependencies, you are ready to go.

Many traditional web-scraping methods rely on feeding in a particular url. For example, a beautifulsup or scrapy based tool to 
collect info on available phones would be fed the url: "https://www.amazon.co.uk/s?k=phones&ref=nb_sb_noss_1"

With this, you could then instruct your scraper to collect the html on this newly rendered search results page. 

BUT some websites are dynamic and built using advanced javascript. These websites have a static url while the html rendering 
is based on user input. How do you program a web-scraper to enter set data for you then collect the results on such a page? 

With selenium WebDriver. 

Selenium is a tool meant for testing web applications. You program it to execute a wide range of commands on your webpage to
test for vulnerabilities that may be exploited through ignorance or malice. We can use this to enter in paticular values into 
search bars, press buttons and enter commands, then pass our session to BeautifulSoup to scrape the resulting dynamic html. 
Finally, we pass the results to the csv library and write to csv in our project folder. 

In this tutorial, we have used the allstarcard fuel price comparison page. 
