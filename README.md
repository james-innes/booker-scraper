# How to prepare catalog

## Select catalog from products

```bash
q -H -O -d , "SELECT code, img_small_url AS image, name, (CAST((CAST(rrp AS REAL) * 100) AS INT)) AS price, sub_cat_name AS cat FROM product.csv WHERE cat IN (SELECT * FROM sub_cat_selection.csv) AND rrp NOT NULL AND image <> 'https://dcveehzef7grj.cloudfront.net/img/smb/no-image-250.png'" > catalog.csv
```

## Clean product names

`clean_names.py`

## Remove duplicates based on product names

`awk -F ',' '!seen[$3]++' catalog.csv > newcatalog.csv`