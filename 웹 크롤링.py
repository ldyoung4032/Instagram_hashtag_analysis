import requests as re
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from urllib.parse import quote_plus
import time
import re
import csv
import datetime
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import traceback
from traceback import extract_stack as exc
from datetime import datetime
from datetime import timedelta
import datetime
import re
import time
import sys
import io
import cx_Oracle
import os
os.putenv('NLS_LANG', '.UTF8')



#################################로그인과 검색어 입력
def log_in (city):

    baseUrl = 'https://www.instagram.com/explore/tags/'
    global plusUrl 
    plusUrl = str(city+"맛집")
    path = "C:\\Users\\dayoung\\Downloads\\chromedriver_win32\\chromedriver"
    global driver 
    driver = webdriver.Chrome(path) ## 경로 설정
    driver.implicitly_wait(3)

    driver.get("http://www.instagram.com")
    element_id = driver.find_element_by_name("username")
    element_pw = driver.find_element_by_name("password")
    element_id.send_keys("dayoung4032@daum.net")
    element_pw.send_keys("dhdnjf27dlf!")
    driver.find_element_by_xpath("""//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[4]/button""").click()

    element_target = driver.find_element_by_xpath("""//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input""") ## 검색창 접근
    element_target.send_keys(str(plusUrl))
    url = baseUrl  + quote_plus(plusUrl)

    driver.get(url)

    time.sleep(3)

    html = driver.page_source
    global soup 
    soup = bs(html, "html.parser")

    driver.find_element_by_css_selector('div.v1Nh3.kIKUG._bz0w').click() ## 첫 게시물 클릭
    
#########################################게시물에 대한 유알엘 선별(두가지 방법)

def get_url():  
    
    random_time = random.random()
    time.sleep((3+random_time)/3)

    html = driver.page_source
    soup = bs(html, "html.parser")

    in_url = soup.find(attrs = {"class":"c-Yi7"}) ## c-Yi7

    if in_url is None :
        
        in_url = soup.find(attrs= {"class":"gU-I7"})
    
    return in_url

###################################### url이 같다면 받지 않는다 unipue확인
def unique_url(in_url):

        connection = cx_Oracle.connect("scott/tiger@localhost:1521/xe")
        cursor = connection.cursor()

        row = (in_url,)
        cursor.execute('select count(each_url) from info_hashtag2 where each_url = (:1)',row)
        for i in cursor : ######### 중복 확인
            a = int(i[0])

        cursor.close()
        connection.commit()
        connection.close()

        return a
                
############## hash 모으기
def hash_to_list():
    
    insta = driver.find_element_by_css_selector('.XQXOT')

    if insta is None :

        insta = driver.find_element_by_css_selector('XQXOT.pXf-y')

    tag_raw = insta.text 
    tags = re.findall('#[A-Za-z0-9가-힣]+', tag_raw) 
    tag = ''.join(tags).replace("#"," ") # "#" 제거 tag_data = tag.split()

    tag_data = tag.split()

    real_tags = []

    for tag_one in tag_data: 
        real_tags.append(tag_one)

    return real_tags

