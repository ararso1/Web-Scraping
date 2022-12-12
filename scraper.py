
import os
import pandas as pd

#import chromedriver_binary
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
#REQUIRED FOR HEADLESS PART 1
#REQUIRED FOR HEADLESS
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from datetime import date
import csv

#Set location of Chrome Driver
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

def get_chrome_driver() -> webdriver.Chrome:
    """
    This is the syntax for selenium. Please do not useselenium without discussion with the contract manager.
    The job will be considered unsuccessful if selenium is used without mutual agreement.
    
    :return: A chrome headless browser.
    """
    
    options = webdriver.ChromeOptions()
    options.add_argument("--headless") # You may use headless if you choose
    options.add_argument("--no-sandbox")
    options.add_argument('--disable-gpu')
    options.add_argument("--disable-dev-shm-usage")

    proxy_address = os.environ.get("HTTP_PROXY")

    if proxy_address:
        options.add_argument(f"--proxy-server={proxy_address}")

    return webdriver.Chrome("chromedriver.exe", options=options)


def run():
    """
    This function will be the main entrypoint to your code and will be called with a filename.
    """
    
    # We use the requests library to load data but you could also use `get_countries_via_chrome()`.
    # countries = get_countries_via_chrome()

    #this loop helps to scrap two times by keeping other constant, one with Canadian Currency and other with U.S Currency
    for cur in range(1,3):
        URL = 'https://www.ic.gc.ca/app/scr/tdst/tdo/crtr.html'
        driver = get_chrome_driver()
        driver.get(URL)
        time.sleep(1)
        today = date.today()
        #try:
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
        #except:
        #    pass
    df = pd.DataFrame(data)
    df.to_csv('sample.csv',mode='w',encoding="utf-8", lineterminator="\n", quotechar='"', quoting=csv.QUOTE_ALL, index=False)
    print('doneeeeeeeee')
    driver.quit()
run()
