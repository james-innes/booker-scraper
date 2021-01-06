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

Sitemap manually copied from side nav pane. Can be automated.

### 3. Category & Code

From list view scrap all product `code` and associate `sub_cat_code`.

### 4. Product Page

Using `product` table each product page can be scraped using the `code`. The `sub_cat_code` is also noted as it can not be determined from the product page.

### 5. Put the data together

Collate the product page data with the `sub_cat_name` and format some of the fields.  
Only use certain sub categories persisted in `sub_cat_selection.csv`.  
Final output is `catalog` view.

## TODO

- Remove pound sign from all currency.
- Remove duplicates based on product names  
`awk -F ',' '!seen[$4]++' catalog.csv > newcatalog.csv`
