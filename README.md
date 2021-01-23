# Booker Scraper

## Process

### 1. Login

`.env`

```env
BOOKER_ACCOUNT=
BOOKER_EMAIL=
BOOKER_PASSWORD=
ASP_NET_SESSION=
ASPXAUTH=
```

Run `login.py` every time Spiders return non 200 responses and copy printed values into `.env`.

### 2. Sitemap

Sitemap manually copied from side nav pane. Could be automated.

### 3. Product List

From list view scrap all product `code` and associate `sub_cat_code` as well as price information.  
`scrapy crawl category`

### 4. Product Detail

From the aforementioned step we have the `category` table which we now use to scrap each product page using the `code`.
`scrapy crawl product`

### 5. Put the data together

Import CSV files as table into SQLite DB which collates the information using views.

## TODO

- Automate renaming of cats e.g remove "Retail" and replace "and" with "&"
