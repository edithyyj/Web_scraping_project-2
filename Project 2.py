#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import time
from urllib.request import Request

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import os

import pymongo
from pymongo import MongoClient

import json


# # Selenium:  The Bored Ape Yacht Club
# ## (1)

# In[5]:


url = "https://opensea.io/collection/boredapeyachtclub?search[sortAscending]=false&search[stringTraits][0][name]=Fur&search[stringTraits][0][values][0]=Solid%20Gold"


# ## (2)

# In[70]:


def main_question2():
    try:
        url_ape = "https://opensea.io/collection/boredapeyachtclub?search[sortAscending]=false&search[stringTraits][0][name]=Fur&search[stringTraits][0][values][0]=Solid%20Gold"
        browser = webdriver.Chrome()
        browser.get(url_ape)
        time.sleep(2)
        for i in range(1,9):
            top_ape = browser.find_element(By.XPATH,f"//*[@id='main']/div/div/div/div[5]/div/div[7]/div[3]/div[2]/div/div[{i}]/article/a")
            top_ape.click()
            time.sleep(5)
            file = open(f"bayc_{i}.htm", "wb")
            content = browser.page_source.encode()
            file.write(content)
            file.close()
            browser.back()
        browser.close()

    except Exception as ex:
        print("Error:" + str(ex))

if __name__ == '__main_question2__':
    main_question2()

main_question2()


# ## (3)

# In[79]:


def main_question3():
    try:
        client = MongoClient()
        client = MongoClient('localhost',27017)
        db = client.mydatabase
        if 'bayc' in db.list_collection_names():
            db.drop_collection('bayc')

        collection = db['bayc']
        for i in range (1,9):
            with open (f"bayc_{i}.htm") as file:
                soup = BeautifulSoup(file, 'lxml')
                name_row = soup.find_all("div", class_="item--main")
                for x in name_row: 
                    ba_name = x.find("h1", class_="sc-29427738-0 hKCSVX item--title")
                    if ba_name is not None:
                        ba_name = ba_name.text
                    else:
                        ba_name = "No name information"
                attribute_row = soup.find_all("div", class_="sc-738ec69b-0 fecmnO Panel--isOpen Panel--isFramed")
                for x in attribute_row: 
                    ba_attribute = x.find("div", class_="BasePanel--body Panel--body")
                    if ba_attribute is not None:
                        ba_attribute = ba_attribute.text
                    else:
                        ba_attribute = "No attribute information"
                ape = {"name": ba_name, "attributes": ba_attribute}
                collection.insert_one(ape)
    
    except Exception as ex:
        print("Error:" + str(ex))

if __name__ == '__main_question3__':
    main_question3()

main_question3()

#Check if information store correctly
client = MongoClient()
client = MongoClient('localhost',27017)
db = client.mydatabase
bayc = db['bayc']

result = bayc.find()

for i in result:
    print(i)


# ## (4)

# In[80]:


def main_question4():
    try:
        what_looking_for = 'Pizzeria'
        city = 'San+Francisco'
        url = f"https://www.yellowpages.com/search?search_terms={what_looking_for}&geo_location_terms={city}"
        header = {'User-agent': 'Mozilla/5.0'} 
        response = requests.get(url, headers=header)
        webcontent = response.content
        f = open('sf_pizzeria_search_page.htm','wb') 
        f.write(webcontent) 
        f.close()
        return url
    
    except Exception as ex:
        print("Error:" + str(ex))
        
if __name__ == '__main_question4__':
    main_question4()

main_question4()


# ## (5)

# In[88]:


