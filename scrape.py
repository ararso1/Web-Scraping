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

#Set location of Chrome Driver
#path = 'C:\Program Files (x86)\chromedriver.exe'
s = Service('C:\Program Files (x86)\chromedriver.exe')

#Set some selenium chrome options
chromeOptions = Options()
chromeOptions.headless = True
driver = webdriver.Chrome(service=s, options=chromeOptions)

    #creating dataframe as dictionary
data={
    "scrape_datetime":[],
    "trade_type":[],
    "trader":[],
    "trading_partner":[],
    "time_period":[],
    "value_type":[],
    "product_option":[],

    "month":[],
    "value":[]
}

#create function 

def initialize_browser():

    #this loop helps to scrap two times by keeping other constant, one with Canadian Currency and other with U.S Currency

    for cur in range(1,3):
        URL = 'https://www.ic.gc.ca/app/scr/tdst/tdo/crtr.html'
        driver.get(URL)
        time.sleep(1)
        today = date.today()
        try:
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="reportType"]/option[4]'))).click()
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="naArea"]/option[1]'))).click()
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="countryList"]/option[2]'))).click()
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="timePeriod"]/option[5]'))).click()
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="currency"]/option['+str(cur)+']'))).click()
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="searchType"]/option[1]'))).click()
            
            trader_type=driver.find_element(By.XPATH,'//*[@id="reportType"]/option[4]').text
            trader=driver.find_element(By.XPATH, '//*[@id="naArea"]/option[1]').text
            trading_partner=driver.find_element(By.XPATH,'//*[@id="countryList"]/option[2]').text
            time_period=driver.find_element(By.XPATH, '//*[@id="timePeriod"]/option[5]').text
            value_type=driver.find_element(By.XPATH, '//*[@id="currency"]/option['+str(cur)+']').text
            product_option=driver.find_element(By.XPATH, '//*[@id="searchType"]/option[1]').text
            
            driver.find_element(By.XPATH, '//*[@id="runReport"]').click()
            
            #used to scrape months and total value in dollar 
            months = driver.find_elements(By.CLASS_NAME, 'text-center')
            tot_value = driver.find_elements(By.TAG_NAME, 'td')
                
            listof_month = []
            listof_value = []
            for month in months:
                listof_month.append(month.text)
            for tot in tot_value:
                listof_value.append(tot.text)
            
            #save the data to csv file with defined setting
            data["scrape_datetime"].append(today)
            data['trade_type'].append(trader_type)
            data['trader'].append(trader)
            data['trading_partner'].append(trading_partner)
            data['time_period'].append(time_period)
            data['value_type'].append(value_type)
            data['product_option'].append(product_option)
            data['month'].append(listof_month[-1])
            data['value'].append(str(listof_value[-1]))
        except:
            pass
    df = pd.DataFrame(data)
    df.to_csv('sample.csv',mode='w',encoding="utf-8", lineterminator="\n", quotechar='"', quoting=csv.QUOTE_ALL, index=False)
    print('done')
#Call the function
initialize_browser()


