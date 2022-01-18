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


site = d.get("https://www.smoking-shisha.de/718-shisha-komplett-sets")
time.sleep(2)

skillsSection = d.find_element_by_xpath("//ul[contains(@class, 'tree dhtml')]")
for child in skillsSection.find_elements_by_xpath(".//li"):
    atag = child.find_element_by_xpath(".//a")
    link = atag.get_attribute("href")
    ul_links.append(link)
print(ul_links)


title_list = []
preis_list = []
link_list = []

client = pymongo.MongoClient(os.getenv('MONGO_CONNECTION_STRING'))
db = client.gettingStarted
people = db.people

# NO UL LINKS HERE


#get info for each product
for link in ul_links:
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
    d.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(1)
    d.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(1)


    #title
    selection = d.find_elements_by_xpath("//li[contains(@class,'ajax_block_product')]")
    print(selection)
    for child in selection:
        #print(child.get_attribute('innerHTML'))
        soup = BeautifulSoup(child.get_attribute('innerHTML'), 'html')
        
        #title
        title = soup.find("span", {"class": "grid-name"})
        print(title.text)
        title_list.append(title.getText())

        #preis
        preis = soup.find("span", {"class": "price"})
        print(preis.getText())
        preis_list.append(preis.getText())

        #link
        link = soup.find('a', href=True)
        print(link['href'])

        personDocument = {
            "title": title.text.lower(),
            "price": preis.getText(),
            "link": link['href'],
            "created": datetime.datetime.now()
            }
        people.insert_one(personDocument)
        print("\n document inserted:" , personDocument)

        


            
    