def main_question5():
    try:
        
        def is_float(x):
            try:
                float(x)
                return True
            except ValueError:
                return False

        with open ('sf_pizzeria_search_page.htm') as file:
            soup = BeautifulSoup(file, 'lxml')
            main_content = soup.find("div", class_="search-results organic")
            main_content_list = main_content.find_all("div", class_="result")
            name_dic = []
            rank_dic = []
            store_url_dic = []
            star_rating_dic = []
            no_review_dic = []
            TA_rating_dic = []
            TA_count_dic = []
            dollar_info_dic = []
            year_info_dic = []
            review_info_dic = []
            amenities_info_dic = []

            for x in main_content_list:
                title = x.find("h2", class_="n").text
                title_index = str(title).find(".")
                rank = str(title)[:title_index]
                name = str(title)[title_index+1:]

                url = x.find_all("a", class_="business-name")[0]['href']
                store_url = f'https://www.yellowpages.com'+url
                star_info = x.find("a", class_="rating hasExtraRating")
                if star_info is not None:
                    star_rating = star_info.find('div', class_='result-rating')['class'][1]
                else:
                    star_rating = 'No star rating information'

                no_review_info = x.find("a", class_="rating")
                if no_review_info is not None:
                    no_review = no_review_info.find('span', class_='count').text
                else:
                    no_review = 'No number of reviews information'


                TA_info = x.find("div", class_="ratings")

                TA_rating_index_a = str(TA_info).find('"rating":"')
                TA_rating_index_b = str(TA_info).find(',"c')
                TA_rating = str(TA_info)[TA_rating_index_a+10:TA_rating_index_b-1]
                if is_float(TA_rating) is True:
                    TA_rating = TA_rating
                else:
                    TA_rating = 'No number of TripAdvisor rating information'

                TA_count_index_a = str(TA_info).find('"count":')
                TA_count_index_b = str(TA_info).find('}')
                TA_count = str(TA_info)[TA_count_index_a+9:TA_count_index_b-1]
                if is_float(TA_count) is True:
                    TA_count = TA_count
                else:
                    TA_count = 'No number of TripAdvisor review information'


                dollar_info = x.find("div", class_="price-range")
                if "$" in str(dollar_info):
                    dollar_info = dollar_info.text
                else:
                    dollar_info = 'No "$" information'


                year_info = x.find("div", class_="number")
                if year_info is not None:
                        year_info = year_info.text
                else:
                        year_info = 'No years in business information'

                review_info =  x.find("p", class_="body with-avatar")
                if review_info is not None:
                    review_info = review_info.text
                else:
                    review_info = 'No reviews information'


                amenities_info =  x.find("div", class_="amenities")
                if amenities_info is not None:
                    amenities_info = amenities_info.text
                else:
                    amenities_info = 'No amenities information'


                name_dic.append(name)
                rank_dic.append(rank)
                store_url_dic.append(store_url)
                star_rating_dic.append(star_rating)
                no_review_dic.append(no_review)
                TA_rating_dic.append(TA_rating) 
                TA_count_dic.append(TA_count)
                dollar_info_dic.append(dollar_info)
                year_info_dic.append(year_info)
                review_info_dic.append(review_info)
                amenities_info_dic.append(amenities_info)
                
                print(rank,name,store_url, "star rating: "+star_rating, "number of reviews: "+no_review, 
                     "TripAdvisor rating: "+TA_rating, "number of TA reviews: "+TA_count, 
                      '“$” signs: '+ dollar_info, "years in business: "+year_info,review_info, "amenities: "+amenities_info, "\n")

        return name_dic,rank_dic,store_url_dic,star_rating_dic,no_review_dic,TA_rating_dic,TA_count_dic,dollar_info_dic,year_info_dic,review_info_dic,amenities_info_dic


                
        
                
    except Exception as ex:
        print("Error:" + str(ex))
        
if __name__ == '__main_question5__':
    main_question5()

main_question5()


# ## (6)

# In[93]:


def main_question6():
    try:
        client = MongoClient()
        client = MongoClient('localhost',27017)
        db = client.mydatabase
        if "sf_pizzerias" in db.list_collection_names():
            db.drop_collection("sf_pizzerias")

        name = db["sf_pizzerias"]
        data = main_question5()
        name_dic,rank_dic,store_url_dic,star_rating_dic,no_review_dic,TA_rating_dic,TA_count_dic,dollar_info_dic,year_info_dic,review_info_dic,amenities_info_dic = data
        for i in range(0,30):
                information = {
                    "name" : name_dic[i],
                    "rank" : rank_dic[i],
                    "Store URL" : store_url_dic[i],
                    "Star Rating" : star_rating_dic[i],
                    "No. of review" : no_review_dic[i],
                    "TripAdvisor rating" : TA_rating_dic[i],
                    "No. of TA reviews" : TA_count_dic[i],
                    "$sign" : dollar_info_dic[i],
                    "Years in business" : year_info_dic[i],
                    "Review" : review_info_dic[i],
                    "Amenities" : amenities_info_dic[i]

                }
                name.insert_one(information)
        
        
        
    except Exception as ex:
        print("Error:" + str(ex))
        
if __name__ == '__main_question6__':
    main_question6()

main_question6()
#check if information store correctly
client = MongoClient()
client = MongoClient('localhost',27017)
db = client.mydatabase
sf_pizzerias = db['sf_pizzerias']


result = sf_pizzerias.find()

for i in result:
    print(i,"\n")


# ## (7)

# In[94]:


def main_question7():
    try:
        client = MongoClient()
        client = MongoClient('localhost',27017)
        db = client.mydatabase
        collection_name = db["sf_pizzerias"]

        rank_list=[]
        url_list=[]
        for i in range(0,31): 
            condition = {"rank": f'{i}'}
            column = {"rank": 1, "Store URL": 1, "_id": 0}
            result = sf_pizzerias.find(condition, column)
            for content in result:
                urls=content["Store URL"]
                ranks=content["rank"]
                url_list.append(urls)
                rank_list.append(ranks)
        for i in range(0,30):
            header = {'User-agent': 'Mozilla/5.0'} 
            response = requests.get(url_list[i], headers=header)
            webcontent = response.content
            f = open(f'sf_pizzerias_{rank_list[i]}.htm','wb') 
            f.write(webcontent) 
            f.close()
            print(f"sf_pizzerias_{rank_list[i]}.htm","create successfully!")
    
    except Exception as ex:
        print("Error:" + str(ex))
        
