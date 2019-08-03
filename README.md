### EventBriteCrawl

Web Crawler to crawl EventBrite. 

What it does - 

1) Go to EventBrite
2) Clicks on Search
3) Search field to be set (currently Singapore but it can be changed in the code)
4) Filters for "Conference" and "Paid"
5) Systematically goes through the filtered results and extracts their info which are:
- Event Name
- Ticket Price
- Event Date
- Event Location
6) The crawler will stop once it reaches 30 pages.
7) Extracted information will then be transformed further (due to the unclean data)
  - Clean up Location and Event Date
  - Ticket Prices
8) Filters out tickets which are less than 300

#### Areas for improvement
1) Unable to extract some events - these are events which has pages that are not the standard EventBrite pages and hence unable to extract the info
2) Ticket prices are not standard currency - may be USD, EUR, or SGD (in my case) 
