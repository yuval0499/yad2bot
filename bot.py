import http.client, urllib
from xml.etree.ElementTree import tostring
from h11 import Data
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
import requests
from time import time
import datetime
import numpy
from bs4 import BeautifulSoup
chrome_options = ChromeOptions()
chrome_options.add_argument('--start-maximized')
chrome_options.add_argument("--log-level=3 ")
chrome_options.add_experimental_option("detach", True)
chrome_options.add_extension('./plugin.zip')
browser = Chrome(ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install(), chrome_options=chrome_options)
time1 = int(time() * 1000)
time2= time1 - 180000
currTime = str(time1)
pastTime= str(time2)
browser.get("https://www.yad2.co.il/realestate/rent?topArea=2&area=1&city=5000&propertyGroup=apartments%2Chouses&rooms=4-4&price=0-11000&startDate="+pastTime+"-"+currTime+"&myAlertsSort=1&utm_source=myAlertsRealestate&utm_medium=email&utm_campaign=myAlertsFeed")
divs = browser.find_elements_by_xpath("//div[@class='feeditem table']/div")
ids=[]
for div in divs:
    ids.append("https://www.yad2.co.il/item/"+div.get_attribute("item-id"))

numpy.unique(ids)
apts=[]
for index, item in enumerate(ids):
    apts.append({"url": "https://www.yad2.co.il/item/"+item})

spans = browser.find_elements_by_xpath("//span[@class='subtitle']")
titles=[]
for span in (spans):
    titles.append(span.get_attribute("innerHTML"))
numpy.unique(titles)
    
pricedivs = browser.find_elements_by_xpath("//div[@class='price']")
prices=[]
for div in (pricedivs):
    prices.append(div.get_attribute("innerHTML"))
numpy.unique(prices)

data=[]
for index, item in enumerate(titles):
    data.append({'title':  item, "price": prices[index]})

for index, i in enumerate(data):
    print("here")
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
    urllib.parse.urlencode({
        "token": "ap1rvqw91kt3bc73q5n64y8do9z7z1",
        "user": "uq9nyb1m87id4ip9iao94ax2u5scht",
        "message": i['title']+ " " + i['price'],
        "url": ids[index]
    }), { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()
    
browser.close()
