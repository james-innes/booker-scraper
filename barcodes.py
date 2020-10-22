       # To Do : Get Bar Codes - 166-200

       # Example :
        # https://www.booker.co.uk/catalog/printbyplof.aspx?printtype=searchcategory&categoryname=cs13_200050
       # Bar Code Prefix = 'https://www.booker.co.uk/catalog/printbyplof.aspx?printtype=searchcategory&categoryname='
       # Bar Code Suffix = cat_codes (already extracted from JSON - see line 42)

       # Iterate through each of the codes, and get the barcode with xpath

       # Bar Code is also named 'alt' in the html - so we will simply call it 'barcode'

   def barcodes(self):
        # make query string using cat_codes (same as with products)
        qs_start = 'https://www.booker.co.uk/catalog/printbyplof.aspx?printtype=searchcategory&categoryname='
        barcode_urls = [(f"{qs_start}{i}") for i in cat_codes]
        for page in barcode_urls:
            request = Request(
                url=page, callback=self.barcode_parse, cb_kwargs={'cat_code': i})
            yield request

        # check for more pages? No, not required, all barcode results on one page!

    def barcode_parse(self, response):

        # get each barcode from page and add with items

        for product in response.xpath('//*[@class="genericListItem"]')  # full selector
           l2 = ItemLoader(item=BarcodeItem(), selector=product, response=response)
            l2.add_xpath('barcode', '//*[@class="genericListItem"]//img/@alt') # barcode
            l2.add_xpath('product_description', './/*[@class="genericListItem"]//td[3]').get() # Text Description
            l2.add.value('cat_code': cat_code)
            yield l2.load_item()

        # send to mariadb - INSERT in separate tables - (much easier with SQL than CSV!)
