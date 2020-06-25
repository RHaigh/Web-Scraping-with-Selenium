# Import the necessary libraries
library(openxlsx)
library(stringr)
library(purrr)
library(RSelenium)
library(readr)
library(dplyr)
library(glue)
library(rvest)

# We will use selenium to navigate to a fuel prices comparison website and collect data to compare prices across Scotland
# This website has registration barriers and reactive javascript but we will show how selenium can easily bypass this

# Open browser using selenium after installing the necessary software
driver <- rsDriver(
  browser = "firefox", geckover = "latest",
  extraCapabilities = list(
    "moz:firefoxOptions" = list(
      args = list('--headless')
    )
  )
)

# Note if you receive a selenium error at this point, you most likely have to update your firefox gecko driver
# Run binman::list_versions("geckodriver") to see available drivers
# Use following code to change RSelenium default version used to compatible version
# driver <- rsDriver(browser=c("firefox"), geckover="8.0.3904.70") or simply put 'latest' if your drivers are all up to date

# This is a headless version but, if you would like to see what your code is doing, you can use:
driver <- rsDriver(
  browser = "firefox", geckover = "latest"
)

remDr <- driver[["client"]]

# Open URL
remDr$navigate("https://www.allstarcard.co.uk/tools/uk-fuel-prices/")

# Allow a pause for the html to load
Sys.sleep(3)

# Now we can see that we must register in order to proceed but testing shows that the user simply needs to submit details, not reply to an email registration
# So we will identify the input boxes using css selector and enter faux registration details
Name <- remDr$findElement(using = 'css selector',  "#Name")
Name$sendKeysToElement(list('MyName'))

# Now for each email registration, only a set number of searches are allowed so we will need to enter a new false email with each scrape
# Generate a random email address using a random string generator and string interpolation
random_string_generator <- function(n = 5000) {
  a <- do.call(paste0, replicate(5, sample(LETTERS, n, TRUE), FALSE))
  paste0(a, sprintf("%04d", sample(9999, n, TRUE)), sample(LETTERS, n, TRUE))
}

email <- random_string_generator(1)

Email <- remDr$findElement(using = 'css selector',  "#Email")
Email$sendKeysToElement(list(glue('{email}@gmal.com'), key = "enter")) # Hit enter and submit our details 

# We can now see that the webpage is ready for us to submit our locations. Again, find the necessary box using chrome css selector
searchBox <- remDr$findElement(using = 'css selector',  "#NearbySitesLocation")
  searchBox$sendKeysToElement(list(location, key = "enter"))

# But we want to look at a list of locations so will create a custom function that will enter in each location and collect the resulting table

ScrapeFuel <- function(driver, location) {
  
  remDr <- driver[["client"]]
  
  # Open URL again - necessary as there is no search box in the table render page
  remDr$navigate("https://www.allstarcard.co.uk/tools/uk-fuel-prices/")
  
  # Type in location to input text box
  searchBox <- remDr$findElement(using = 'css selector',  "#NearbySitesLocation")
  searchBox$sendKeysToElement(list(location, key = "enter"))
  
  # Get our data by passing the url object to rvest and collecting using html_nodes 
  html <- remDr$getPageSource()[[1]]
  
  table <- read_html(html) %>%
    html_nodes("table.table.table-bordered.results-table") %>% # we find the table class name using web developer tools in chrome
    .[[1]] %>%
    html_table(fill=T) #html_table handily converts data packets into data frame format
  
  # Add additional columns and tidy away empty ones
  table$Date <- Sys.Date()
  table$Location <- location
  table$Map <- NULL
  table$Petrol <- NULL
  table$Diesel <- NULL
  
  return(table)
  
}

# So now we have our custom function, let's put together a list of locations we want it to search for
location_list <- c("Dunrossness", "Orkney", "Aberfeldy", "Kinnaird", 
                   "Springside", "Moffat", "Linton", "Ibrox", "Edinburgh", "Glasgow", 
                   "Dundee", "Aberdeen", "Stranrae", "Girvan", "Fife")

# and using assign and lapply we apply this custom function to every location and put the resulting df into a list
fuel_prices_list <- lapply(location_list, function(i) {
  assign(i, ScrapeFuel(driver, i))
})

# Use to close browser
driver$server$stop()

# Bundle all our dataframes together with rbind and we have our comprehensive list of fuel prices across Scotland
fuel_prices_current <- bind_rows(fuel_prices_list)

# So the complete workflow will be:
# 1. Naviagate to url and create registration details
# 2. Cycle through list of location searches using custom function
# 3. Collect and collate results into a single dataframe

# END OF SCRIPT
