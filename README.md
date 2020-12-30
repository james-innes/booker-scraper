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

Using `category.csv` each product page can be scraped using the `code` and the `sub_cat_code` is also noted as it can not be determined from the product page.

### 5. Put the data together

Collate the product page data with the `sub_cat_name` and format some of the fields.  
Only use certain sub categories persisted in `sub_cat_selection.csv`.  
Final output is `catalog.csv`.

```bash
q -H -O -d , \
"SELECT
    product.code,
    product.name,
    category.sub_cat_name AS cat,
    product.img_small,
    product.img_big,
    (CAST(
        (
            CAST(
                (
                    CASE
                        WHEN product.rrp IS NULL
                    THEN
                        (product.wsp_inc_vat + (product.wsp_inc_vat + 0.25))
                    ELSE
                        product.rrp END
                )
            AS REAL)
        * 100)
    AS INT)) AS price,
    product.product_info AS info
    FROM
        product.csv product
    JOIN category.csv category ON
        (category.code = product.code)
    WHERE
        category.sub_cat_code IN (SELECT sub_cat_code FROM sub_cat_selection.csv)
    AND
        img_small NOT NULL
    AND
        img_big NOT NULL
" > catalog.csv
```

## TODO

- Remove pound sign from all currency.
- Remove duplicates based on product names  
`awk -F ',' '!seen[$3]++' catalog.csv > newcatalog.csv`