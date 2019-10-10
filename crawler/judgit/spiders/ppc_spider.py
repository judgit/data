import scrapy
from judgit.items import JudgitItem
from judgit import id_string, text_content


class PPCSpider(scrapy.Spider):
    name = 'ppc'

    def start_requests(self):
        urls = [
            'https://www.ppc.go.jp/news/budget/2014review/',
            'https://www.ppc.go.jp/news/budget/2015review/',
            'https://www.ppc.go.jp/news/budget/2016review/',
            'https://www.ppc.go.jp/news/budget/2017review/',
            'https://www.ppc.go.jp/news/budget/2018review/',
            'https://www.ppc.go.jp/aboutus/budget/2019review/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        title = response.css('h1::text').get()
        year = 1988 + int(title[2:4])
        for tr in response.css('tbody>tr'):
            n = len(tr.css('td'))
            if n < 2:
                continue
            item = JudgitItem()
            project_number = text_content(tr.css('td:nth-child(1)::text'))
            if '-' in project_number:
                n1, n2 = project_number.split('-')
                item['project_number1'] = n1
                item['project_number2'] = n2
            else:
                item['project_number2'] = id_string(project_number)
            url = tr.css('td:nth-child({}) a'.format(n)).attrib['href']
            item['url'] = 'https://www.ppc.go.jp' + url
            item['ministry'] = '個人情報保護委員会'
            if year == 2014:
                name = text_content(tr.css('td:nth-child(2) a::text'))
                item['project_name'] = name.split()[0]
            else:
                name = text_content(tr.css('td:nth-child(2)::text'))
                item['project_name'] = name
            item['year'] = year
            yield item
