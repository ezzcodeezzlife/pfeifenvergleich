from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import pymongo
from bs4 import BeautifulSoup
d = webdriver.Chrome(executable_path='chromedriver.exe')
import datetime
import re
import os
from dotenv import load_dotenv
load_dotenv()

#scrape nav links from link (sale) and save in array
ul_links = []
under_ul_links = []


site = d.get("https://www.shisha-dreams.de/")
time.sleep(2)

title_list = []
preis_list = []
link_list = []

client = pymongo.MongoClient(os.getenv('MONGO_CONNECTION_STRING'))
db = client.gettingStarted
people = db.people

under_ul_links = ['https://www.shisha-dreams.de/shishas/alpha-shisha/', 'https://www.shisha-dreams.de/shishas/al-mani/', 'https://www.shisha-dreams.de/shishas/aladin-shishas/', 'https://www.shisha-dreams.de/shishas/alligator/', 'https://www.shisha-dreams.de/shishas/alookah/', 'https://www.shisha-dreams.de/shishas/amy-shisha/', 'https://www.shisha-dreams.de/shishas/aryf/', 'https://www.shisha-dreams.de/shishas/caesar/', 'https://www.shisha-dreams.de/shishas/chaos-shisha/', 'https://www.shisha-dreams.de/shishas/chill-shisha/', 'https://www.shisha-dreams.de/shishas/cyborg/', 'https://www.shisha-dreams.de/shishas/dum/', 'https://www.shisha-dreams.de/shishas/hoodz/', 'https://www.shisha-dreams.de/shishas/hustla/', 'https://www.shisha-dreams.de/shishas/invi-hookah/', 'https://www.shisha-dreams.de/shishas/kaya-shisha/', 'https://www.shisha-dreams.de/shishas/luna-hookah/', 'https://www.shisha-dreams.de/shishas/mata-leon/', 'https://www.shisha-dreams.de/shishas/moze/', 'https://www.shisha-dreams.de/shishas/oduman/', 'https://www.shisha-dreams.de/shishas/smokah/', 'https://www.shisha-dreams.de/shishas/tsar/', 'https://www.shisha-dreams.de/shishas/wd-hookah/', 'https://www.shisha-dreams.de/shishas/vendetta/', 'https://www.shisha-dreams.de/shishas/mehrschlauch-modelle/', 'https://www.shisha-dreams.de/shishas/bis-50/', 'https://www.shisha-dreams.de/shishas/bis-100/', 
'https://www.shisha-dreams.de/shishas/high-end-modelle/', 'https://www.shisha-dreams.de/shishas/top-bewertet/', 'https://www.shisha-dreams.de/shishas/edelstahl-shishas/', 'https://www.shisha-dreams.de/shishas/outdoor-shisha/', 'https://www.shisha-dreams.de/shisha-tabak/booster/', 'https://www.shisha-dreams.de/shisha-tabak/20-gramm-tabak-shot-s-proben/', 'https://www.shisha-dreams.de/shisha-tabak/anregungen/', 'https://www.shisha-dreams.de/shisha-tabak/187-tabak/', 'https://www.shisha-dreams.de/shisha-tabak/7-days-tabak/', 'https://www.shisha-dreams.de/shisha-tabak/adalya-tobacco/', 'https://www.shisha-dreams.de/shisha-tabak/aino/', 'https://www.shisha-dreams.de/shisha-tabak/almassiva-tabak/', 'https://www.shisha-dreams.de/shisha-tabak/al-ajamy-gold/', 'https://www.shisha-dreams.de/shisha-tabak/al-fakher/', 'https://www.shisha-dreams.de/shisha-tabak/al-waha/', 'https://www.shisha-dreams.de/shisha-tabak/alwazir/', 'https://www.shisha-dreams.de/shisha-tabak/aamoza/', 'https://www.shisha-dreams.de/shisha-tabak/argileh/', 'https://www.shisha-dreams.de/shisha-tabak/aqua-mentha/', 'https://www.shisha-dreams.de/shisha-tabak/bad-mad/', 'https://www.shisha-dreams.de/shisha-tabak/brohood/', 'https://www.shisha-dreams.de/shisha-tabak/bluehorse/', 'https://www.shisha-dreams.de/shisha-tabak/chaos/', 'https://www.shisha-dreams.de/shisha-tabak/covid-21/', 'https://www.shisha-dreams.de/shisha-tabak/darkside-tobacco/', 'https://www.shisha-dreams.de/shisha-tabak/electro-smog/', 'https://www.shisha-dreams.de/shisha-tabak/fadi-tobaggo/', 'https://www.shisha-dreams.de/shisha-tabak/gringo-tabak/', 'https://www.shisha-dreams.de/shisha-tabak/habiboz/', 'https://www.shisha-dreams.de/shisha-tabak/hasso-tabak/', 'https://www.shisha-dreams.de/shisha-tabak/hookain/', 'https://www.shisha-dreams.de/shisha-tabak/holster/', 'https://www.shisha-dreams.de/shisha-tabak/hookah-squad/', 'https://www.shisha-dreams.de/shisha-tabak/koenig-im-schatten/', 'https://www.shisha-dreams.de/shisha-tabak/maridan/', 'https://www.shisha-dreams.de/shisha-tabak/mazaya-mza/', 'https://www.shisha-dreams.de/shisha-tabak/moloko-tabak/', 'https://www.shisha-dreams.de/shisha-tabak/nameless/', 'https://www.shisha-dreams.de/shisha-tabak/nakhla/', 'https://www.shisha-dreams.de/shisha-tabak/octo-buzz/', 'https://www.shisha-dreams.de/shisha-tabak/os-doobacco/', 'https://www.shisha-dreams.de/shisha-tabak/ottamann/', 'https://www.shisha-dreams.de/shisha-tabak/revoshi/', 'https://www.shisha-dreams.de/shisha-tabak/savu/', 'https://www.shisha-dreams.de/shisha-tabak/shades/', 'https://www.shisha-dreams.de/shisha-tabak/stahl-specht/', 'https://www.shisha-dreams.de/shisha-tabak/smokah-tobacco/', 'https://www.shisha-dreams.de/shisha-tabak/the-don-hookah/', 'https://www.shisha-dreams.de/shisha-tabak/tumbaki/', 'https://www.shisha-dreams.de/shisha-tabak/true-passion/', 'https://www.shisha-dreams.de/shisha-tabak/vidavi/', 'https://www.shisha-dreams.de/shisha-tabak/xracher/', 'https://www.shisha-dreams.de/shisha-tabak/zomo/', 'https://www.shisha-dreams.de/shisha-tabak/weitere/', 'https://www.shisha-dreams.de/tabakersatz/bigg-steam-stones/', 'https://www.shisha-dreams.de/tabakersatz/shiazo-dampfsteine/', 'https://www.shisha-dreams.de/tabakersatz/cloudz-by-7days/', 'https://www.shisha-dreams.de/tabakersatz/hookain-intensify/', 'https://www.shisha-dreams.de/tabakersatz/hookahsqueeze/', 'https://www.shisha-dreams.de/tabakersatz/true-cloudz-creme/', 'https://www.shisha-dreams.de/tabakersatz/cloud-one/', 
'https://www.shisha-dreams.de/tabakersatz/shishavaping/', 'https://www.shisha-dreams.de/shisha-kohle/selbstzuender-kohle/', 'https://www.shisha-dreams.de/shisha-kohle/naturkohlen/', 'https://www.shisha-dreams.de/shisha-kohle/kohleanzuender/', 'https://www.shisha-dreams.de/shisha-schlaeuche/silikonschlaeuche/', 'https://www.shisha-dreams.de/shisha-schlaeuche/premium-schlaeuche/', 'https://www.shisha-dreams.de/shisha-schlaeuche/silikonschlaeuche-als-set/', 'https://www.shisha-dreams.de/shisha-schlaeuche/mundstuecke/', 'https://www.shisha-dreams.de/shisha-schlaeuche/schlauch-zubehoer/', 'https://www.shisha-dreams.de/tabakkoepfe/kopfsets-mit-aufsatz/', 'https://www.shisha-dreams.de/tabakkoepfe/aufsaetze/', 'https://www.shisha-dreams.de/tabakkoepfe/steinkoepfe/', 'https://www.shisha-dreams.de/tabakkoepfe/silikonkoepfe/', 'https://www.shisha-dreams.de/tabakkoepfe/glaskoepfe/', 'https://www.shisha-dreams.de/tabakkoepfe/tonkoepfe/', 'https://www.shisha-dreams.de/tabakkoepfe/funnels-einlochkoepfe/', 'https://www.shisha-dreams.de/tabakkoepfe/aladin-phunnels/', 'https://www.shisha-dreams.de/tabakkoepfe/ath-koepfe/', 'https://www.shisha-dreams.de/tabakkoepfe/cyborg-funnel/', 'https://www.shisha-dreams.de/tabakkoepfe/denka-bowl/', 'https://www.shisha-dreams.de/tabakkoepfe/hookain-drip-bowl-lit-lip/', 'https://www.shisha-dreams.de/tabakkoepfe/ks-original-steinkoepfe/', 'https://www.shisha-dreams.de/tabakkoepfe/luna-crater-phunnel/', 'https://www.shisha-dreams.de/tabakkoepfe/oblako/', 'https://www.shisha-dreams.de/tabakkoepfe/siebeinlagen/', 'https://www.shisha-dreams.de/tabakkoepfe/weitere-koepfe/', 'https://www.shisha-dreams.de/zubehoer/alufolie-zubehoer/', 'https://www.shisha-dreams.de/zubehoer/dichtungen/', 'https://www.shisha-dreams.de/zubehoer/ersatzglaeser/', 'https://www.shisha-dreams.de/zubehoer/glasrauchsaeulen/', 'https://www.shisha-dreams.de/zubehoer/feuchthaltemittel-melassen/', 'https://www.shisha-dreams.de/zubehoer/faerbemittel/', 'https://www.shisha-dreams.de/zubehoer/hygienemundstuecke/', 'https://www.shisha-dreams.de/zubehoer/kohleteller/', 'https://www.shisha-dreams.de/zubehoer/kohlekoerbe/', 'https://www.shisha-dreams.de/zubehoer/koffer-und-taschen/', 'https://www.shisha-dreams.de/zubehoer/kopfadapter/', 'https://www.shisha-dreams.de/zubehoer/kohle-zangen/', 'https://www.shisha-dreams.de/zubehoer/kohleanzuender/', 'https://www.shisha-dreams.de/zubehoer/led-module/', 'https://www.shisha-dreams.de/zubehoer/molassefaenger/', 'https://www.shisha-dreams.de/zubehoer/reinigung/', 'https://www.shisha-dreams.de/zubehoer/schlauchadapter-und-anschluesse/', 'https://www.shisha-dreams.de/zubehoer/schlauch-aufhaengung/', 'https://www.shisha-dreams.de/zubehoer/windschutz/', 'https://www.shisha-dreams.de/zubehoer/sonstiges/']

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
    selection = d.find_elements_by_xpath("//div[@class = 'product--box box--image']")
    for child in selection:
        print("checking new ul link")
        #print(child.get_attribute('innerHTML'))
        soup = BeautifulSoup(child.get_attribute('innerHTML'), 'html')
        
        #title
        title = soup.find("a", {"class": "product--title"})
        #print(title.text)
        title_list.append(title.text)

        #preis
        preis = soup.find("span", {"class": "price--default"})
        #print(preis.getText())
        integer_price = re.findall(r"[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", preis.getText()) #get int and float puit of str

        #link
        link = soup.find('a', href=True)
        #print(link['href'])

        print("found details. adding to datbase...")
        personDocument = {
            "title": title.text.lower(),
            "price": integer_price[0] + ',' + integer_price[1],
            "link": link['href'],
            "created": datetime.datetime.now()
            }
        people.insert_one(personDocument)
        print("\n document inserted:" , personDocument)

        

        


            
    
