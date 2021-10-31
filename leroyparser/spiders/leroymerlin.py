import scrapy
from scrapy.http import HtmlResponse
from leroyparser.items import LeroyparserItem
from scrapy.loader import ItemLoader


class LeroymerlinSpider(scrapy.Spider):
    name = 'leroy'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['https://leroymerlin.ru/catalogue/svetodiodnye-lampy/']


    def parse(self, response: HtmlResponse):
        next_page = response.css('[data-qa-pagination-item="right"]::attr("href")').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.css('.iypgduq_plp::attr("href")').getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)


    # def vacancy_parse(self, response: HtmlResponse):
    #     title = response.css('.header-2::text').get()
    #     photos = response.css('[media=" only screen and (min-width: 1024px)"]::attr("data-origin")').extract()
    #     link = response.request.url
    #     price = response.css('.primary-price [slot="price"]::text').get()
    #     item = LeroyparserItem(title=title, photos=photos, link=link, price=price)
    #     yield item


    def vacancy_parse(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroyparserItem(), response=response)
        loader.add_css('title', '.header-2::text')
        loader.add_css('photos', '[media=" only screen and (min-width: 1024px)"]::attr("data-origin")')
        loader.add_value('link', response.url)
        loader.add_css('price', '.primary-price [slot="price"]::text')
        yield loader.load_item()
        