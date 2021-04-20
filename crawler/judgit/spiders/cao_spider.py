import re
import scrapy
from judgit.items import JudgitItem
from judgit import text_content

pattern = re.compile(r'^(.+)\(.+\)(※.+)?$')


class CAOSpider(scrapy.Spider):
    name = 'cao'

    def start_requests(self):
        urls = [
            'https://www.cao.go.jp/yosan/review_25_2.html',
            'https://www.cao.go.jp/yosan/review_26_2.html',
            'https://www.cao.go.jp/yosan/review_27_2.html',
            'https://www.cao.go.jp/yosan/review_28_2.html',
            'https://www.cao.go.jp/yosan/review_29_2.html',
            'https://www.cao.go.jp/yosan/review_30_2.html',
            'https://www.cao.go.jp/yosan/review_1_2.html',
            'https://www.cao.go.jp/yosan/review_2_3.html'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        title = response.css('h1::text').get()
        year = 1988 + int(title[2:4])
        for tr in response.css('tr'):
            if len(tr.css('td')) < 2:
                continue
            item = JudgitItem()
            project_number = tr.css('td:nth-child(1)::text').get()
            if '-' in project_number:
                n1, n2 = project_number.split('-')
                item['project_number1'] = n1
                item['project_number2'] = n2
            else:
                item['project_number2'] = project_number
            url = tr.css('td:nth-child(2) a').attrib['href']
            item['url'] = 'https://www.cao.go.jp/yosan/' + url
            item['ministry'] = '内閣府' if 'naikakufu' in url else '内閣官房'
            name = text_content(tr.css('td:nth-child(2) a::text'))
            item['project_name'] = pattern.match(name)[1]
            item['year'] = year
            yield item
