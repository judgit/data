import scrapy
from judgit.items import JudgitItem
from judgit import id_string, text_content


class CAASpider(scrapy.Spider):
    name = 'caa'

    def start_requests(self):
        urls = [
            'https://www.caa.go.jp/policies/budget/review/2013/review_sheet_003/',
            'https://www.caa.go.jp/policies/budget/review/2013/review_sheet_004/',
            'https://www.caa.go.jp/policies/budget/review/2014/review_sheet_003/',
            'https://www.caa.go.jp/policies/budget/review/2014/review_sheet_004/',
            'https://www.caa.go.jp/policies/budget/review/2015/review_sheet_003/',
            'https://www.caa.go.jp/policies/budget/review/2015/review_sheet_004/',
            'https://www.caa.go.jp/policies/budget/review/2016/review_sheet_003/',
            'https://www.caa.go.jp/policies/budget/review/2016/review_sheet_004/',
            'https://www.caa.go.jp/policies/budget/review/2017/review_sheet_003/',
            'https://www.caa.go.jp/policies/budget/review/2017/review_sheet_004/',
            'https://www.caa.go.jp/policies/budget/review/2018/review_sheet_003/',
            'https://www.caa.go.jp/policies/budget/review/2018/review_sheet_004/',
            'https://www.caa.go.jp/policies/budget/review/2019/review_sheet_002/',
            'https://www.caa.go.jp/policies/budget/review/2020/review_sheet_004.html',
            'https://www.caa.go.jp/policies/budget/review/2020/review_sheet_005/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        title = response.css(
            '#topic_path > ol > li:nth-child(5) > a::text').get()
        ey = 31 if title[:4] == '令和元年' else int(title[2:4])
        year = 1988 + ey
        for tr in response.css('tr'):
            if not tr.css('a'):
                continue
            item = JudgitItem()
            project_number = text_content(tr.css('td:nth-child(1) *::text'))
            if '-' in project_number:
                if project_number.startswith('新'):
                    n1, n2 = project_number.split('-')
                    item['project_number1'] = n1
                    item['project_number2'] = id_string(n2)
                else:
                    n2, n3 = project_number.split('-')
                    item['project_number2'] = id_string(n2)
                    item['project_number3'] = id_string(n3)[2:]
            else:
                item['project_number2'] = id_string(project_number)
            url = tr.css('a').attrib['href']
            item['url'] = 'https://www.caa.go.jp' + url
            item['ministry'] = '消費者庁'
            name = text_content(tr.css('td:nth-child(2)::text'))
            item['project_name'] = name
            item['year'] = year
            yield item
