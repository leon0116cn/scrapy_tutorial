import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = ['http://quotes.toscrape.com/']

    # def start_requests(self):
    #     urls = [
    #         'http://quotes.toscrape.com/page/1/',
    #         'http://quotes.toscrape.com/page/2/',
    #     ]
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'title': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall()
            }

        # next_page = response.css("li.next a::attr(href)").get()
        # if next_page is not None:
            # next_page = response.urljoin(next_page)
            # yield scrapy.Request(url=next_page, callback=self.parse)

        for a in response.css('li.next a'):
            yield response.follow(a, callback=self.parse)


class AuthorSpider(scrapy.Spider):
    name = 'author'
    start_urls = start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        for a in response.css('.author + a'):
            yield response.follow(a, self.parse_author)

        for a in response.css('li.next a'):
            yield response.follow(a, self.parse)

    def parse_author(self, response):
        def extrace_with_css(query):
            return response.css(query).get(default='').strip()

        yield {
            'name': extrace_with_css('h3.author-title::text'),
            'birthdate': extrace_with_css('.author-born-date::text'),
            'bio': extrace_with_css('.author-born-location::text'),
            'description': extrace_with_css('.author-description::text')
        }
