import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from dotenv import load_dotenv

load_dotenv()
print("Be patient :)")
options = Options()
# options.headless = True
d = webdriver.Chrome(options=options)
d.get("https://www.booker.co.uk/home")

d.find_element(by=By.ID, value="CustomerNumber").send_keys(
    os.getenv("BOOKER_ACCOUNT"), Keys.RETURN
)
time.sleep(2)
d.find_element(by=By.ID, value="Email").send_keys(os.getenv("BOOKER_EMAIL"))
d.find_element(by=By.ID, value="Password").send_keys(
    os.getenv("BOOKER_PASSWORD"), Keys.RETURN
)
time.sleep(3)
print("ASP_NET_SESSION: " + d.get_cookie("ASP.NET_SessionId")["value"])
print("ASPXAUTH: " + d.get_cookie(".ASPXAUTH")["value"])

d.quit()
