import scrapy
from scrapy.http import HtmlResponse

from DoubanMovie.items import DoubanmovieItem
from DoubanMovie.settings import PROXY_LIST
import json
import requests


class MovieSpider(scrapy.Spider):
    name = 'movie'
    allowed_domains = ['douban.com']
    start_urls = ['https://movie.douban.com/top250']

    # def start_requests(self):
    #    url = 'https://movie.douban.com/top250'
    #    yield Request(url, headers=self.headers)

    def parse(self, response: HtmlResponse):
        reque=response.request # type:scrapy.Request

        print()
        # 当可用代理小于3个时,获取新代理
        while len(PROXY_LIST) < 3 & 1 == 0:
            get_proxy_url = 'http://webapi.http.zhimacangku.com/getip?num=1&type=2&pro=0&city=0&yys=0&port=1&pack=126415&ts=1&ys=1&cs=1&lb=1&sb=0&pb=45&mr=1&regions='
            proxy_obj = requests.get(get_proxy_url).content.decode()
            # proxy_response = scrapy.Request(url=get_proxy_url, )
            # print(proxy_response.body)
            proxy_obj = json.loads(proxy_obj)
            if (proxy_obj['success'] == True):
                temp = {}
                temp['ip'] = proxy_obj['data'][0]['ip']
                temp['port'] = proxy_obj['data'][0]['port']
                temp['expire_time'] = proxy_obj['data'][0]['expire_time']
                temp['city'] = proxy_obj['data'][0]['city']
                temp['isp'] = proxy_obj['data'][0]['isp']
                PROXY_LIST.append(temp)

        # print(response.request.meta)
        # print(response.request.headers['User-Agent'])

        movie_el_list = response.xpath('//*[@class="grid_view"]/li')
        for movie_el in movie_el_list:
            item = DoubanmovieItem()
            item['movie_name_zh'] = movie_el.xpath('.//span[@class="title"][1]/text()').extract_first()
            item['score'] = movie_el.xpath('.//span[@class="rating_num"]/text()').extract_first()
            item['description'] = movie_el.xpath('.//span[@class="inq"]/text()').extract_first()
            yield item

        next_url = response.xpath('//span[@class="next"]/a/@href').extract_first()
        if (next_url != None):
            url = response.urljoin(next_url)
            yield scrapy.Request(url=url)
