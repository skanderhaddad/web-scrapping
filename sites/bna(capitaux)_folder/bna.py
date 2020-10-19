from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from re import split
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import codecs

def scraper(a):
    PATH = "C:\projects\The Complete Python\web scraper\chromedriver.exe"
    driver = webdriver.Chrome(PATH)
    driver.get('http://www.bnacapitaux.com.tn/?pg='+a+'&news=all')

    driver.implicitly_wait(200)
    list_date_name = driver.find_elements_by_xpath('//span[@class="NewsDate"]')
    list_title=driver.find_elements_by_xpath('//span[@class="NewsTitle"]')
    list_description=driver.find_elements_by_xpath('//div[@class="NewsDesc"]')
    list_add = driver.find_elements_by_xpath('//div[@style="text-align:right; background-color:#F7F7F7; font-weight:bolder"]')

    add_list = []
    date_list =[]
    name_list=[]
    title_list=[]
    desc_list=[]

    for p in range(len(list_date_name)):

        date_name_list=list_date_name[p].text
        date_name_list_separated=split(":",date_name_list)
        date_list.append(date_name_list_separated[0])
        name_list.append(date_name_list_separated[1])
        title_list.append(list_title[p].text)
        desc_list.append(list_description[p*2].text)

        try:

            var = list_add[p].find_element_by_link_text('[ Attachement ]')
            var1 = var.get_attribute('href')
            add_list.append(var1)
            continue
        except NoSuchElementException:
            print("")


        try:

            var = list_add[p].find_element_by_link_text('[Plus]')
            var1 = None
            add_list.append(var1)
            continue
        except NoSuchElementException:
            print("")

        var1 = None
        add_list.append(var1)
        continue



    driver.quit()
    return(date_list,name_list,title_list,desc_list,add_list)


def bna(a):

    start_time = time.time()
    date_list =[]
    name_list=[]
    title_list=[]
    desc_list=[]
    add_list =[]

    for j in range(1,a+1):
        var =scraper(str(j))
        date_list = date_list+var[0]
        name_list = name_list+var[1]
        title_list =title_list+var[2]
        desc_list =desc_list+var[3]
        add_list =add_list+var[4]
        print(j)


    date_d_news = pd.Series(date_list)
    name_d_news =pd.Series(name_list)
    title_d_news=pd.Series(title_list)
    desc_d_news=pd.Series(desc_list)
    link_d_news=pd.Series(add_list)

    df = pd.DataFrame({'date': date_d_news, 'name': name_d_news, 'title': title_d_news,'description':desc_d_news,'link':link_d_news})
    #print(df)
    print('this prog running for ',(time.time() - start_time))
    df.to_csv('C:\projects\The Complete Python\web scraper\sites\\bna_folder\\bna(200pages).csv',encoding='utf-8-sig')


