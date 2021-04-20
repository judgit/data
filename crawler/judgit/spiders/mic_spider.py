import scrapy
from judgit.items import JudgitItem
from judgit import id_string, text_content


class MICSpider(scrapy.Spider):
    name = 'mic'

    def start_requests(self):
        urls = [
            'http://www.soumu.go.jp/menu_yosan/jigyou27/shinki/shinki_h27.html',
            'http://www.soumu.go.jp/menu_yosan/jigyou27/youkyu/youkyu_h28.html',
            'http://www.soumu.go.jp/menu_yosan/jigyou27/kizon/kizon_h26.html',
            'http://www.soumu.go.jp/menu_yosan/jigyou28/kizon/kizon_h27.html',
            'http://www.soumu.go.jp/menu_yosan/jigyou29/kizon/kizon_h28.html',
            'http://www.soumu.go.jp/menu_yosan/jigyou30/kizon/kizon_h29.html',
            'http://www.soumu.go.jp/menu_yosan/jigyou31/kizon/kizon_h30.html',
            'https://www.soumu.go.jp/menu_yosan/jigyou31/kizon/kizon_h31.html',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'parent': True})
        urls = [
            'http://www.soumu.go.jp/menu_yosan/jigyou28/shinki/shinki_h28.html',
            'http://www.soumu.go.jp/menu_yosan/jigyou28/youkyu/youkyu_h29.html',
            'http://www.soumu.go.jp/menu_yosan/jigyou29/shinki/shinki_h29.html',
            'http://www.soumu.go.jp/menu_yosan/jigyou29/youkyu/youkyu_h30.html',
            'http://www.soumu.go.jp/menu_yosan/jigyou30/shinki/shinki_h30.html',
            'http://www.soumu.go.jp/menu_yosan/jigyou30/youkyu/youkyu_h31.html',
            'http://www.soumu.go.jp/menu_yosan/jigyou31/shinki/shinki_h31.html',
            'http://www.soumu.go.jp/menu_yosan/jigyou31/youkyu/youkyu_r2.html',
            'https://www.soumu.go.jp/menu_yosan/jigyou1/shinki/shinki_r1.html',
            'https://www.soumu.go.jp/menu_yosan/jigyou2/youkyu/youkyu_r3.html',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        if 'parent' in response.meta:
            for a in response.css('#contentsWrapper > div.contentsBody > table a'):
                yield scrapy.Request(url='http://www.soumu.go.jp' + a.attrib['href'], callback=self.parse)
        else:
            title = response.css(
                '#contentsWrapper > div.bread > a:nth-child(5)::text').get()
            ey = 31 if title[:4] == '令和元年' else int(title[2:4])
            year = 1988 + ey
            for tr in response.css('#contentsWrapper > div.contentsBody > div > table > tbody > tr'):
                if not tr.css('a'):
                    continue
                item = JudgitItem()
                project_number = text_content(
                    tr.css('th:nth-child(1) *::text'))
                if not project_number:
                    project_number = text_content(
                        tr.css('td:nth-child(1) *::text'))
                if '-' in project_number:
                    n1, n2 = project_number.split('-')
                    item['project_number1'] = n1
                    item['project_number2'] = n2
                else:
                    item['project_number2'] = id_string(project_number)
                url = tr.css('a').attrib['href']
                item['url'] = 'http://www.soumu.go.jp' + url
                item['ministry'] = '総務省'
                name = text_content(tr.css('td:nth-child(2) *::text'))
                item['project_name'] = name
                item['year'] = year
                yield item
