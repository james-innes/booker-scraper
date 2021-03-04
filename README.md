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
`scrapy crawl product_list`

Load outputted CSV file into Database for the following step!

### 4. Product Detail

From the aforementioned step we have the `product_list` table which we now use to scrap each product page using the `code`.
`scrapy crawl product_detail`

Load the data into database.

### 5. View the database

SQLite views collate data which can be exported to CSV.
