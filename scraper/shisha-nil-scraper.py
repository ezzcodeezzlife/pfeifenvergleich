from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import pymongo
from bs4 import BeautifulSoup
d = webdriver.Chrome(executable_path='chromedriver.exe')
import datetime
import os
from dotenv import load_dotenv
load_dotenv()

#scrape nav links from link (sale) and save in array
ul_links = []
under_ul_links = []


site = d.get("https://www.shisha-nil.de/sale?p=1")
time.sleep(2)

#oberkatregorien
skillsSection = d.find_element_by_xpath("//ul[contains(@class, 'sidebar--navigation categories--navigation navigation--list is--drop-down is--level0 is--rounded')]")
for child in skillsSection.find_elements_by_xpath(".//li"):
    atag = child.find_element_by_xpath(".//a")
    link = atag.get_attribute("href")
    ul_links.append(link)
print(ul_links)

#save every under ul links  
for link in ul_links:
    d.get(link)
    time.sleep(3)
    try:
        skillsSection = d.find_element_by_xpath("//ul[contains(@class, 'sidebar--navigation categories--navigation navigation--list is--level1 is--rounded')]")
        for child in skillsSection.find_elements_by_xpath(".//li"):
            atag = child.find_element_by_xpath(".//a")
            link = atag.get_attribute("href")
            under_ul_links.append(link)
    except:
        print("no ul found // error with under ul link")
print(under_ul_links)

title_list = []
preis_list = []
link_list = []

client = pymongo.MongoClient(os.getenv('MONGO_CONNECTION_STRING'))
db = client.gettingStarted
people = db.people



#get info for each product
for link in under_ul_links:
    site = d.get(link)
    time.sleep(3)

    d.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(0.5)
    d.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(1)
    d.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(1)
    d.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(1)

    #title
    selection = d.find_elements_by_xpath("//div[@class = 'product--box box--basic']")
    for child in selection:
        #print(child.get_attribute('innerHTML'))
        soup = BeautifulSoup(child.get_attribute('innerHTML'), 'html')
        
        #title
        title = soup.find("a", {"class": "product--title"})

        #preis
        preis = soup.find("span", {"class": "price--default"})

        #link
        link = soup.find('a', href=True)

        #img
        #img = ""
        #for el in soup.findAll('img', attrs = {'srcset' : True}):
            #img = el['srcset']

        personDocument = {
            "title": title.text.lower(),
            "price": preis.getText(),
            "link": link['href'],
            #"img": img,
            "created": datetime.datetime.now(),
            }
        people.insert_one(personDocument)
        print("\n document inserted:" , personDocument)
