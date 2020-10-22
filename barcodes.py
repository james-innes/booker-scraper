      # To Do : Get Bar Codes - 165-190

        Example:
        https: // www.booker.co.uk/catalog/printbyplof.aspx?printtype = searchcategory & categoryname = cs13_200050
        Bar Code Prefix = 'https://www.booker.co.uk/catalog/printbyplof.aspx?printtype=searchcategory&categoryname='
        Bar Code Suffix = cat_codes(already extracted from JSON - see line 42)

        Iterate through each of the codes, and get the barcode with xpath
	//*[@class= 'genericListItem']//img/alt/text() ?

        Bar Code is also named 'alt' in the html - so we will simply call it 'barcode'
        make 2nd table in a DB and do a join using product code as the KEY
        Nice.

    def barcodes(self):
        make query string using cat_codes (same as with products)
        qs_start = 'https://www.booker.co.uk/catalog/printbyplof.aspx?printtype=searchcategory&categoryname='
        barcode_urls =[(f"{qs_start}{i}") for i in cat_codes]
        for page in barcode_urls:
            request = Request(url=page,callback=self.barcode_parse)
            yield requests
            
            
   def barcode(self):
        get each barcode from page and add with items
        pass
        
