import scrapy
from judgit.items import JudgitItem
from judgit import id_string, text_content


class NPASpider(scrapy.Spider):
    name = 'npa'

    def start_requests(self):
        urls = [
            'https://www.npa.go.jp/policies/budget/review/h25/24-saisyukohyo.html',
            'https://www.npa.go.jp/policies/budget/review/h25/25-saisyukohyo.html',
            'https://www.npa.go.jp/policies/budget/review/h25/26-saisyukohyo.html',
            'https://www.npa.go.jp/policies/budget/review/h26/25-saisyukohyo.html',
            'https://www.npa.go.jp/policies/budget/review/h26/26-saisyukohyo.html',
            'https://www.npa.go.jp/policies/budget/review/h26/27-saisyukohyo.html',
            'https://www.npa.go.jp/policies/budget/review/h27/26-saisyukohyo.html',
            'https://www.npa.go.jp/policies/budget/review/h27/27-saisyukohyo.html',
            'https://www.npa.go.jp/policies/budget/review/h27/28-saisyukohyo.html',
            'https://www.npa.go.jp/policies/budget/review/h28/27-saisyukohyo.html',
            'https://www.npa.go.jp/policies/budget/review/h28/28-saisyukohyo.html',
            'https://www.npa.go.jp/policies/budget/review/h28/29-saisyukohyo.html',
            'https://www.npa.go.jp/policies/budget/review/h29/29-tyukankohyo.html',
            'https://www.npa.go.jp/policies/budget/review/h29/29-tyukankohyo_sinnki.html',
            'https://www.npa.go.jp/policies/budget/review/h29/H30_youkyuu.html',
            'https://www.npa.go.jp/policies/budget/review/h30/30-cyukankohyo29.html',
            'https://www.npa.go.jp/policies/budget/review/h30/30-cyukankohyo_sinnki.html',
            'https://www.npa.go.jp/policies/budget/review/h30/H31_youkyuu.html',
            'https://www.npa.go.jp/policies/budget/review/h31/R1-cyukankohyo30.html',
            'https://www.npa.go.jp/policies/budget/review/h31/R1-cyukankohyo_sinnki.html',
            'https://www.npa.go.jp/policies/budget/review/h31/R2-saishyukohyo_sinnki.html',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        ey = int(response.url[46:48])
        year = 1988 + ey
        for tr in response.css('tr'):
            if not tr.css('a'):
                continue
            item = JudgitItem()
            project_number = text_content(tr.css('td:nth-child(1) *::text'))
            if not project_number:
                continue
            if year >= 2017:
                if 'sinnki' in response.url:
                    item['project_number1'] = '新{}'.format(ey)
                elif 'youkyuu' in response.url:
                    item['project_number1'] = '新{}'.format(ey + 1)
            else:
                y = int(response.url[49:51])
                if y >= ey:
                    item['project_number1'] = '新{}'.format(y)
            item['project_number2'] = id_string(project_number)
            if year >= 2017:
                url = tr.css('td:nth-child(2) a').attrib['href']
            else:
                url = tr.css('td:nth-child(3) a').attrib['href']
            item['url'] = 'https://www.npa.go.jp' + url
            item['ministry'] = '警察庁'
            name = text_content(tr.css('td:nth-child(2) *::text'))
            item['project_name'] = name
            item['year'] = year
            yield item
