import re
import requests
import pickle
from bs4 import BeautifulSoup
import codecs
import time 

# set up background webdriver 
# !apt install chromium-chromedriver
# !cp /usr/lib/chromium-browser/chromedriver /usr/bin

import sys,os
sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# scrape all pages
def scrape_all_pages():
    print('scraping website')
    # target URL
    url='https://www.happycow.net/oceania/australia/new_south_wales/sydney/'

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    wd = webdriver.Chrome('chromedriver',chrome_options=chrome_options)

    # get content of URL
    wd.get(url)

    # get file path to save page
    dir_name = "scraped_html"    
    while True:
      time.sleep(5)
      page_num = wd.find_element(By.XPATH,"//nav[@class='search-pager text-center']/*/li/a[@title='Current page']")
      file_name = "page_" + page_num.get_attribute('data-page')   
      print('page ' + page_num.get_attribute('data-page') )
      n = os.path.join(dir_name,file_name)    
      # open file in write mode with encoding
      f = codecs.open(n, "w", "utf−8")
      # write page source content to file
      f.write(wd.page_source)
      # if not last page then click on next page:
      
      
      if len(wd.find_elements(By.XPATH,"//nav[@class='search-pager text-center']/*/li[@class='next']")) > 0 :          
        # printing url to log progress
        time.sleep(10)
        log=WebDriverWait(wd,10).until(EC.presence_of_all_elements_located((By.XPATH ,"//nav[@class='search-pager text-center']/*/li[@class='next']/a[@class='pagination-link']")))
        print(log[0].get_attribute('href'))
        # click next page file
        more_buttons = wd.find_elements(By.XPATH,"//nav[@class='search-pager text-center']/*/li[@class='next']/a[@class='pagination-link']/span")
        for x in range(len(more_buttons)):
          if more_buttons[x].is_displayed():
              wd.execute_script("arguments[0].click();", more_buttons[x])
              time.sleep(5)
        # element=WebDriverWait(wd,10).until(EC.presence_of_all_elements_located((By.XPATH ,"//nav[@class='search-pager text-center']/*/li[@class='next']/a[@class='pagination-link']/span")))
        # element[0].click()
        continue
      else :
          wd.quit()
          break

if __name__ == '__main__':
    scrape_all_pages()

