# Booker Scraper

## Login

Run `session.py`. Copy printed token as env variable `ASP_NET_SESSION`.

## Select catalog from products

```bash
q -H -O -d , "SELECT code, img_small, img_big, name, (CASE WHEN rrp IS NULL THEN wsp_inc_vat*(1+50%) AS price ELSE (CAST((CAST(rrp AS REAL) * 100) AS INT)) AS price END), sub_cat_name AS cat, additives, brand, origin_country, storage_type, description, allergy_advice, ingredients, nutrition_table, nutrition_notes, prepare_and_use, storage_information FROM product_detail.csv WHERE cat IN (SELECT * FROM sub_cat_selection.csv) AND rrp NOT NULL AND img_small NOT NULL AND img_big NOT NULL'" > catalog.csv
```

## Remove duplicates based on product names

`awk -F ',' '!seen[$3]++' catalog.csv > newcatalog.csv`
