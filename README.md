# Booker Web Scrapping Project

Random Notes  
Browser support: https://pypi.org/project/webdriver-manager/
pip install -U selenium webdriver-manager

## Sitemap

Booker website is made using old version of SiteCore ASP.NET MVC and Categories / Sub-Categories navigation can not be visited with crawler as website uses javascript `javascript(visitPage)` instead of direct `href=https://` link.
To ovoid this problem `./sitemap.json` has been manually created so you can visit each Sub-Category product list page.

```json
{
  "categories": [
    {
      "name": "Beer, Cider and Alcoholic RTDs",
      "subCategories": [
        {
          "code": "CS13_200001",
          "name": "Beer"
        }
      ]
    },
  ]
}
```

## Pseudo code

```js
  for ( category in categories ) {

    for ( subCategory in category ) {

        visit productList url = `https://www.booker.co.uk/catalog/products.aspx?categoryName=${subCategory.code}`

        // Get all products in list
        yield productListItems = scrap selector(.info_r1 a)

        for ( product in productListItems ) {

            visit product url

            categoryName = category.name
            subCategoryCode = subCategory.code
            subCategoryName = subCategory.name

            // Selectors from ./productPage-selectors.json
            
            // Example:
            yield code = selector(.pip .pir ul li:contains(Code: ) span)

            // Final product object should look like this `./product-template.json`

            shelfCode = productUrl.queryParam('categoryName')
            
            // e.g:
            `https://www.booker.co.uk/catalog/productinformation.aspx?code=606053&settype=23&categoryName= {{ 307954&CS }} Url=https%3a%2f%2fwww.booker.co.uk%2fcatalog%2fproducts.aspx%3fcategoryName%3dCS13_200001%26view%3dUnGrouped%26multi%3dFalse`

        }

    }
    
  }

```


## Sample login script

```python
import requests
from bs4 import BeautifulSoup

# Headers - use to fake as if request is from browser

headers = {
    'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 12239.92.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.136 Safari/537.36'
}

#first booker login form 
login_data = {
    'OutsideHomePageControl$CustomerNumber': '***REMOVED***'
}

# second booker login form - will work when we have found all hidden values

user_data = {
    '__VIEWSTATEGENERATOR': 'E026D3EE', # check - may be dynamically created
    'LoginControl$EmailSingle': '***REMOVED***',
    'LoginControl$PasswordSingle': '#############', # I will have to give this to you :)
    'LoginControl$EnterEmailPasswordSubmit.x': '55', # may be dynamically created
    'LoginControl$EnterEmailPasswordSubmit.y': '74' # may be dynamically created
}


with requests.Session() as s:
    url = 'https://www.booker.co.uk/account/loginregister/UserLogin.aspx'
    response = s.post(url,login_data, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    print('___The First Log In Page___')
    print(soup.prettify())
    print("******")
    hidden_values = soup.find_all("div", {"class":"aspNetHidden"})
    print(hidden_values)

with requests.session() as s:
    url = 'https://www.booker.co.uk/catalog/mybooker.aspx'
    response = s.post(url, user_data, headers=headers)
    print(response.content)
    print("\n")
```