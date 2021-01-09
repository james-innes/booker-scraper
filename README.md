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

Run `login.py`. Copy printed token as env variable `ASP_NET_SESSION`.


### 2. Sitemap

Sitemap manually copied from side nav pane. Could be automated.

### 3. Category & Code

From list view scrap all product `code` and associate `sub_cat_code`.  
`scrapy crawl category`

### 4. Product Page

From the aforementioned step we have the `category` table which we now use to scrap each product page using the `code`.
The category can not be determined from the product page markup alone.  
`scrapy crawl product`

### 5. Put the data together

The SQLite DB collates the information using views.

## TODO

- `barcode` and `category` broken using ProductPipeline
- Remove pound sign from all currency.
- Automate renaming of cats e.g remove "Retail" and replace "and" with "&"
- Automate loading of new info into database form scraper
