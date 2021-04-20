import scrapy
from judgit.items import JudgitItem
from judgit import id_string, text_content


class FSASpider(scrapy.Spider):
    name = 'fsa'

    def start_requests(self):
        urls = [
            'https://www.fsa.go.jp/common/budget/kourituka/03_h27/saisyu.html',
            'https://www.fsa.go.jp/common/budget/kourituka/03_h28/saisyu.html',
            'https://www.fsa.go.jp/common/budget/kourituka/03_h29/saisyu/saisyu.html',
            'https://www.fsa.go.jp/common/budget/kourituka/03_h30/saisyu/saisyu.html',
            'https://www.fsa.go.jp/common/budget/kourituka/03_h31/saisyuu.html',
            'https://www.fsa.go.jp/common/budget/kourituka/03_R2/saisyuu.html',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        title = response.css(
            '#location > ul > li:nth-child(5) > a::text').get()
        ey = 31 if title[:4] == '令和元年' else int(title[2:4])
        year = 1988 + ey
        for tr in response.css('#main tbody tr'):
            item = JudgitItem()
            project_number = text_content(tr.css('th:nth-child(1) *::text'))
            if not project_number:
                continue
            project_number = project_number.replace('－', '-')
            if '-' in project_number:
                n2, n3 = project_number.split('-')
                item['project_number2'] = id_string(n2)
                item['project_number3'] = id_string(n3)[2:]
            else:
                item['project_number2'] = id_string(project_number)
            for a in tr.css('td:nth-child(3) a'):
                if a.attrib['href'].endswith('.pdf'):
                    url = a.attrib['href']
            if year == 2018:
                if url[-7] == '-':
                    item['project_number1'] = '新{}'.format(ey)
            elif year == 2017:
                if int(url[-11:-9]) == 31:
                    item['project_number1'] = '新30'
            else:
                if url[-6] == '-' and int(url[-8:-6]) >= ey:
                    item['project_number1'] = '新' + url[-8:-6]
            item['url'] = 'https://www.fsa.go.jp' + url
            item['ministry'] = '金融庁'
            name = text_content(tr.css('td:nth-child(2) *::text'))
            item['project_name'] = name
            item['year'] = year
            yield item
