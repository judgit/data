import scrapy
from judgit.items import JudgitItem
from judgit import id_string, text_content


class ReconstructionSpider(scrapy.Spider):
    name = 'reconstruction'

    def start_requests(self):
        urls = [
            (2015, 2014, 'https://www.reconstruction.go.jp/topics/main-cat8/sub-cat8-3/reviewsheet_h27/20150909100503.html'),
            (2015, 2015, 'https://www.reconstruction.go.jp/topics/main-cat8/sub-cat8-3/reviewsheet_h27/20150909101133.html'),
            (2015, 2016, 'https://www.reconstruction.go.jp/topics/main-cat8/sub-cat8-3/reviewsheet_h27/20150917103043.html'),
            (2016, 2015, 'https://www.reconstruction.go.jp/topics/main-cat8/sub-cat8-3/review_h28/saishu28/20160907111909.html'),
            (2016, 2016, 'https://www.reconstruction.go.jp/topics/main-cat8/sub-cat8-3/review_h28/saishu28/20160907112011.html'),
            (2016, 2017, 'https://www.reconstruction.go.jp/topics/main-cat8/sub-cat8-3/review_h28/saishu28/20160915092354.html'),
            (2017, 2016, 'https://www.reconstruction.go.jp/topics/main-cat8/sub-cat8-3/review_h29/rs29page/h29rss28jigyou-summary.html'),
            (2017, 2017, 'https://www.reconstruction.go.jp/topics/main-cat8/sub-cat8-3/review_h29/rs29page/h29rss29kaisi-jigyou-summary.html'),
            (2017, 2018, 'https://www.reconstruction.go.jp/topics/main-cat8/sub-cat8-3/review_h29/rs29page/h29rss30youkyu_jigyou_summary.html'),
            (2018, 2017, 'https://www.reconstruction.go.jp/topics/main-cat8/sub-cat8-3/review_h30/rs30page/H30H29jigyou-summery.html'),
            (2018, 2018, 'https://www.reconstruction.go.jp/topics/main-cat8/sub-cat8-3/review_h30/rs30page/H30H30jigyou-summery.html'),
            (2018, 2019, 'https://www.reconstruction.go.jp/topics/main-cat8/sub-cat8-3/review_h30/rs30page/20180912142308.html'),
            (2019, 2018, 'http://www.reconstruction.go.jp/topics/main-cat8/sub-cat8-3/review_r01/rs2019page/2019H30jigyou-summery.html'),
            (2019, 2019, 'http://www.reconstruction.go.jp/topics/main-cat8/sub-cat8-3/review_r01/rs2019page/2019R01jigyou-summery.html'),
            (2019, 2020, 'http://www.reconstruction.go.jp/topics/main-cat8/sub-cat8-3/review_r01/rs2019page/r01r02rs-matome.html'),
            (2020, 2019, 'https://www.reconstruction.go.jp/topics/main-cat8/sub-cat8-3/review_r02/rs2020page/20200811112220.html'),
            (2020, 2020, 'https://www.reconstruction.go.jp/topics/main-cat8/sub-cat8-3/review_r02/rs2020page/20200819172600.html'),
            (2020, 2021, 'https://www.reconstruction.go.jp/topics/main-cat8/sub-cat8-3/review_r02/rs2020page/20201016175247.html'),
        ]
        for y1, y2, url in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'y1': y1, 'y2': y2})

    def parse(self, response):
        if 'child' in response.meta:
            for tr in response.css('tbody tr'):
                if not tr.css('a'):
                    continue
                item = JudgitItem()
                project_number = text_content(
                    tr.css('td:nth-child(1) *::text'))
                if '-' in project_number:
                    n2, n3 = project_number.split('-')
                    item['project_number2'] = id_string(n2)
                    item['project_number3'] = id_string(n3)[2:]
                elif '－' in project_number:
                    n2, n3 = project_number.split('－')
                    item['project_number2'] = id_string(n2)
                    item['project_number3'] = id_string(n3)[2:]
                else:
                    item['project_number2'] = id_string(project_number)
                if response.meta['y2'] >= response.meta['y1']:
                    item['project_number1'] = '新{}'.format(response.meta['y2'])
                url = tr.css('a').attrib['href']
                item['url'] = 'https://www.reconstruction.go.jp' + url
                item['ministry'] = '復興庁'
                name = text_content(tr.css('td:nth-child(2) *::text'))
                item['project_name'] = name
                item['year'] = response.meta['y1']
                yield item
        else:
            for a in response.css('#contents_col2 a'):
                yield scrapy.Request(url='http://www.reconstruction.go.jp' + a.attrib['href'],
                                     callback=self.parse,
                                     meta={'y1': response.meta['y1'], 'y2': response.meta['y2'], 'child': True})
