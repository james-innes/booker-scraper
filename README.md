# Booker Scraper

## Process

### 1. Login

`.env`

```env
BOOKER_ACCOUNT=
BOOKER_EMAIL=
BOOKER_PASSWORD=
ASP_NET_SESSION=
```

Run `session.py`. Copy printed token as env variable `ASP_NET_SESSION`.


### 2. Sitemap

Sitemap manually copied from side nav pane. Could be automated.

### 3. Category & Code

From list view scrap all product `code` and associate `sub_cat_code`.  
`scrapy crawl category`

### 4. Product Page

From the aforementioned step we have the `category` table which we now use to scrap each product page.
The category can not be determined from the product page markup alone.  
`scrapy crawl product`

### 5. Put the data together

The SQLite DB collates the information into views.

## TODO

- Remove pound sign from all currency.
- Remove duplicates based on product names  
`awk -F ',' '!seen[$4]++' catalog.csv > newcatalog.csv`
- Automate loading of new info into database form scraper
