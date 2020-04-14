library(openxlsx)
library(stringr)
library(purrr)
library(RSelenium)
library(readr)

# Again, ensure you have aligned your browser to the driver. We will utilise Chrome in our search
# As with our python version, we will find a list of locations and write our resulting tables to a csv file

# As we must apply a function to a list, we will define a custom function and apply it to each list element
ScrapeFuel<-function(driver,PC){
   
  remDr <- driver[["client"]]
  
  #Open URL and navigate to the link
  remDr$navigate("https://www.allstarcard.co.uk/tools/uk-fuel-prices/")
  
  # Allow pauses to account for slow reponse times
  readrSys.sleep(3)
  
  # Type in post code once we have located the tex box by its css element 
  PostCode<-remDr$findElement(using = 'css selector',  "#postcode")
  # Send our string characters to this box
  PostCode$sendKeysToElement(list(PC, key = "enter"))
  Sys.sleep(3)
  
  # Click button to initiate the search
  Button<-remDr$findElement(using = 'css selector',  '#find-my-nearest-station > button')
  Button$clickElement()
  
  Sys.sleep(3)
  # Grab resulting rendered data
  t <- remDr$findElements(using = 'css selector', "#find-my-nearest-station > div > table")
  t <- t$getElementText()
  
  return(t)
  
}

# A handy custom function for isolating the last space character in a string
FindLastSpace<-function(x){
  LastSpace<-rev(gregexpr("\\ ", x)[[1]])[1]
  return(LastSpace)
}

# A custom function for tidying the data into a readable format 
Wrangle<-function(Scraped){
  
  Station <- as.character(Scraped)
  Fuel<-strsplit(Station,"\n")
  Fuel2<-data.frame(Station = unlist(Fuel), stringsAsFactors = FALSE)
  FuelSplit<-do.call(rbind,strsplit(Fuel2$Station," miles "))
  Prices<-do.call(rbind,strsplit(FuelSplit[,2],"\ "))
  Fuel2$Petrol <- Prices[,1]
  Fuel2$Diesel <- Prices[,2]
  Location<-FuelSplit[,1]
  Split<-map(Location,~FindLastSpace(.x))
  Fuel2 <- Fuel2[-c(1:7),] 
  Fuel2$Date <- Sys.Date()
  Fuel2$Station <- gsub("[0-9].*", "", Fuel2$Station)
  return(Fuel2)
  
}

# Now we have defined our custom functions, we apply them to each item in our list

# Open browser using selenium
driver<- rsDriver(
  browser = "firefox", geckover = "latest",
  extraCapabilities = list(
    "moz:firefoxOptions" = list(
      args = list('--headless')
    )
  )
)

# Scrape data

# CHANGE THE DESTINATIONS YOU WISH TO ENTER INTO THE SEARCH BAR HERE
location_list <- c("Dunrossness", "Orkney", "Lochbroom", "Aberfeldy", "Kinnaird", 
                   "Springside", "Moffat", "Linton", "Ibrox", "Edinburgh", "Glasgow", 
                   "Dundee", "Aberdeen", "Stranrae", "Girvan", "Fife")

# Apply our custom scraping function to each element and create a list of dataframe results using lapply
fuel_prices_list <- lapply(location_list, function(i) {
  assign(i, ScrapeFuel(driver, i))
})

# Tidy data and create a list of tidy dataframe results 
fuel_prices_tidy <- lapply(fuel_prices_list, function(i) {
  assign(as.character(i), Wrangle(i))
})

# Use to close browser
driver$server$stop()

# Save the resulting price tables as csv files - here is an example of the syntax
write.csv("fuel_prices_location1", fuel_prices_tidy[[1]])
