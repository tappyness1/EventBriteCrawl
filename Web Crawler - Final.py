import pandas as pd
import urllib.request
import csv
from selenium import webdriver
import getpass
import time
from selenium.webdriver.support.ui import Select
import os
from selenium.webdriver.common.keys import Keys

# put in the chromepath for your chromedriver before executing this script.

chrome_path = 'chromedriver.exe'
searchfield = 'Singapore'

driver = webdriver.Chrome(chrome_path)
url = 'https://www.eventbrite.com/'
driver.get(url)
driver.find_element_by_class_name('eds-show-up-md').click()
time.sleep(2)

driver.find_element_by_id('locationPicker').send_keys(searchfield)
driver.find_element_by_class_name('eds-show-up-sw').click()
time.sleep(2)
filterbuttons = driver.find_elements_by_class_name('eds-text-bs')
# must iterate before finding the right react-id i think. need to do an if-else then
for i in filterbuttons:
    try:
        if i.text == 'More filters': filterbutton = i 
    except:
        pass
filterbutton.click()

time.sleep(1)
select_fr = Select(driver.find_element_by_id("format-select"))
select_fr.select_by_visible_text('Conference')

select_fr = Select(driver.find_element_by_id("price-select"))
select_fr.select_by_visible_text('Paid')


for i in driver.find_elements_by_class_name('eds-btn'):
    if i.text == 'Apply': i.click

time.sleep(2)

dict1 = {}
dictnum = 0
for num in range(30):
    try:
        items = driver.find_elements_by_class_name('search-event-card-wrapper')

        for item in items:
            if item.text == '':
                pass
            else:
                try:
                    elem = item.find_element_by_class_name('eds-media-card-content__action-link')
                    link = elem.get_attribute('href')
                    driver.execute_script("window.open('');")
                    time.sleep(1)
                    # Switch to the new window
                    driver.switch_to.window(driver.window_handles[1])
                    driver.get(link)
                    time.sleep(2)
                    event_name = driver.find_element_by_class_name('listing-hero-title').text
                    #print (event_name)
                    ticket_price = driver.find_element_by_class_name('js-display-price').text
                    #print (ticket_price)
                    event_details = driver.find_elements_by_class_name('event-details__data')
                    EventDetails = []
                    for i in event_details:
                        if i.text ==  '':
                            pass
                        else:
                            EventDetails.append(i.text)
        
                    dict1[dictnum] = {'EventName': event_name, 
                         'TicketPrice' : ticket_price,
                         'EventDate': EventDetails[0],
                         'EventLocation': EventDetails[1],
                         'Link': link
                         }
                    dictnum += 1
                    driver.close()
                    driver.switch_to_window(driver.window_handles[0])
                except:
                    driver.close()
                    driver.switch_to_window(driver.window_handles[0])
                    pass
    except:
        pass
    time.sleep(2)
    if driver.find_element_by_class_name('eds-l-pad-left-4').find_element_by_class_name('eds-btn').get_attribute('aria-disabled') == 'true':
        print ("No more pages")
        break
    else: driver.find_element_by_class_name('eds-l-pad-left-4').click()
    time.sleep(2)
    
data = pd.DataFrame.from_dict(dict1, orient = 'index')

data['EventDate'] = data['EventDate'].str.replace('\n', ' ')
data['EventDate'] = data['EventDate'].str.replace('Add to Calendar', '')
data['EventDate'] = data['EventDate'].str.strip()

data['EventLocation'] = data['EventLocation'].str.replace('\n', ' ')
data['EventLocation'] = data['EventLocation'].str.replace('View Map', '')
data['EventLocation'] = data['EventLocation'].str.strip()

# change all Free to blank
data['TicketPrice'] = data.apply(lambda row: np.nan if row['TicketPrice'] == 'Free' else row['TicketPrice'], axis = 1)
data['TicketPrice'] = data.apply(lambda row: np.nan if row['TicketPrice'] == '' else row['TicketPrice'], axis = 1)
data = data.dropna(subset = ['TicketPrice'])
data['TicketPrice'] = data['TicketPrice'].astype('str')
# split the price based on TicketPrice
#data[['Starting Price','Highest Price']] = data['TicketPrice'].str.split(' - ', expand = True)

data[['StartingPrice', 'Nothing','HighestPrice']] = data['TicketPrice'].str.split(expand = True)
data = data.drop(columns="Nothing")
data['HighestPrice'].fillna(value = "", inplace = True)
data['HighestPrice'].fillna(value = "", inplace = True)
data['StartingPrice'] = data['StartingPrice'].apply(lambda x: ''.join([i for i in x if i in '1234567890.']))

data['HighestPrice'] = data['HighestPrice'].apply(lambda x: ''.join([i for i in x if i in '1234567890.']))
data['StartingPrice'] = data['StartingPrice'].apply(lambda x: 0 if x == '' else x)
data['HighestPrice'] = data['HighestPrice'].apply(lambda x: 0 if x == '' else x)

data['Keep'] = data.apply(lambda row: 'Yes' if float(row['StartingPrice']) > 300 or float(row['HighestPrice']) > 300 else 'No', axis = 1)
# filter out if both starting price and highest price are below the minimum
data = data[data['Keep'] == 'Yes']
data = data.drop(columns = 'Keep')

data.to_csv('results.csv', index = False)


