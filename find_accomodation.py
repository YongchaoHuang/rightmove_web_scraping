# a Python program to scrap rightmove.co.uk property data
# created by Yongchao Huang on 21/07/2021
# with refence to the framework: https://towardsdatascience.com/looking-for-a-house-build-a-web-scraper-to-help-you-5ab25badc83e

results_save_folder='/home/yongchao/Desktop/web_scrapper/' # pls modify as appropriate
total_page=10 # number of page to be mined

# before scraping, you can check what actions are allowed/enabled on the particular website by adding suffix '/robots.txt' to the website domain
# e.g. https://www.rightmove.co.uk/robots.txt

# we first use a command to reach ask a response from the website. The result will be some html code, which we will then use to get the elements we want for our final table.
import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
from random import randint
import re
from datetime import datetime
from time import time, sleep
from bs4 import BeautifulSoup
from requests import get
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

headers = ({'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})



...
#### a single page scraping example: you can skip the simple example here, or simply use it as a test case. NB: some of the methods used here may have been revised later.
# manually generate a search case with pre-set search constrains (e.g. rent, sell, buy properties, price range, location/postcode, etc), and paste the url herebase="https://www.rightmove.co.uk/property-to-rent/find.html?searchType=RENT&locationIdentifier=OUTCODE%5E1883&insId=1&radius=0.0&minPrice=&maxPrice=1500&minBedrooms=1&maxBedrooms=2&displayPropertyType=&maxDaysSinceAdded=&sortByPriceDescending=&_includeLetAgreed=on&primaryDisplayPropertyType=&secondaryDisplayPropertyType=&oldDisplayPropertyType=&oldPrimaryDisplayPropertyType=&letType=&letFurnishType=&houseFlatShare="
response = get(base, headers=headers)
print(response)
print(response.text[:1000])

html_soup = BeautifulSoup(response.text, 'html.parser')
# house_containers = html_soup.find_all('div', class_="l-searchResult is-list" )#
house_containers = html_soup.find_all('div', class_="propertyCard")

item = house_containers[0]
item.find_all('span')

# extract property price
price_str = item.find_all('span')[5].text
price = locale.atof(price_str.split('£')[1].split(' ')[0])

# The other fields we are interested: location, details, title, date posted, description, contact info, urls, etc

# location
location=item.find_all('address')[0].text
location = location.strip()

# details
detail=item.find_all('div', class_="propertyCard-details")

# heading: no. of bed room, property type, etc
heading=item.find_all('h2')[0].text.strip()

# date posted
date_str=item.find_all(class_="propertyCard-branchSummary-addedOrReduced")[0].text
match = re.search(r'\d{2}/\d{2}/\d{4}', date_str)
date = datetime.strptime(match.group(), '%d/%m/%Y').date()

# description
desc=item.find_all(class_="propertyCard-description")[0].text.strip()

# contact number
phone=item.find_all(class_="propertyCard-contactsPhoneNumber")[0].text.strip()

# get property link
url = 'https://www.rightmove.co.uk' + item.find_all('a')[1].get('href')

# get an image
image_link = item.find_all(class_="propertyCard-img")[0].img.get('src')
...


...
#### iterate through pages
prices=[]
locations=[]
headings=[]
dates=[]
descs=[]
phones=[]
urls=[]
images=[]

# total_page=10 # scrp 10 pages
# The code is made up with two for loops, which navigate through every house in the page, for every page possible.
n_pages = 0
for page in range(0, total_page):
    n_pages += 1
    print("scraping the {}th page: ".format(n_pages))
    base1='https://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=OUTCODE%5E1883&maxBedrooms=2&minBedrooms=1&maxPrice=1500&'
    index=24*page
    base2='&propertyTypes=&includeLetAgreed=false&mustHave=&dontShow=&furnishTypes=&keywords='
    page_url=base1 + 'index=' + str(index) + base2

    r = get(page_url, headers=headers)
    page_html = BeautifulSoup(r.text, 'html.parser')
    house_containers = html_soup.find_all('div', class_="propertyCard")
    if house_containers != []:
        n_property=0
        for item in house_containers:
            print("scraping the {}th property: ".format(n_property))

            # details
            # detail = item.find_all('div', class_="propertyCard-details")

            # price
            price_str = item.find_all('div', class_='propertyCard-rentalPrice-primary')[0].text
            if price_str==' ':
                price=price_str
            else:
                price = locale.atof(price_str.split('£')[1].split(' ')[0])
            prices.append(int(price))

            # location
            location = item.find_all('address')[0].text
            if location==' ':
                pass
            else:
                location = location.strip()
            locations.append(location)

            # heading: no. of bed room, property type, etc
            heading = item.find_all('h2')[0].text
            if heading==' ':
                pass
            else:
                heading = heading.strip()
            headings.append(heading)

            # date posted
            date_str = item.find_all(class_="propertyCard-branchSummary-addedOrReduced")[0].text
            if date_str == ' ':
                date=date_str
            else:
                if date_str == 'Added today' or 'Reduced today':
                    date = date.today()
                else:
                    date_str = re.search(r'\d{2}/\d{2}/\d{4}', date_str)
                    date = datetime.strptime(date_str.group(), '%d/%m/%Y').date()
            dates.append(date)

            # description
            desc = item.find_all(class_="propertyCard-description")[0].text
            if desc == ' ':
                pass
            else:
                desc = desc.strip()
            descs.append(desc)

            # contact number
            phone = item.find_all(class_="propertyCard-contactsPhoneNumber")[0].text
            if phone == ' ':
                pass
            else:
                phone = phone.strip()
            phones.append(phone)

            # get property link
            url = 'https://www.rightmove.co.uk' + item.find_all('a')[1].get('href')
            urls.append(url)

            # get an image
            image_link = item.find_all(class_="propertyCard-img")[0].img.get('src')
            images.append(image_link)

            n_property+=1
    else: # to break the loop if it finds a page without any house container.
        raise Exception("no contents returned by the page!")

    sleep(randint(1,3))
print('You scraped {} pages containing {} properties.'.format(n_pages, len(headings)))

# save the results
df = pd.DataFrame({'price': prices,
                       'location': locations,
                       'title': headings,
                       'date': dates,
                       'description': descs,
                       'phone': phones,
                       'url': urls,
                       'image': images})

df.to_excel(results_save_folder + 'rightMove.xlsx') #NB: you need to install 'openyxl' to use pandas df.to_excel(), pip install openpyxl

# EDA: price distribution over locations
from pylab import rcParams
rcParams['figure.figsize'] = 10, 6

df1 = df[["location", "price"]]
df1.groupby(["location"]).mean().plot(kind="bar")
plt.xticks(size=8, rotation=90)
plt.show()
...

# last edited by Yongchao on 21/07/2020