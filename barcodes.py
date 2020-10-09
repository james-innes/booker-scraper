

# Instead of using static website running on local host use sitemap.json to visit all category pages and click print list and then scrap barcodes for all the products

# Seleiumn webdriver here


selectors = [
    {
        "id": "categories",
        "type": "SelectorLink",
        "parentSelectors": ["_root"],
        "selector": "a",

    },
    {
        "id": "sub-categories",
        "type": "SelectorLink",
        "parentSelectors": ["categories"],
        "selector": "a",

    },
    {
        "id": "print-product-list",
        "type": "SelectorLink",
        "parentSelectors": ["sub-categories"],
        "selector": "#printRow a",
    }
    {
        "id": "ungrouped-proceed",
        "type": "SelectorLink",
        "parentSelectors": ["print-product-list"],
        "selector": "a#hypUngrouped2",

    },
    {
        "id": "table-row",
        "type": "SelectorElement",
        "parentSelectors": ["ungrouped-proceed"],
        "selector": "tbody tr",

    },
    {
        "id": "code",
        "type": "SelectorText",
        "parentSelectors": ["table-row"],
        "selector": "td:nth-of-type(2)",
        "multiple": false,

    },
    {
        "id": "barcode",
        "type": "SelectorElementAttribute",
        "parentSelectors": ["table-row"],
        "selector": "td img",
        "multiple": false,

    }
]
