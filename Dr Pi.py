# import packages 
import requests
from bs4 import BeautifulSoup

# headers - use to fake as if request is from browser

headers = {
    'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 12239.92.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.136 Safari/537.36'
}

#first booker login form 
login_data = {
    'OutsideHomePageControl$CustomerNumber': '303182030'
}

# second booker login form - will work when we have found all hidden values

user_data = {
    '__VIEWSTATEGENERATOR': 'E026D3EE', # check - may be dynamically created
    'LoginControl$EmailSingle': 'nigelsr@gmail.com',
    'LoginControl$PasswordSingle': 'wCeFBxSnxCpkF93m',
    'LoginControl$EnterEmailPasswordSubmit.x': '55', # may be dynamically created
    'LoginControl$EnterEmailPasswordSubmit.y': '74' # may be dynamically created
}


with requests.Session() as s:
    url = 'https://www.booker.co.uk/account/loginregister/UserLogin.aspx'
    response = s.post(url,login_data, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    print('___The First Log In Page___')
    print(soup.prettify()) # The html we need to extract hidden values from
    print("******")
    hidden_values = soup.find_all("div", {"class":"aspNetHidden"})
    print(hidden_values)

'''with requests.session() as s:
    url = 'https://www.booker.co.uk/catalog/mybooker.aspx'
    response = s.post(url, user_data, headers=headers)
    print(response.content)
    print("\n")'''
    
    # Once logged in, get robots.txt and visit all disallowed directories ;o)
