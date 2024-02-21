import scrapy


class HomebrewingSpider(scrapy.Spider):
    name = "homebrewing"
    allowed_domains = ["homebrewing.pl"]
    start_urls = ["https://homebrewing.pl"]

    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'ScrapperData.json'
    }

    def parse(self, response, **kwargs):
        # Wskazuje interesujące dane
        categories = response.css('.BoxOdstep ul li a::attr(href)').getall()
        category_names = response.css('.BoxOdstep ul li a::text').getall()

        for url, name in zip(categories, category_names):
            yield response.follow(url, self.parse_category, meta={'category_name': name.strip()})

    def parse_category(self, response):
        category_name = response.meta['category_name']
        products = response.css('.Okno.OknoRwd')

        for product in products:
            yield {
                'category': category_name,
                'name': product.css('.ProdCena a::text').get().strip(),
                'price': product.css('.Cena::text').get().strip().replace(' zł', '').replace(',', '.')
            }

        # Jak  poradzić sobie z indeksami stron do iteracji
        current_page = response.css('.IndexStron a.Aktywna::text').get()
        if current_page:
            next_page_number = int(current_page) + 1
            next_page_link = response.css(f'.IndexStron a[href*="s={next_page_number}"]::attr(href)').get()

            if next_page_link is not None:
                yield response.follow(next_page_link, self.parse_category, meta={'category_name': category_name})
