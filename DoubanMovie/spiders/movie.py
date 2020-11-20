import scrapy
from DoubanMovie.items import DoubanmovieItem


class MovieSpider(scrapy.Spider):
    name = 'movie'
    allowed_domains = ['douban.com']
    start_urls = ['https://movie.douban.com/top250']

    #def start_requests(self):
    #    url = 'https://movie.douban.com/top250'
    #    yield Request(url, headers=self.headers)

    def parse(self, response):
        movie_el_list=response.xpath('//*[@class="grid_view"]/li')
        for movie_el in movie_el_list:
            item=DoubanmovieItem()
            item['movie_name_zh']=movie_el.xpath('.//span[@class="title"][1]/text()').extract_first()
            item['score']=movie_el.xpath('.//span[@class="rating_num"]/text()').extract_first()
            item['description'] = movie_el.xpath('.//span[@class="inq"]/text()').extract_first()
            yield item

        next_url=response.xpath('//span[@class="next"]/a/@href').extract_first()
        if(next_url!=None):
            url=response.urljoin(next_url)
            yield scrapy.Request(url=url)