############### real_tags의 길이가 1이상이라면 get data
def get_data(n, in_url, real_tags):
    
    date = driver.find_element_by_css_selector(" time._1o9PC.Nzb55").text
    
    now = datetime.datetime.now()


    if "시간" in date :
        a = re.findall('\d+', date)
        a = a[0]
        each_date = now - datetime.timedelta(hours = int(a))
        date = each_date.strftime('%Y-%m-%d')
        
    elif "분" in date :
        a = re.findall('\d+', date)
        a = a[0]
        each_date = now - datetime.timedelta(minutes = int(a))
        date = each_date.strftime('%Y-%m-%d')
        
    elif "초" in date :
        a = re.findall('\d+', date)
        a = a[0]
        each_date = now - datetime.timedelta(seconds= int(a))
        date = each_date.strftime('%Y-%m-%d')

    elif "일 전" in date :
        a = re.findall('\d+', date)
        a = a[0]
        each_date = now - datetime.timedelta(days= int(a))
        date = each_date.strftime('%Y-%m-%d')

    elif "년" in date :
        date = re.findall('\d+', date)
        if len(date[1]) == 2 and len(date[2]) == 2 :
            date = str("{0}-{1}-{2}".format(date[0], date[1], date[2]))
        elif len(date[1]) == 1 and len(date[2]) == 1 :
            date = str("{0}-0{1}-0{2}".format(date[0], date[1], date[2]))
        elif len(date[1]) == 1 and len(date[2]) != 1 :
            date = str("{0}-0{1}-{2}".format(date[0], date[1], date[2]))
        elif len(date[1]) != 1 and len(date[2]) == 1 :
            date = str("{0}-{1}-0{2}".format(date[0], date[1], date[2]))
        
        
    else:
        date = re.findall('\d+', date)
        if len(date[0]) == 2 and len(date[1]) == 2 :
            date = str("2020-{0}-{1}".format(date[0], date[1]))
        elif len(date[0]) == 1 and len(date[1]) == 1 :
            date = str("2020-0{0}-0{1}".format(date[0], date[1]))
        elif len(date[0]) == 1 and len(date[1]) != 1 :
            date = str("2020-0{0}-{1}".format(date[0], date[1]))
        elif len(date[0]) != 1 and len(date[1]) == 1 :
            date = str("2020-{0}-0{1}".format(date[0], date[1]))
        

    print("{0}번째 게시물 url = {1}, 태그 갯수 : {2}, 날짜 : {3}, 태그 : {4} ".format(n,in_url, len(real_tags),date ,real_tags))

    connection = cx_Oracle.connect("scott/tiger@localhost:1521/xe")
    cursor = connection.cursor()    
    
    ## 해시태그 관련 자료 테이블 insert
    sql = "insert into info_hashtag2 values(:1, :2, :3)"
    row = (in_url, date, plusUrl)
    cursor.execute(sql,row)

    # 해시태그 테이블 insert
    for i in range(0,len(real_tags)) :
        sql = "insert into hashtag2 values(:1, :2, :3)"
        row = (n, i+1, real_tags[i] )
        cursor.execute(sql, row)
    print("저장")
    cursor.close()
    connection.commit()
    connection.close()

##################### 다음 게시물로 넘어가기
def next_script():

    try: 
        WebDriverWait(driver, 10000).until(EC.presence_of_element_located((By.CSS_SELECTOR, '._65Bje.coreSpriteRightPaginationArrow'))) 
        driver.find_element_by_css_selector('._65Bje.coreSpriteRightPaginationArrow').click() 
        random_time = random.random()
        time.sleep((2+random_time)/5)
    except: 
        driver.close()

global city 
city = str("성동구")
log_in(city) ## 1번 : 로그인하기
for i in range(111111111111) : ## 게시물 개수 지정
    get_url() ## 2번 : url 가져오기
    in_url = get_url() ## 해당 게시물의 url을 반환받는다
    if in_url is not None : ## 2번의 url값이 none이 아니라면 3번 url의 중복 확인
        in_url = str(in_url['href'])
        in_url = in_url.split('/')
        in_url = str(in_url[2])
        unique_url(in_url)
        a = unique_url(in_url) ## 0이면 중복X, 1이면 중복
        if a == 0 : ## 중복이 아니라면 
            try :
                hash_to_list() ## 4번 해당 게시물의 text에서 hashtag list 만들기
                real_tags = hash_to_list()
                if len(real_tags) >= 1 : ## 태그가 존재하는 게시물에 대해서만 data 수집
                    get_data(i+1, in_url, real_tags)
                    # print("해당 게시물 저장 완료")
                    next_script() ## 해당 게시물의 data를 수집한 이후에 6번 next
                else :
                    next_script()
                    continue
            except :
                next_script() ## 오류가 날 경우에 6번 다음 게시물로 클릭
                continue
        else :
            next_script() ## url값이 none이면 6번 next
            continue
    else :
        next_script()
        continue
