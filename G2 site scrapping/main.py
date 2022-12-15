import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
#REQUIRED FOR HEADLESS PART 1
from selenium.webdriver.chrome.options import Options
#REQUIRED FOR HEADLESS
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from datetime import date
import csv
import cloudscraper
import undetected_chromedriver as uc

#Set location of Chrome Driver
#path = 'C:\Program Files (x86)\chromedriver.exe'
s = Service('C:\Program Files (x86)\chromedriver.exe')

#Set some selenium chrome options
chromeOptions = Options()
chromeOptions.headless = False
driver = uc.Chrome(service=s, use_subprocess=True)
#driver = webdriver.Chrome(service=s, options=chromeOptions)

    #creating dataframe as dictionary
data={
    "Sales and Marketing":[],
    "Categories":[],
    "link of website":[],
}

#create function 

def g2_srapping():

    #this loop helps to scrap two times by keeping other constant, one with Canadian Currency and other with U.S Currency
    #URL = 'file:///C:/Users/Csolve/Downloads/All%20Categories%20_%20G2.html'
    URL = "https://www.g2.com/categories"
    driver.get(URL)
    time.sleep(3)
    print('starting.............')
            
    #This loop scraps the main rowsn sales cotegories

    sales_table = driver.find_element(By.XPATH, '//*[@id="categorySearch"]/table[1]/tbody')
    sales_rows = sales_table.find_elements(By.TAG_NAME, 'tr')
    row_list = []
    sales_link = []
    sales_categories = []
    for sales in sales_rows:
        sales_link.append(sales.find_element(By.TAG_NAME, 'a').get_attribute('href'))
        row_list.append(sales.find_element(By.TAG_NAME, 'a').text)
        sales_categories.append(sales.find_element(By.CLASS_NAME, 'categories__parent').text)
        

    #This loops scrapes the data under sub categoires of sales
    sales_hidden_rows = [14,21]
    s=606
    sales_sub_list = []
    s_sub_categories = []
    for row in sales_hidden_rows:
        
        sales_table.find_element(By.XPATH, '//*[@id="categorySearch"]/table[1]/tbody/tr['+str(row)+']/td/div/div/a').click()
        sales_sub_rows = sales_table.find_elements(By.CLASS_NAME, 'js-container-'+str(s))
        for s_sales in sales_sub_rows:
            sales_sub_list.append(s_sales.find_element(By.TAG_NAME,'a').text)
            s_sub_categories.append(s_sales.find_element(By.CLASS_NAME, 'categories__parent').text)
        s=607
  

    s_index = 0
    for i in range(len(row_list)):    
        if row_list[i]=='':
            row_list[i]=sales_sub_list[s_index]
            s_index+=1
        else:
            continue
    
    val=0
    for s in range(len(sales_categories)):
        if sales_categories[s] == '':
            sales_categories[s]=s_sub_categories[val]
            val+=1
        else:
            continue
 

    #This loop is used to scrapes the main rows of Marketing         
    marketing_table = driver.find_element(By.XPATH, '//*[@id="categorySearch"]/table[2]/tbody')
    marketing_row = marketing_table.find_elements(By.TAG_NAME, 'tr')
    marketing_list = []
    marketing_link = []
    marketing_categories = []
    for market in marketing_row:
        marketing_categories.append(market.find_element(By.CLASS_NAME, 'categories__parent').text)
        marketing_list.append(market.find_element(By.TAG_NAME, 'a').text)
        marketing_link.append(market.find_element(By.TAG_NAME, 'a').get_attribute('href'))
    

    #This loops used to scrapes the data under sub categoires of marketing
    m_hidden_rows = [1,22,29,40,60,75,97,110]
    mark_sub_list = []
    c = [490,242,272,48,53,20,182,60]
    ind = 0
    m_sub_categories = []
    for row in m_hidden_rows:
        marketing_table.find_element(By.XPATH, '//*[@id="categorySearch"]/table[2]/tbody/tr['+str(row)+']/td/div/div/a').click()
        mark_sub_rows = marketing_table.find_elements(By.CLASS_NAME, 'js-container-'+str(c[ind]))
        ind+=1
        for sub in mark_sub_rows:
            m_sub_categories.append(sub.find_element(By.CLASS_NAME, 'categories__parent').text)
            mark_sub_list.append(sub.find_element(By.TAG_NAME,'a').text)

    
    m_index = 0
    for i in range(len(marketing_list)):    
        if marketing_list[i]=='':
            marketing_list[i]=mark_sub_list[m_index]
            m_index+=1
            
        else:
            continue

    val1=0
    for m in range(len(marketing_categories)):
        if marketing_categories[m] == '':
            marketing_categories[m] = m_sub_categories[val1]
            val1+=1

    # Concatinate both sales and marketing data and save to csv file
    categories = sales_categories+marketing_categories
    sales_and_marketing = row_list+marketing_list
    listof_link = sales_link+marketing_link

    for value in range(len(listof_link)):
    
        
        data["Sales and Marketing"].append(sales_and_marketing[value])
        data['Categories'].append(categories[value])
        data['link of website'].append(listof_link[value])
        
    #save the data to csv file with defined setting
    df = pd.DataFrame(data)    
    df.to_csv('companies.csv',mode='w',encoding="utf-8", lineterminator="\n", quotechar='"', quoting=csv.QUOTE_ALL, index=False)
    print('done.........')


#Call the function
g2_srapping()