if __name__ == '__main_question7__':
    main_question7()

main_question7()


# ## (8)

# In[124]:


def main_question8():
    try:
        def find_store_info(file_name):
            with open (file_name) as file:
                address_dic =[]
                phone_dic = []
                website_dic = []
                soup = BeautifulSoup(file, 'lxml')
                main_content = soup.find_all("section", class_="inner-section")
                for x in main_content:

                    address = x.find("span",class_ = "address")
                    if address is not None:
                        address_index = str(address.text).find("San Francisco")
                        address = str(address.text)[:address_index-1]
                        address = address + ", San Francisco CA"
                    else: 
                        address = "No address information"

                    phone = x.find("a",class_ = "phone dockable")
                    if phone is not None:
                        phone = phone.text
                    else:
                        phone = "No phone information"

                    website = x.find("a",class_ = "website-link dockable")
                    if website is not None :
                        website = website['href']
                    else:
                        website = "No website information"

                    print(file_name,":",address,phone,website,"\n")

                    address_dic.append(address)
                    phone_dic.append(phone)
                    website_dic.append(website)

                    return address_dic, phone_dic, website_dic
        for i in range(1,31):
            find_store_info(f"sf_pizzerias_{i}.htm")
        
    except Exception as ex:
        print("Error:" + str(ex))
        
if __name__ == '__main_question8__':
    main_question8()

main_question8()


# ## (9)

# In[128]:


def main_question9():
    try:
        #code from question 8
        def find_store_info(file_name):
            with open (file_name) as file:
                address_dic =[]
                phone_dic = []
                website_dic = []
                soup = BeautifulSoup(file, 'lxml')
                main_content = soup.find_all("section", class_="inner-section")
                for x in main_content:

                    address = x.find("span",class_ = "address")
                    if address is not None:
                        address_index = str(address.text).find("San Francisco")
                        address = str(address.text)[:address_index-1]
                        address = address + ", San Francisco CA"
                    else: 
                        address = "No address information"

                    phone = x.find("a",class_ = "phone dockable")
                    if phone is not None:
                        phone = phone.text
                    else:
                        phone = "No phone information"

                    website = x.find("a",class_ = "website-link dockable")
                    if website is not None :
                        website = website['href']
                    else:
                        website = "No website information"

                    print(file_name,":",address,phone,website,"\n")

                    address_dic.append(address)
                    phone_dic.append(phone)
                    website_dic.append(website)

                    return address_dic, phone_dic, website_dic

        # new code for question 9
        def mongo_create_and_update_product():
            client = MongoClient()
            client = MongoClient('localhost',27017)
            db = client.mydatabase
            sf_pizzerias = db['sf_pizzerias']

            address_phone_website = []
            for i in range(1, 31):
                search_result = find_store_info(f"sf_pizzerias_{i}.htm")
                address_dic, phone_dic, website_dic = search_result
                for j in range(len(address_dic)):
                    information = {
                        "address" : address_dic[j],
                        "phone" : phone_dic[j],
                        "web" : website_dic[j]}
                    address_phone_website.append(information)

            header = {'User-agent': 'Mozilla/5.0'}
            url = 'http://api.positionstack.com/v1/forward'
            access_key = "e713c706a8d09c3b8cafd7971b40e4ec"


            latitude_longtitude_list = []
            for i in range(0,30):
                latitude_dic = []
                longtitude_dic = []

                query = address_phone_website[i]["address"]
                output = 'json'

                params = {'access_key': access_key, 'query': query, 'output': output}
                response = requests.get(url, params=params)

                doc = BeautifulSoup(response.content, 'html.parser')
                json_dict = json.loads(str(doc))
                if len(json_dict['data'])>0 :
                    latitude =  json_dict['data'][0]['latitude']
                    longtitude = json_dict['data'][0]['longitude']
                else:
                    latitude =  "No latitude data"
                    longtitude = "No longtitude data"

                long_la_info = {"latitude":latitude, 
                    "longtitude":longtitude}

                latitude_longtitude_list.append(long_la_info)


            for i in range(0,30):
                sf_pizzerias.update_many({"rank":f'{i+1}'},{"$set": address_phone_website[i]})
                sf_pizzerias.update_many({"rank":f'{i+1}'},{"$set": latitude_longtitude_list[i]})
                
        mongo_create_and_update_product()

        
    except Exception as ex:
        print("Error:" + str(ex))
        
if __name__ == '__main_question9__':
    main_question9()

main_question9()

#check if information store correctly
client = MongoClient()
client = MongoClient('localhost',27017)
db = client.mydatabase
sf_pizzerias = db['sf_pizzerias']


result = sf_pizzerias.find()

for i in result:
    print(i,"\n")

