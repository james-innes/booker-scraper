
import os, time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from dotenv import load_dotenv

load_dotenv()
print("Be patient :)")
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)
driver.get('https://www.booker.co.uk/home.aspx')
driver.find_element_by_id('OutsideHomePageControl_CustomerNumber').send_keys(os.getenv('BOOKER_ACCOUNT'))
driver.find_element_by_id('OutsideHomePageControl_cmdCustomerNumber').click()
time.sleep(0.5)
driver.find_element_by_id('LoginControl_EmailSingle').send_keys(os.getenv('BOOKER_EMAIL'))
driver.find_element_by_id('LoginControl_PasswordSingle').send_keys(os.getenv('BOOKER_PASSWORD'))
driver.find_element_by_id('LoginControl_EnterEmailPasswordSubmit').click()
cookie = driver.get_cookie('ASP.NET_SessionId')
session = cookie['value']
driver.quit()

print(session)