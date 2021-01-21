import scrapy
from yellowpages.items import YellowpagesItem
from scrapy_selenium import SeleniumRequest

class YellowSpider(scrapy.Spider):
    name = 'yellow'
    allowed_domains = ['yellowpagesofafrica.com']
    start_urls = ['https://www.yellowpagesofafrica.com/']


    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(url=url, callback=self.parse)

    def parse(self, response):
        urls = response.xpath('//div[@class="col-sm-12"]//div[@class="col-sm-4 col-xs-6 col-md-4 col-lg-3"]/a/@href').extract()

        for url in urls:
            yield SeleniumRequest(
                url = response.urljoin(url), callback = self.parse_country_page
            )
    def parse_country_page(self, response):
        urls = response.xpath('//div[@class="col-sm-12 col-lg-12 ct-u-marginBottom40"]//div[@class="row"]/a/@href').extract()

        for url in urls:
            yield SeleniumRequest(
                url = response.urljoin(url), callback = self.parse_companies_detail
            )

    def parse_companies_detail(self, response):
        country,industry = response.url.split('/')[-3:-1]
        names = response.xpath('//div[@class="col-sm-6 col-md-6 col-lg-4"]//div[@class="ct-product--tilte"]/text()').extract()
        names = [i.strip() for i in names]
    
        websites = response.xpath('//div[@class="row ct-js-search-results ct-showProducts--list ct-u-marginTop10"]//div[@class="col-sm-6 col-md-6 col-lg-4"]//div[@class="ct-product--description"]')
        for i,j in enumerate(websites):
            w = j.xpath('a/@href').extract()
            websites[i]= w if w else ""


        mails = numbers = []
        for i in response.xpath('//div[@class="row ct-js-search-results ct-showPproduct--description"]//div[@class="buttonShowCo"]'):
            id_ = i.xpath('@onclick').get().split("'")[-2]

            m = response.xpath(f'//*[@id="{id_}"]/a/@href').extract()
            mails.append(m if m else "")
            p = response.xpath(f'//*[@id="{id_}"]/text()').extract_first()
            numbers.append(p if p else "")

        for name, website, mail, number in zip(names, websites, mails, numbers):
            item = YellowpagesItem()
            item['name'] = name
            item['website'] = website
            item['mail'] = mail
            item['number'] = number
            item['country'] = country.title()
            item['industry'] = industry.title()
            print ('**parse_companies_detail:', item["name"], item["website"])
            yield item

        nxt = response.xpath('//div[@class="ct-pagination text-center"]/ul/li/a/@href').extract()
        if nxt:
            nxt = nxt[-1]
            if nxt!='#':
                yield SeleniumRequest(
                    url = response.urljoin(nxt), callback = self.parse_companies_detail
                )

        