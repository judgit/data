import scrapy
from judgit.items import JudgitItem
from judgit import id_string, text_content


class JTFCSpider(scrapy.Spider):
    name = 'jtfc'

    def start_requests(self):
        urls = [
            'https://www.jftc.go.jp/soshiki/kyotsukoukai/review/h23/saishu.html',
            'https://www.jftc.go.jp/soshiki/kyotsukoukai/review/h24/saishu.html',
            'https://www.jftc.go.jp/soshiki/kyotsukoukai/review/h25/h24review2.html',
            'https://www.jftc.go.jp/soshiki/kyotsukoukai/review/h25/H25saisyuu.html',
            'https://www.jftc.go.jp/soshiki/kyotsukoukai/review/h26/h26-h25-final.html',
            'https://www.jftc.go.jp/soshiki/kyotsukoukai/review/h26/h26-h26-final.html',
            'https://www.jftc.go.jp/soshiki/kyotsukoukai/review/h27/h27-final.html',
            'https://www.jftc.go.jp/soshiki/kyotsukoukai/review/index/h28-final.html',
            'https://www.jftc.go.jp/soshiki/kyotsukoukai/review/h29/h29-final.html',
            'https://www.jftc.go.jp/soshiki/kyotsukoukai/review/h30/H29review_saisyuu.html',
            'https://www.jftc.go.jp/soshiki/kyotsukoukai/review/h30/H30kaisinoreview_saisyuu.html',
            'https://www.jftc.go.jp/soshiki/kyotsukoukai/review/2019/H30review_saisyuu.html',
            'https://www.jftc.go.jp/soshiki/kyotsukoukai/review/r2/r1review_saisyuu.html',
            'https://www.jftc.go.jp/soshiki/kyotsukoukai/review/r2/r2kaishinoreview_saisyuu.html',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        title = response.css(
            '#basewrap > div.pankuzu > ul > li:nth-child(6) > a::text').get()
        ey = int(title[2:4])
        year = 1988 + ey
        for tr in response.css('tr'):
            if tr.css('td:nth-child(1)::text').get() == 'No.':
                continue
            elif tr.css('th:nth-child(1)::text').get() == 'No.':
                continue
            item = JudgitItem()
            project_number = text_content(tr.css('td:nth-child(1) *::text'))
            if '-' in project_number:
                n1, n2 = project_number.split('-')
                item['project_number1'] = '新' + n1
                item['project_number2'] = id_string(n2)
            else:
                item['project_number2'] = id_string(project_number)
            url = tr.css('td:nth-child(3) a').attrib['href']
            item['url'] = 'https://www.jftc.go.jp/soshiki/kyotsukoukai/review/h{}/'.format(
                ey) + url
            item['ministry'] = '公正取引委員会'
            name = text_content(tr.css('td:nth-child(2) *::text'))
            item['project_name'] = name
            item['year'] = year
            yield item
