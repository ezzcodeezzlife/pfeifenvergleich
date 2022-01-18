from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import pymongo
from bs4 import BeautifulSoup
d = webdriver.Chrome(executable_path='chromedriver.exe')
import datetime
from helperfunctions import priceStringToFloat
import os
from dotenv import load_dotenv
load_dotenv()

#scrape nav links from link (sale) and save in array
ul_links = []
under_ul_links = []

# Hauptseite bestimmen
site = d.get("https://hookahflow.de/") 
time.sleep(2)

ul_links = ["https://hookahflow.de/shisha/","https://hookahflow.de/tabak/","https://hookahflow.de/kohle/"]

#save every under ul links  
for link in ul_links:
    d.get(link)
    time.sleep(3)
    try:
    #Bearbeiten
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

    #category
    categorysammlung = d.find_elements_by_xpath("//a[contains(@class, 'navigation--link is--active')]")
    category = categorysammlung[2].get_attribute("title") #Hier aufpassen!
    print("-----------> " + category) 
    

    selection = d.find_elements_by_xpath("//div[@class = 'product--box box--image']")
    for child in selection:
        try:
            #print(child.get_attribute('innerHTML'))
            soup = BeautifulSoup(child.get_attribute('innerHTML'),  features="html.parser")
            
            #title
            title = soup.find("a", {"class": "product--title"})
            print(title.text.lower())

            #preis
            preis = soup.find("span", {"class": "price--default is--nowrap"})
            print(preis.text)
            #link
            link = soup.find("a", href=True)
            

            #img
            """img = ""
            for el in soup.findAll('img', attrs = {'srcset' : True}):
                img = el['srcset']"""

            personDocument = {
                "title": title.text.lower(),
                "price": priceStringToFloat(preis.text),
                "category": category,
                "link": link['href'],
                #"img": img,
                "created": datetime.datetime.now(),
                }
            
            key = {"title": title.text.lower()}

            people.update( key , personDocument, upsert=True)
            print("\n document updated or inserted:" , personDocument)
        except Exception as e:
            print("ERROR WITH PRODUCT INSERTION", e)