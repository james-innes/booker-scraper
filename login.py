
import os
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv

load_dotenv()
print("Be patient :)")
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)
driver.get('https://www.booker.co.uk/home')
driver.find_element_by_id('CustomerNumber').send_keys(os.getenv('BOOKER_ACCOUNT'), Keys.RETURN)
time.sleep(0.5)
driver.find_element_by_id('Email').send_keys(os.getenv('BOOKER_EMAIL'))
driver.find_element_by_id('Password').send_keys(os.getenv('BOOKER_PASSWORD'), Keys.RETURN)
session = driver.get_cookie('ASP.NET_SessionId')['value']
driver.quit()

print(session)
