SELECT
    product.code,
    category.sub_cat_name AS cat,
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
    product.name,
    product.img_small,
    product.img_big,
    product.product_info AS info
    FROM
        product.csv product
    JOIN category.csv category ON
        (category.code = product.code)
    WHERE
        category.sub_cat_code IN (SELECT sub_cat_code FROM sub_cat_selection.csv)
    AND
        img_small like 'https%'
    AND
        img_big like 'https%';