import sys
##from PyQt4.QtGui import QApplication
##from PyQt4.QtCore import QUrl
##from PyQt4.QtWebKit import QWebPage



"""
# Developer : Pritam Samadder
# Developer Email : pritamsamadder048@gmail.com
# Scrap Website : https://www.expedia.co.in
"""
import selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


import bs4
from bs4 import BeautifulSoup as bs
import urllib.request
import datetime
import csv
import html
import time










##class WebClient(QWebPage):
##    
##    def __init__(self,url):
##        self.app=QApplication(sys.argv)
##        QWebPage.__init__(self)
##        self.loadFinished.connect(self.on_page_load)
##        self.mainFrame().load(QUrl(url))
##		self.app.exec_()
##
##    def on_page_load(self):
##        self.app.quit()
##

#04/01/2017

#.co.in format == month/day/year ->  day/month/year
#base_url="https://www.expedia.co.in/Fort-Walton-Beach-Destin-Hotels-Sandestin-Golf-And-Beach-Resort.h67449.Hotel-Information?chkin={0}%2F{1}%2F{2}&chkout={3}%2F{4}%2F{5}&rm1=a2&regionId=0&sort=recommended&hwrqCacheKey=b7ad0f0f-c7e2-4c4d-b825-8446cddf71a8HWRQ1490790643521&vip=false&c=b182dc7f-8230-4cca-8198-6d25dc320292&&exp_dp=207.31&exp_ts=1490790645057&exp_curr=USD&exp_pg=HSR&rfrr=Redirect.From.www.expedia.com%2FFort-Walton-Beach-Destin-Hotels-Sandestin-Golf-And-Beach-Resort.h67449.Hotel-Information#chkin={6}%2F{7}%2F{8}&chkout={9}%2F{10}%2F{11}&adults=2&children=0&ts=1490790751405"



#.com format = month/day/year
base_url="https://www.expedia.com/Fort-Walton-Beach-Destin-Hotels-Sandestin-Golf-And-Beach-Resort.h67449.Hotel-Information?chkin={0}%2F{1}%2F{2}&chkout={3}%2F{4}%2F{5}&rm1=a2&regionId=0&sort=recommended&hwrqCacheKey=b7ad0f0f-c7e2-4c4d-b825-8446cddf71a8HWRQ1490790643521&vip=false&c=b182dc7f-8230-4cca-8198-6d25dc320292&&exp_dp=207.31&exp_ts=1490790645057&exp_curr=USD&exp_pg=HSR&#chkin={6}%2F{7}%2F{8}&chkout={9}%2F{10}%2F{11}&daysInFuture=&stayLength=&adults=2&children=0&ts=1490850477220"

od=[]
urls=[]
allarticles=[]
singledayarticles=[]
sd=datetime.date(2017,4,1)
ed=None
max_day=30
parameters=[]
explicit_timeout=10000
explicit_timecount=0


sd=datetime.date(2017,4,1)
for x in range(max_day):
    ed=sd+datetime.timedelta(days=1)
    furl=base_url.format(str(sd.month),str(sd.day),str(sd.year),str(ed.month),str(ed.day),str(ed.year),str(sd.month),str(sd.day),str(sd.year),str(ed.month),str(ed.day),str(ed.year))  #.com
    #furl=base_url.format(str(sd.month),str(sd.day),str(sd.year),str(ed.month),str(ed.day),str(ed.year),str(sd.day),str(sd.month),str(sd.year),str(ed.day),str(ed.month),str(ed.year))
    print(furl)
    
    explicit_timecount=0
    
    browser = webdriver.Firefox()
    browser.get(furl)
    print()
    print("data loaded in browser")
    time.sleep(3)
    try:
        print("clicking on link")
        browser.find_element_by_link_text("Continue to the U.S. site at Expedia.com").click();
        print("clicked 1")
        time.sleep(3)
        browser.find_element_by_link_text("Continue to the U.S. site at Expedia.com").click();
        print("clicked 2")
        time.sleep(3)
    except:
        pass
    
    sourcecode=browser.page_source
    soup=bs(sourcecode,"lxml")
    articles=soup.find_all("tbody",{ "class":"room"})
    while(len(articles)<1):
        sourcecode=browser.page_source
        soup=bs(sourcecode,"lxml")
        articles=soup.find_all("tbody",{ "class":"room"})
        explicit_timecount+=1
        if (explicit_timecount>explicit_timeout):
            break
    print("found {0} hotel types ".format(len(articles)))
    singledayarticle=[]
    browser.quit()
    if(len(articles)<1):
        sd=ed
        continue
    print("extracting hotel details for date : ",sd.__str__())
    for article in articles:

        try:

            print("extracting a type")
            hotelname=article.find("h3","room-name").text.strip()
            square_area=article.find("span","square-area").text.strip()
            bed_type=article.find("div",{"class":["bed-types" ,"bold-bed-types"]}).text.strip()
            extra_bed_type=article.find("div","extra-bed-types").text.strip().strip("(").strip(")").replace("\n"," ")
            max_guest=article.find("span","max-guest-msg").text.strip()
            
            max_child=article.find("span","child-msg").text.strip().strip("(").strip(")")
            current_price=article.find("span","room-price ").text.strip()
        except:
            print("skipping this type")
            continue;
##        distance=article.find("li","distance secondary tabAccess").text.strip()
##        hoteldetail=html.unescape(article.find("div","sponsoredListingDescription secondary gt-mobile").text.strip())
##        hotelprice=article.find("li","actualPrice price fakeLink ").text.strip().split("\n")[1].strip()

        temp_data=[sd.__str__(),ed.__str__(),hotelname,square_area,bed_type,extra_bed_type,max_guest,max_child,current_price]
        if(len(temp_data)<9):
            del(temp_data)
            continue

        singledayarticles.append(temp_data)
        del(temp_data)
    
    
    allarticles.append(singledayarticles)

    sd=ed



try:
    f = open("one_month_hotel_details.csv", 'w',newline='')
    writer = csv.writer(f)
    writer.writerow(["check in","check out","hotel name","square area","bed type","extra bed type","max guest","max child","current price"])
    for da in allarticles:
        for sa in da:
            writer.writerow(sa)


    f.flush()
    f.close()
except:
    print("error while trying to write data to csv file")

    try:
        f.flush()
        f.close()
    except:
        pass


