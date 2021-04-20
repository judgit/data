import re
import scrapy
from judgit.items import JudgitItem
from judgit import id_string, text_content


class JudgitSpider(scrapy.Spider):
    name = 'judgit'

    def start_requests(self):
        urls = [
            (False, '法務省', 'http://www.moj.go.jp/kaikei/bunsho/kaikei03_00091.html', 27, 26),
            (False, '法務省', 'http://www.moj.go.jp/kaikei/bunsho/kaikei03_00109.html', 27, 27),
            (False, '法務省', 'http://www.moj.go.jp/kaikei/bunsho/kaikei03_00091b.html', 28, 27),
            (False, '法務省', 'http://www.moj.go.jp/kaikei/bunsho/kaikei03_00080d.html', 28, 28),
            (False, '法務省', 'http://www.moj.go.jp/kaikei/bunsho/kaikei03_00104.html', 29, 28),
            (False, '法務省', 'http://www.moj.go.jp/kaikei/bunsho/kaikei03_00106.html', 29, 30),
            (False, '法務省', 'http://www.moj.go.jp/kaikei/bunsho/kaikei11_04488.html', 30, 29),
            (False, '法務省', 'http://www.moj.go.jp/kaikei/bunsho/kaikei11_04487.html', 30, 30),
            (False, '法務省', 'http://www.moj.go.jp/kaikei/bunsho/kaikei11_04486.html', 30, 31),
            (False, '法務省', 'http://www.moj.go.jp/kaikei/bunsho/kaikei03_00127.html', 31, 30),
            (False, '法務省', 'http://www.moj.go.jp/kaikei/bunsho/kaikei03_00124.html', 31, 31),
            (False, '法務省', 'http://www.moj.go.jp/kaikei/bunsho/kaikei03_00032.html', 32, 31),
            (False, '法務省', 'http://www.moj.go.jp/kaikei/bunsho/kaikei03_00033.html', 32, 32),
            (True, '外務省', 'https://www.mofa.go.jp/mofaj/ms/fa/page22_002218.html', 27, 26),
            (True, '外務省', 'https://www.mofa.go.jp/mofaj/ms/fa/page22_002236.html', 27, 27),
            (True, '外務省', 'https://www.mofa.go.jp/mofaj/ms/fa/page22_002250.html', 27, 28),
            (True, '外務省', 'https://www.mofa.go.jp/mofaj/ms/fa/page24_000760.html', 28, 27),
            (True, '外務省', 'https://www.mofa.go.jp/mofaj/ms/fa/page24_000780.html', 28, 28),
            (True, '外務省', 'https://www.mofa.go.jp/mofaj/ms/fa/page22_002693.html', 28, 29),
            (True, '外務省', 'https://www.mofa.go.jp/mofaj/ms/fa/page25_000965.html', 29, 28),
            (True, '外務省', 'https://www.mofa.go.jp/mofaj/ms/fa/page25_000966.html', 29, 29),
            (True, '外務省', 'https://www.mofa.go.jp/mofaj/ms/fa/page25_000967.html', 29, 30),
            (True, '外務省', 'https://www.mofa.go.jp/mofaj/ms/fa/page25_001555.html', 30, 29),
            (True, '外務省', 'https://www.mofa.go.jp/mofaj/ms/fa/page25_001556.html', 30, 30),
            (True, '外務省', 'https://www.mofa.go.jp/mofaj/ms/fa/page25_001596.html', 30, 31),
            (True, '外務省', 'https://www.mofa.go.jp/mofaj/ms/fa/page23_003069.html', 31, 30),
            (True, '外務省', 'https://www.mofa.go.jp/mofaj/ms/fa/page23_003088.html', 31, 31),
            (True, '外務省', 'https://www.mofa.go.jp/mofaj/ms/fa/page25_001978.html', 31, 32),
            (True, '外務省', 'https://www.mofa.go.jp/mofaj/ms/fa/page22_003411.html', 32, 31),
            (True, '外務省', 'https://www.mofa.go.jp/mofaj/ms/fa/page22_003443.html', 32, 32),
            (True, '外務省', 'https://www.mofa.go.jp/mofaj/ms/fa/page22_003445.html', 32, 33),
            (False, '財務省', 'https://www.mof.go.jp/about_mof/mof_budget/review/2015/saishu/2014reviewsaishukohyo.htm', 27, 26),
            (False, '財務省', 'https://www.mof.go.jp/about_mof/mof_budget/review/2015/saishu/saishu_28_shinki.htm', 27, 28),
            (False, '財務省', 'https://www.mof.go.jp/about_mof/mof_budget/review/2015reviewsaishukohyo.htm', 28, 27),
            (False, '財務省', 'https://www.mof.go.jp/about_mof/mof_budget/review/2016shinki_saishukohyo.html', 28, 28),
            (False, '財務省', 'https://www.mof.go.jp/about_mof/mof_budget/review/saishu_29_shinki.htm', 28, 29),
            (False, '財務省', 'https://www.mof.go.jp/about_mof/mof_budget/review/2016reviewsaishukohyo.html', 29, 28),
            (False, '財務省', 'https://www.mof.go.jp/about_mof/mof_budget/review/2017shinki_saishukohyo.html', 29, 29),
            (False, '財務省', 'https://www.mof.go.jp/about_mof/mof_budget/review/2017reviewsaishukohyo.html', 30, 29),
            (False, '財務省', 'https://www.mof.go.jp/about_mof/mof_budget/review/2018shinki_saishukohyo.html', 30, 30),
            (False, '財務省', 'https://www.mof.go.jp/about_mof/mof_budget/review/saishu_31_shinki.html', 30, 31),
            (False, '財務省', 'https://www.mof.go.jp/about_mof/mof_budget/review/2018review_saishukohyo.html', 31, 30),
            (False, '財務省', 'https://www.mof.go.jp/about_mof/mof_budget/review/2019shinki_saishukohyo.html', 31, 31),
            (False, '財務省', 'https://www.mof.go.jp/about_mof/mof_budget/review/saishu_2_shinki.html', 31, 32),
            (False, '財務省', 'https://www.mof.go.jp/about_mof/mof_budget/review/2019review_saishukohyo.html', 32, 31),
            (False, '財務省', 'https://www.mof.go.jp/about_mof/mof_budget/review/2020shinki_saishukohyo.html', 32, 32),
            (False, '財務省', 'https://www.mof.go.jp/about_mof/mof_budget/review/saishu_3_shinki.html', 32, 33),
            (True, '文部科学省', 'http://www.mext.go.jp/a_menu/kouritsu/detail/1361566.htm', 27, 26),
            (True, '文部科学省', 'http://www.mext.go.jp/a_menu/kouritsu/detail/1361618.htm', 27, 27),
            (True, '文部科学省', 'http://www.mext.go.jp/a_menu/kouritsu/detail/1361964.htm', 27, 28),
            (True, '文部科学省', 'http://www.mext.go.jp/a_menu/kouritsu/detail/1375111.htm', 28, 27),
            (True, '文部科学省', 'http://www.mext.go.jp/a_menu/kouritsu/detail/1376487.htm', 28, 28),
            (True, '文部科学省', 'http://www.mext.go.jp/a_menu/kouritsu/detail/1375590.htm', 28, 29),
            (True, '文部科学省', 'http://www.mext.go.jp/a_menu/kouritsu/detail/1388832.htm', 29, 28),
            (True, '文部科学省', 'http://www.mext.go.jp/a_menu/kouritsu/detail/1388896.htm', 29, 29),
            (True, '文部科学省', 'http://www.mext.go.jp/a_menu/kouritsu/detail/1395932.htm', 29, 30),
            (True, '文部科学省', 'http://www.mext.go.jp/a_menu/kouritsu/detail/1405376.htm', 30, 29),
            (False, '文部科学省', 'http://www.mext.go.jp/a_menu/kouritsu/detail/1405341.htm', 30, 29),
            (True, '文部科学省', 'http://www.mext.go.jp/a_menu/kouritsu/detail/1405378.htm', 30, 30),
            (True, '文部科学省', 'http://www.mext.go.jp/a_menu/kouritsu/detail/1408920.htm', 30, 31),
            (True, '文部科学省', 'http://www.mext.go.jp/a_menu/kouritsu/detail/1419388.htm', 31, 30),
            (True, '文部科学省', 'http://www.mext.go.jp/a_menu/kouritsu/detail/1419522.htm', 31, 31),
            (True, '文部科学省', 'http://www.mext.go.jp/a_menu/kouritsu/detail/1421137.htm', 31, 32),
            (True, '文部科学省', 'https://www.mext.go.jp/a_menu/kouritsu/detail/block30_00005.htm', 32, 31),
            (True, '文部科学省', 'https://www.mext.go.jp/a_menu/kouritsu/detail/block30_00006.htm', 32, 32),
            (True, '文部科学省', 'https://www.mext.go.jp/a_menu/kouritsu/detail/block30_00007.htm', 32, 33),
            (True, '厚生労働省', 'https://www.mhlw.go.jp/jigyo_shiwake/gyousei_review_sheet/2015/h26_saisyu.html', 27, 26),
            (True, '厚生労働省', 'https://www.mhlw.go.jp/jigyo_shiwake/gyousei_review_sheet/2015/h27_saisyu.html', 27, 27),
            (True, '厚生労働省', 'https://www.mhlw.go.jp/jigyo_shiwake/gyousei_review_sheet/2015/h28_saisyu.html', 27, 28),
            (True, '厚生労働省', 'https://www.mhlw.go.jp/jigyo_shiwake/gyousei_review_sheet/2016/h27_saisyu.html', 28, 27),
            (True, '厚生労働省', 'https://www.mhlw.go.jp/jigyo_shiwake/gyousei_review_sheet/2016/h28_saisyu.html', 28, 28),
            (True, '厚生労働省', 'https://www.mhlw.go.jp/jigyo_shiwake/gyousei_review_sheet/2016/h29_saisyu.html', 28, 29),
            (True, '厚生労働省', 'https://www.mhlw.go.jp/jigyo_shiwake/gyousei_review_sheet/2017/h28_saisyu.html', 29, 28),
            (True, '厚生労働省', 'https://www.mhlw.go.jp/jigyo_shiwake/gyousei_review_sheet/2017/h29_saisyu.html', 29, 29),
            (True, '厚生労働省', 'https://www.mhlw.go.jp/jigyo_shiwake/gyousei_review_sheet/2017/h30_saisyu.html', 29, 30),
            (True, '厚生労働省', 'https://www.mhlw.go.jp/jigyo_shiwake/gyousei_review_sheet/2018/h29_saisyu.html', 30, 29),
            (True, '厚生労働省', 'https://www.mhlw.go.jp/jigyo_shiwake/gyousei_review_sheet/2018/h30_saisyu.html', 30, 30),
            (True, '厚生労働省', 'https://www.mhlw.go.jp/jigyo_shiwake/gyousei_review_sheet/2018/h31_saisyu.html', 30, 31),
            (True, '厚生労働省', 'https://www.mhlw.go.jp/jigyo_shiwake/gyousei_review_sheet/2019/h30_saisyu.html', 31, 30),
            (True, '厚生労働省', 'https://www.mhlw.go.jp/jigyo_shiwake/gyousei_review_sheet/2019/2019_saisyu.html', 31, 31),
            (True, '厚生労働省', 'https://www.mhlw.go.jp/jigyo_shiwake/gyousei_review_sheet/2019/2020_saisyu.html', 31, 32),
            (True, '厚生労働省', 'https://www.mhlw.go.jp/jigyo_shiwake/gyousei_review_sheet/2020/2019_saisyu.html', 32, 31),
            (True, '厚生労働省', 'https://www.mhlw.go.jp/jigyo_shiwake/gyousei_review_sheet/2020/2020_saisyu.html', 32, 32),
            (True, '厚生労働省', 'https://www.mhlw.go.jp/jigyo_shiwake/gyousei_review_sheet/2020/2021_saisyu.html', 32, 33),
            (True, '農林水産省', 'http://www.maff.go.jp/j/budget/review/h27/27syukei.html', 27, 26),
            (False, '農林水産省', 'http://www.maff.go.jp/j/budget/review/h27/27itiran_syu.html', 27, 27),
            (False, '農林水産省', 'http://www.maff.go.jp/j/budget/review/h27/28sinki.html', 27, 28),
            (True, '農林水産省', 'http://www.maff.go.jp/j/budget/review/h28/28syukei.html', 28, 27),
            (False, '農林水産省', 'http://www.maff.go.jp/j/budget/review/h28/28itiran_syu.html', 28, 28),
            (False, '農林水産省', 'http://www.maff.go.jp/j/budget/review/h28/29sinki.html', 28, 29),
            (True, '農林水産省', 'http://www.maff.go.jp/j/budget/review/h29/review/bunya/28itiran_saisyu.html', 29, 28),
            (False, '農林水産省', 'http://www.maff.go.jp/j/budget/review/h29/review/bunya/29_sinnki_saisyu.html', 29, 29),
            (False, '農林水産省', 'http://www.maff.go.jp/j/budget/review/h29/review/bunya/30_sinnki.html', 29, 30),
            (True, '農林水産省', 'http://www.maff.go.jp/j/budget/review/h30/saisyu/h29saisyu.html', 30, 29),
            (False, '農林水産省', 'http://www.maff.go.jp/j/budget/review/h30/saisyu/30_sinki_s.html', 30, 30),
            (False, '農林水産省', 'http://www.maff.go.jp/j/budget/review/h30/saisyu/31_sinki_n.html', 30, 31),
            (True, '農林水産省', 'http://www.maff.go.jp/j/budget/review/h31/30s.html', 31, 30),
            (False, '農林水産省', 'http://www.maff.go.jp/j/budget/review/h31/31s.html', 31, 31),
            (False, '農林水産省', 'http://www.maff.go.jp/j/budget/review/h31/2s.html', 31, 32),
            (False, '農林水産省', 'https://www.maff.go.jp/j/budget/review/R2/01f.html', 32, 31),
            (False, '農林水産省', 'https://www.maff.go.jp/j/budget/review/R2/02f.html', 32, 32),
            (False, '農林水産省', 'https://www.maff.go.jp/j/budget/review/R2/03f.html', 32, 33),
            (False, '経済産業省', 'http://www.meti.go.jp/information_2/publicoffer/review2015/1-1saisyu.html', 27, 26),
            (False, '経済産業省', 'http://www.meti.go.jp/information_2/publicoffer/review2015/1-2saisyu.html', 27, 26),
            (False, '経済産業省', 'http://www.meti.go.jp/information_2/publicoffer/review2015/1-3saisyu.html', 27, 26),
            (False, '経済産業省', 'http://www.meti.go.jp/information_2/publicoffer/review2015/1-4saisyu.html', 27, 26),
            (False, '経済産業省', 'http://www.meti.go.jp/information_2/publicoffer/review2015/1-5saisyu.html', 27, 26),
            (False, '経済産業省', 'http://www.meti.go.jp/information_2/publicoffer/review2015/1-6saisyu.html', 27, 26),
            (False, '経済産業省', 'http://www.meti.go.jp/information_2/publicoffer/review2015/1-7saisyu.html', 27, 26),
            (False, '経済産業省', 'http://www.meti.go.jp/information_2/publicoffer/review2015/2saisyu.html', 27, 27),
            (False, '経済産業省', 'http://www.meti.go.jp/information_2/publicoffer/review2015/3saisyu.html', 27, 28),
            (False, '経済産業省', 'http://www.meti.go.jp/information_2/publicoffer/review2016/saishu/1-1saishu.html', 28, 27),
            (False, '経済産業省', 'http://www.meti.go.jp/information_2/publicoffer/review2016/saishu/1-2saishu.html', 28, 27),
            (False, '経済産業省', 'http://www.meti.go.jp/information_2/publicoffer/review2016/saishu/1-3saishu.html', 28, 27),
            (False, '経済産業省', 'http://www.meti.go.jp/information_2/publicoffer/review2016/saishu/1-4saishu.html', 28, 27),
            (False, '経済産業省', 'http://www.meti.go.jp/information_2/publicoffer/review2016/saishu/1-5saishu.html', 28, 27),
            (False, '経済産業省', 'http://www.meti.go.jp/information_2/publicoffer/review2016/saishu/1-6saishu.html', 28, 27),
            (False, '経済産業省', 'http://www.meti.go.jp/information_2/publicoffer/review2016/saishu/1-7saishu.html', 28, 27),
            (False, '経済産業省', 'http://www.meti.go.jp/information_2/publicoffer/review2016/saishu/2-1saishu.html', 28, 28),
            (False, '経済産業省', 'http://www.meti.go.jp/information_2/publicoffer/review2016/saishu/2-2saishu.html', 28, 28),
            (False, '経済産業省', 'http://www.meti.go.jp/information_2/publicoffer/review2016/saishu/2-3saishu.html', 28, 28),
            (False, '経済産業省', 'http://www.meti.go.jp/information_2/publicoffer/review2016/saishu/2-4saishu.html', 28, 28),
            (False, '経済産業省', 'http://www.meti.go.jp/information_2/publicoffer/review2016/saishu/2-5saishu.html', 28, 28),
            (False, '経済産業省', 'http://www.meti.go.jp/information_2/publicoffer/review2016/saishu/2-6saishu.html', 28, 28),
            (False, '経済産業省', 'http://www.meti.go.jp/information_2/publicoffer/review2016/saishu/2-7saishu.html', 28, 28),
            (False, '経済産業省', 'http://www.meti.go.jp/information_2/publicoffer/review2016/saishu/3-1saishu.html', 28, 29),
            (False, '経済産業省', 'http://www.meti.go.jp/information_2/publicoffer/review2016/saishu/3-2saishu.html', 28, 29),
            (False, '経済産業省', 'http://www.meti.go.jp/information_2/publicoffer/review2016/saishu/3-3saishu.html', 28, 29),
            (False, '経済産業省', 'http://www.meti.go.jp/information_2/publicoffer/review2016/saishu/3-4saishu.html', 28, 29),
            (False, '経済産業省', 'http://www.meti.go.jp/information_2/publicoffer/review2016/saishu/3-5saishu.html', 28, 29),
            (False, '経済産業省', 'http://www.meti.go.jp/information_2/publicoffer/review2016/saishu/3-6saishu.html', 28, 29),
            (False, '経済産業省', 'http://www.meti.go.jp/information_2/publicoffer/review2016/saishu/segment.html  ', 28, 27),
            (False, '経済産業省', 'http://www.meti.go.jp/information_2/publicoffer/review2017/saishu/1-1saishu.html', 29, 28),
            (False, '経済産業省', 'http://www.meti.go.jp/information_2/publicoffer/review2017/saishu/1-2saishu.html', 29, 28),
            (False, '経済産業省', 'http://www.meti.go.jp/information_2/publicoffer/review2017/saishu/1-3saishu.html', 29, 28),
            (False, '経済産業省', 'http://www.meti.go.jp/information_2/publicoffer/review2017/saishu/1-4saishu.html', 29, 28),
            (False, '経済産業省', 'http://www.meti.go.jp/information_2/publicoffer/review2017/saishu/1-5saishu.html', 29, 28),
            (False, '経済産業省', 'http://www.meti.go.jp/information_2/publicoffer/review2017/saishu/1-6saishu.html', 29, 28),
            (False, '経済産業省', 'http://www.meti.go.jp/information_2/publicoffer/review2017/saishu/1-7saishu.html', 29, 28),
            (False, '経済産業省', 'http://www.meti.go.jp/information_2/publicoffer/review2017/saishu/2-1saishu.html', 29, 29),
            (False, '経済産業省', 'http://www.meti.go.jp/information_2/publicoffer/review2017/saishu/2-2saishu.html', 29, 29),
            (False, '経済産業省', 'http://www.meti.go.jp/information_2/publicoffer/review2017/saishu/2-3saishu.html', 29, 29),
            (False, '経済産業省', 'http://www.meti.go.jp/information_2/publicoffer/review2017/saishu/2-4saishu.html', 29, 29),
            (False, '経済産業省', 'http://www.meti.go.jp/information_2/publicoffer/review2017/saishu/2-5saishu.html', 29, 29),
            (False, '経済産業省', 'http://www.meti.go.jp/information_2/publicoffer/review2017/saishu/2-6saishu.html', 29, 29),
            (False, '経済産業省', 'http://www.meti.go.jp/information_2/publicoffer/review2017/saishu/2-7saishu.html', 29, 29),
            (False, '経済産業省', 'http://www.meti.go.jp/information_2/publicoffer/review2017/saishu/3-1saishu.html', 29, 30),
            (False, '経済産業省', 'http://www.meti.go.jp/information_2/publicoffer/review2017/saishu/3-2saishu.html', 29, 30),
            (False, '経済産業省', 'http://www.meti.go.jp/information_2/publicoffer/review2017/saishu/3-3saishu.html', 29, 30),
            (False, '経済産業省', 'http://www.meti.go.jp/information_2/publicoffer/review2017/saishu/3-4saishu.html', 29, 30),
            (False, '経済産業省', 'http://www.meti.go.jp/information_2/publicoffer/review2017/saishu/3-5saishu.html', 29, 30),
            (False, '経済産業省', 'http://www.meti.go.jp/information_2/publicoffer/review2017/saishu/3-6saishu.html', 29, 30),
            (False, '経済産業省', 'http://www.meti.go.jp/information_2/publicoffer/review2017/saishu/3-7saishu.html', 29, 30),
            (False, '経済産業省', 'http://www.meti.go.jp/information_2/publicoffer/review2017/saishu/3-8saishu.html', 29, 30),
            (False, '経済産業省', 'http://www.meti.go.jp/information_2/publicoffer/review2017/saishu/segment_saishu.html', 29, 28),
            (False, '経済産業省', 'http://www.meti.go.jp/information_2/publicoffer/review2018/saisyu/1-1saisyu.html', 30, 29),
            (False, '経済産業省', 'http://www.meti.go.jp/information_2/publicoffer/review2018/saisyu/1-2saisyu.html', 30, 29),
            (False, '経済産業省', 'http://www.meti.go.jp/information_2/publicoffer/review2018/saisyu/1-3saisyu.html', 30, 29),
            (False, '経済産業省', 'http://www.meti.go.jp/information_2/publicoffer/review2018/saisyu/1-4saisyu.html', 30, 29),
            (False, '経済産業省', 'http://www.meti.go.jp/information_2/publicoffer/review2018/saisyu/1-5saisyu.html', 30, 29),
            (False, '経済産業省', 'http://www.meti.go.jp/information_2/publicoffer/review2018/saisyu/1-6saisyu.html', 30, 29),
            (False, '経済産業省', 'http://www.meti.go.jp/information_2/publicoffer/review2018/saisyu/1-7saisyu.html', 30, 29),
            (False, '経済産業省', 'http://www.meti.go.jp/information_2/publicoffer/review2018/saisyu/1-8saisyu.html', 30, 29),
            (False, '経済産業省', 'http://www.meti.go.jp/information_2/publicoffer/review2018/saisyu/2-1saisyu.html', 30, 30),
            (False, '経済産業省', 'http://www.meti.go.jp/information_2/publicoffer/review2018/saisyu/2-2saisyu.html', 30, 30),
            (False, '経済産業省', 'http://www.meti.go.jp/information_2/publicoffer/review2018/saisyu/2-3saisyu.html', 30, 30),
            (False, '経済産業省', 'http://www.meti.go.jp/information_2/publicoffer/review2018/saisyu/2-4saisyu.html', 30, 30),
            (False, '経済産業省', 'http://www.meti.go.jp/information_2/publicoffer/review2018/saisyu/2-5saisyu.html', 30, 30),
            (False, '経済産業省', 'http://www.meti.go.jp/information_2/publicoffer/review2018/saisyu/2-6saisyu.html', 30, 30),
            (False, '経済産業省', 'http://www.meti.go.jp/information_2/publicoffer/review2018/saisyu/2-7saisyu.html', 30, 30),
            (False, '経済産業省', 'http://www.meti.go.jp/information_2/publicoffer/review2018/saisyu/2-8saisyu.html', 30, 30),
            (False, '経済産業省', 'http://www.meti.go.jp/information_2/publicoffer/review2018/saisyu/saisyu.html', 30, 31),
            (False, '経済産業省', 'http://www.meti.go.jp/information_2/publicoffer/review2018/saisyu/segment_saisyu.html', 30, 29),
            (False, '経済産業省', 'https://www.meti.go.jp/information_2/publicoffer/review2019/saisyu/1-1saisyu.html', 31, 30),
            (False, '経済産業省', 'https://www.meti.go.jp/information_2/publicoffer/review2019/saisyu/1-2saisyu.html', 31, 30),
            (False, '経済産業省', 'https://www.meti.go.jp/information_2/publicoffer/review2019/saisyu/1-3saisyu.html', 31, 30),
            (False, '経済産業省', 'https://www.meti.go.jp/information_2/publicoffer/review2019/saisyu/1-4saisyu.html', 31, 30),
            (False, '経済産業省', 'https://www.meti.go.jp/information_2/publicoffer/review2019/saisyu/1-5saisyu.html', 31, 30),
            (False, '経済産業省', 'https://www.meti.go.jp/information_2/publicoffer/review2019/saisyu/1-6saisyu.html', 31, 30),
            (False, '経済産業省', 'https://www.meti.go.jp/information_2/publicoffer/review2019/saisyu/1-7saisyu.html', 31, 30),
            (False, '経済産業省', 'https://www.meti.go.jp/information_2/publicoffer/review2019/saisyu/1-8saisyu.html', 31, 30),
            (False, '経済産業省', 'https://www.meti.go.jp/information_2/publicoffer/review2019/saisyu/2-1saisyu.html', 31, 31),
            (False, '経済産業省', 'https://www.meti.go.jp/information_2/publicoffer/review2019/saisyu/2-2saisyu.html', 31, 31),
            (False, '経済産業省', 'https://www.meti.go.jp/information_2/publicoffer/review2019/saisyu/2-3saisyu.html', 31, 31),
            (False, '経済産業省', 'https://www.meti.go.jp/information_2/publicoffer/review2019/saisyu/2-4saisyu.html', 31, 31),
            (False, '経済産業省', 'https://www.meti.go.jp/information_2/publicoffer/review2019/saisyu/2-5saisyu.html', 31, 31),
            (False, '経済産業省', 'https://www.meti.go.jp/information_2/publicoffer/review2019/saisyu/2-6saisyu.html', 31, 31),
            (False, '経済産業省', 'https://www.meti.go.jp/information_2/publicoffer/review2019/saisyu/2-7saisyu.html', 31, 31),
            (False, '経済産業省', 'https://www.meti.go.jp/information_2/publicoffer/review2019/saisyu/2-8saisyu.html', 31, 31),
            (False, '経済産業省', 'https://www.meti.go.jp/information_2/publicoffer/review2019/saisyu/3saisyu.html', 31, 32),
            (False, '経済産業省', 'https://www.meti.go.jp/information_2/publicoffer/review2020/saisyu/1-1saisyu.html', 32, 31),
            (False, '経済産業省', 'https://www.meti.go.jp/information_2/publicoffer/review2020/saisyu/1-2saisyu.html', 32, 31),
            (False, '経済産業省', 'https://www.meti.go.jp/information_2/publicoffer/review2020/saisyu/1-3saisyu.html', 32, 31),
            (False, '経済産業省', 'https://www.meti.go.jp/information_2/publicoffer/review2020/saisyu/1-4saisyu.html', 32, 31),
            (False, '経済産業省', 'https://www.meti.go.jp/information_2/publicoffer/review2020/saisyu/1-5saisyu.html', 32, 31),
            (False, '経済産業省', 'https://www.meti.go.jp/information_2/publicoffer/review2020/saisyu/1-6saisyu.html', 32, 31),
            (False, '経済産業省', 'https://www.meti.go.jp/information_2/publicoffer/review2020/saisyu/1-7saisyu.html', 32, 31),
            (False, '経済産業省', 'https://www.meti.go.jp/information_2/publicoffer/review2020/saisyu/1-8saisyu.html', 32, 31),
            (False, '経済産業省', 'https://www.meti.go.jp/information_2/publicoffer/review2020/saisyu/2-1saisyu.html', 32, 32),
            (False, '経済産業省', 'https://www.meti.go.jp/information_2/publicoffer/review2020/saisyu/2-2saisyu.html', 32, 32),
            (False, '経済産業省', 'https://www.meti.go.jp/information_2/publicoffer/review2020/saisyu/2-3saisyu.html', 32, 32),
            (False, '経済産業省', 'https://www.meti.go.jp/information_2/publicoffer/review2020/saisyu/2-4saisyu.html', 32, 32),
            (False, '経済産業省', 'https://www.meti.go.jp/information_2/publicoffer/review2020/saisyu/2-5saisyu.html', 32, 32),
            (False, '経済産業省', 'https://www.meti.go.jp/information_2/publicoffer/review2020/saisyu/2-6saisyu.html', 32, 32),
            (False, '経済産業省', 'https://www.meti.go.jp/information_2/publicoffer/review2020/saisyu/2-7saisyu.html', 32, 32),
            (False, '経済産業省', 'https://www.meti.go.jp/information_2/publicoffer/review2020/saisyu/2-8saisyu.html', 32, 32),
            (False, '経済産業省', 'https://www.meti.go.jp/information_2/publicoffer/review2020/saisyu/3saisyu.html', 32, 33),
            (True, '国土交通省', 'http://www.mlit.go.jp/page/kanbo05_hy_001060.html', 27, 26),
            (True, '国土交通省', 'http://www.mlit.go.jp/page/kanbo05_hy_001061.html', 27, 27),
            (True, '国土交通省', 'http://www.mlit.go.jp/page/kanbo05_hy_001063.html', 27, 28),
            (True, '国土交通省', 'http://www.mlit.go.jp/page/kanbo05_hy_001283.html', 28, 27),
            (True, '国土交通省', 'http://www.mlit.go.jp/page/kanbo05_hy_001284.html', 28, 28),
            (True, '国土交通省', 'http://www.mlit.go.jp/page/kanbo05_hy_001285.html', 28, 29),
            (True, '国土交通省', 'http://www.mlit.go.jp/page/kanbo05_hy_001412.html', 29, 28),
            (True, '国土交通省', 'http://www.mlit.go.jp/page/kanbo05_hy_001413.html', 29, 29),
            (True, '国土交通省', 'http://www.mlit.go.jp/page/kanbo05_hy_001480.html', 29, 30),
            (True, '国土交通省', 'http://www.mlit.go.jp/page/kanbo05_hy_001635.html', 30, 29),
            (True, '国土交通省', 'http://www.mlit.go.jp/page/kanbo05_hy_001636.html', 30, 30),
            (True, '国土交通省', 'http://www.mlit.go.jp/page/kanbo05_hy_001721.html', 30, 31),
            (True, '国土交通省', 'http://www.mlit.go.jp/page/kanbo05_hy_001856.html', 31, 30),
            (True, '国土交通省', 'http://www.mlit.go.jp/page/kanbo05_hy_001922.html', 31, 31),
            (True, '国土交通省', 'http://www.mlit.go.jp/page/kanbo05_hy_001923.html', 31, 32),
            (True, '国土交通省', 'https://www.mlit.go.jp/page/kanbo05_hy_002158.html', 32, 31),
            (True, '国土交通省', 'https://www.mlit.go.jp/page/kanbo05_hy_002159.html', 32, 32),
            (True, '国土交通省', 'https://www.mlit.go.jp/page/kanbo05_hy_002185.html', 32, 33),
            (True, '環境省', 'https://www.env.go.jp/guide/budget/spv_eff/review_h27/sheets_h26f.html', 27, 26),
            (True, '環境省', 'https://www.env.go.jp/guide/budget/spv_eff/review_h27/sheets_h27f.html', 27, 27),
            (True, '環境省', 'https://www.env.go.jp/guide/budget/spv_eff/review_h27/sheets_h28f.html', 27, 28),
            (True, '環境省', 'https://www.env.go.jp/guide/budget/spv_eff/review_h28/sheets_h27f.html', 28, 27),
            (True, '環境省', 'https://www.env.go.jp/guide/budget/spv_eff/review_h28/sheets_h28f.html', 28, 28),
            (True, '環境省', 'https://www.env.go.jp/guide/budget/spv_eff/review_h28/sheets_h29.html', 28, 29),
            (True, '環境省', 'https://www.env.go.jp/guide/budget/spv_eff/review_h29/sheets_h28f.html', 29, 28),
            (True, '環境省', 'https://www.env.go.jp/guide/budget/spv_eff/review_h29/sheets_h29f.html', 29, 29),
            (True, '環境省', 'https://www.env.go.jp/guide/budget/spv_eff/review_h29/sheets_h30.html', 29, 30),
            (True, '環境省', 'https://www.env.go.jp/guide/budget/spv_eff/review_h30/sheets_h29f.html', 30, 29),
            (True, '環境省', 'https://www.env.go.jp/guide/budget/spv_eff/review_h30/sheets_h30f.html', 30, 30),
            (True, '環境省', 'https://www.env.go.jp/guide/budget/spv_eff/review_h30/sheets_h31.html', 30, 31),
            (True, '環境省', 'https://www.env.go.jp/guide/budget/review/2019/sheets/h30_f/sheets.html', 31, 30),
            (True, '環境省', 'https://www.env.go.jp/guide/budget/review/2019/sheets/h31_f/sheets.html', 31, 31),
            (True, '環境省', 'https://www.env.go.jp/guide/budget/review/2019/sheets/r02/sheets.html', 31, 32),
            (True, '環境省', 'https://www.env.go.jp/guide/budget/review/2020/sheets/h31_f/sheets.html', 32, 31),
            (True, '環境省', 'https://www.env.go.jp/guide/budget/review/2020/sheets/r02_f/sheets.html', 32, 32),
            (True, '環境省', 'https://www.env.go.jp/guide/budget/review/2020/sheets/r03/sheets.html', 32, 33),
            (False, '原子力規制委員会', 'https://www.nsr.go.jp/nra/seisakujikkou/budget/h27_jigyou/saisyu/h26sheet/sesaku1.html', 27, 26),
            (False, '原子力規制委員会', 'https://www.nsr.go.jp/nra/seisakujikkou/budget/h27_jigyou/saisyu/h26sheet/sesaku2.html', 27, 26),
            (False, '原子力規制委員会', 'https://www.nsr.go.jp/nra/seisakujikkou/budget/h27_jigyou/saisyu/h26sheet/sesaku3.html', 27, 26),
            (False, '原子力規制委員会', 'https://www.nsr.go.jp/nra/seisakujikkou/budget/h27_jigyou/saisyu/h26sheet/sesaku4.html', 27, 26),
            (False, '原子力規制委員会', 'https://www.nsr.go.jp/nra/seisakujikkou/budget/h27_jigyou/saisyu/h26sheet/sesaku5.html', 27, 26),
            (False, '原子力規制委員会', 'https://www.nsr.go.jp/nra/seisakujikkou/budget/h27_jigyou/saisyu/h26sheet/sesaku6.html', 27, 26),
            (False, '原子力規制委員会', 'https://www.nsr.go.jp/nra/seisakujikkou/budget/h27_jigyou/saisyu/h27sheet/sesaku4.html', 27, 27),
            (False, '原子力規制委員会', 'https://www.nsr.go.jp/nra/seisakujikkou/budget/h27_jigyou/saisyu/h28sheet/sesaku4.html', 27, 28),
            (False, '原子力規制委員会', 'https://www.nsr.go.jp/nra/seisakujikkou/budget/h27_jigyou/saisyu/h28sheet/sesaku6.html', 27, 28),
            (False, '原子力規制委員会', 'https://www.nsr.go.jp/nra/seisakujikkou/budget/h28_jigyou/h27saisyu1.html', 28, 27),
            (False, '原子力規制委員会', 'https://www.nsr.go.jp/nra/seisakujikkou/budget/h28_jigyou/h27saisyu2.html', 28, 27),
            (False, '原子力規制委員会', 'https://www.nsr.go.jp/nra/seisakujikkou/budget/h28_jigyou/h27saisyu3.html', 28, 27),
            (False, '原子力規制委員会', 'https://www.nsr.go.jp/nra/seisakujikkou/budget/h28_jigyou/h27saisyu4.html', 28, 27),
            (False, '原子力規制委員会', 'https://www.nsr.go.jp/nra/seisakujikkou/budget/h28_jigyou/h27saisyu5.html', 28, 27),
            (False, '原子力規制委員会', 'https://www.nsr.go.jp/nra/seisakujikkou/budget/h28_jigyou/h27saisyu6.html', 28, 27),
            (False, '原子力規制委員会', 'https://www.nsr.go.jp/nra/seisakujikkou/budget/h28_jigyou/h28startsaisyu4.html', 28, 28),
            (False, '原子力規制委員会', 'https://www.nsr.go.jp/nra/seisakujikkou/budget/h28_jigyou/h28startsaisyu5.html', 28, 28),
            (False, '原子力規制委員会', 'https://www.nsr.go.jp/nra/seisakujikkou/budget/h29_jigyou/h28saisyu1.html', 29, 28),
            (False, '原子力規制委員会', 'https://www.nsr.go.jp/nra/seisakujikkou/budget/h29_jigyou/h28saisyu2.html', 29, 28),
            (False, '原子力規制委員会', 'https://www.nsr.go.jp/nra/seisakujikkou/budget/h29_jigyou/h28saisyu3.html', 29, 28),
            (False, '原子力規制委員会', 'https://www.nsr.go.jp/nra/seisakujikkou/budget/h29_jigyou/h28saisyu4.html', 29, 28),
            (False, '原子力規制委員会', 'https://www.nsr.go.jp/nra/seisakujikkou/budget/h29_jigyou/h28saisyu5.html', 29, 28),
            (False, '原子力規制委員会', 'https://www.nsr.go.jp/nra/seisakujikkou/budget/h29_jigyou/h28saisyu6.html', 29, 28),
            (False, '原子力規制委員会', 'https://www.nsr.go.jp/nra/seisakujikkou/budget/h29_jigyou/h29startsaisyu4.html', 29, 30),
            (False, '原子力規制委員会', 'https://www.nsr.go.jp/nra/seisakujikkou/budget/h30_jigyou/h29saisyu1.html', 30, 29),
            (False, '原子力規制委員会', 'https://www.nsr.go.jp/nra/seisakujikkou/budget/h30_jigyou/h29saisyu2.html', 30, 29),
            (False, '原子力規制委員会', 'https://www.nsr.go.jp/nra/seisakujikkou/budget/h30_jigyou/h29saisyu3.html', 30, 29),
            (False, '原子力規制委員会', 'https://www.nsr.go.jp/nra/seisakujikkou/budget/h30_jigyou/h29saisyu4.html', 30, 29),
            (False, '原子力規制委員会', 'https://www.nsr.go.jp/nra/seisakujikkou/budget/h30_jigyou/h29saisyu5.html', 30, 29),
            (False, '原子力規制委員会', 'https://www.nsr.go.jp/nra/seisakujikkou/budget/h30_jigyou/h29saisyu6.html', 30, 29),
            (False, '原子力規制委員会', 'https://www.nsr.go.jp/nra/seisakujikkou/budget/h30_jigyou/h30saisyu2.html', 30, 30),
            (False, '原子力規制委員会', 'https://www.nsr.go.jp/nra/seisakujikkou/budget/h30_jigyou/h31startsaisyu2.html', 30, 31),
            (False, '原子力規制委員会', 'https://www.nsr.go.jp/nra/seisakujikkou/budget/h30_jigyou/h31startsaisyu4.html', 30, 31),
            (False, '原子力規制委員会', 'https://www.nsr.go.jp/nra/seisakujikkou/budget/h31_jigyou/h30saisyu1.html', 31, 30),
            (False, '原子力規制委員会', 'https://www.nsr.go.jp/nra/seisakujikkou/budget/h31_jigyou/h30saisyu2.html', 31, 30),
            (False, '原子力規制委員会', 'https://www.nsr.go.jp/nra/seisakujikkou/budget/h31_jigyou/h30saisyu3.html', 31, 30),
            (False, '原子力規制委員会', 'https://www.nsr.go.jp/nra/seisakujikkou/budget/h31_jigyou/h30saisyu4.html', 31, 30),
            (False, '原子力規制委員会', 'https://www.nsr.go.jp/nra/seisakujikkou/budget/h31_jigyou/h30saisyu5.html', 31, 30),
            (False, '原子力規制委員会', 'https://www.nsr.go.jp/nra/seisakujikkou/budget/h31_jigyou/h30saisyu6.html', 31, 30),
            (False, '原子力規制委員会', 'https://www.nsr.go.jp/nra/seisakujikkou/budget/h31_jigyou/r1startedsaisyu4.html', 31, 31),
            (False, '原子力規制委員会', 'https://www.nsr.go.jp/nra/seisakujikkou/budget/h31_jigyou/r2startsaisyu4.html', 31, 32),
            (False, '原子力規制委員会', 'https://www.nsr.go.jp/nra/seisakujikkou/budget/2020_jigyou/2019saisyu1.html', 32, 31),
            (False, '原子力規制委員会', 'https://www.nsr.go.jp/nra/seisakujikkou/budget/2020_jigyou/2019saisyu2.html', 32, 31),
            (False, '原子力規制委員会', 'https://www.nsr.go.jp/nra/seisakujikkou/budget/2020_jigyou/2019saisyu3.html', 32, 31),
            (False, '原子力規制委員会', 'https://www.nsr.go.jp/nra/seisakujikkou/budget/2020_jigyou/2019saisyu4.html', 32, 31),
            (False, '原子力規制委員会', 'https://www.nsr.go.jp/nra/seisakujikkou/budget/2020_jigyou/2019saisyu5.html', 32, 31),
            (False, '原子力規制委員会', 'https://www.nsr.go.jp/nra/seisakujikkou/budget/2020_jigyou/2019saisyu6.html', 32, 31),
            (False, '原子力規制委員会', 'https://www.nsr.go.jp/nra/seisakujikkou/budget/2020_jigyou/r2startedsaisyu4.html', 32, 32),
            (False, '原子力規制委員会', 'https://www.nsr.go.jp/nra/seisakujikkou/budget/2020_jigyou/r3startsaisyu4.html', 32, 33),
        ]
        for f, m, url, y1, y2 in urls:
            meta = {
                'ministry': m,
                'report_year': y1,
                'target_year': y2,
            }
            yield scrapy.Request(url=url, meta=meta,
                                 callback=self.parse_list if f else self.parse)

    def parse_list(self, response):
        for a in self.find_links(response):
            yield response.follow(url=a.attrib['href'],
                                  callback=self.parse,
                                  meta=response.meta)

    def parse(self, response):
        ministry = response.meta['ministry']
        report_year = response.meta['report_year']
        target_year = response.meta['target_year']
        year = report_year + 1988
        for tr in self.find_rows(response):
            item = JudgitItem()
            project_number = self.find_project_number(response, tr)
            n1, n2, n3 = self.parse_project_number(response, project_number)
            if n1:
                item['project_number1'] = n1
            if n2:
                item['project_number2'] = id_string(n2)
            if n3:
                item['project_number3'] = n3
            item['url'] = self.find_url(response, tr)
            item['project_name'] = self.find_project_name(response, tr)
            item['ministry'] = ministry
            item['year'] = year
            yield item

    def find_links(self, response):
        ministry = response.meta['ministry']
        selectors = {
            '外務省': '#section1 > div > div > ul > li > a',
            '文部科学省': '#contentsMain > div > ul > li > a',
            '厚生労働省': '#contentsInner a',
            '農林水産省': '#main_content a',
            '国土交通省': '#contents a',
            '環境省': '#main-body > table > tbody > tr > td > a',
            '防衛省': '#schedule a',
        }
        for a in response.css(selectors[ministry]):
            if ministry == '農林水産省':
                href = a.attrib['href']
                if not (href.startswith('http://www.maff.go.jp') or href.startswith('./')):
                    continue
            if ministry == '国土交通省':
                ignore = [
                    '  22 国際競争力・地域の自立等を強化する道路ネットワークを形成する（再掲のみ）',
                    '）',
                    '21 景観に優れた国土・観光地づくりを推進する（新32-032）',
                ]
                if text_content(a.css('*::text')) in ignore:
                    continue
            yield a

    def find_rows(self, response):
        ministry = response.meta['ministry']
        report_year = response.meta['report_year']
        target_year = response.meta['target_year']
        if ministry == '法務省':
            for tr in response.css('#content > div.section01 > table > tbody > tr'):
                if tr.css('a') and tr.css('td::text').get().strip():
                    yield tr
        if ministry == '外務省':
            for tr in response.css('#section1 > div > div > table > tbody > tr'):
                if tr.css('td::text'):
                    yield tr
        if ministry == '財務省':
            for tr in response.css('#main-base > table > tbody > tr'):
                yield tr
        if ministry == '文部科学省':
            for a in response.css('#contentsMain > div.bottom20 > ul > li > a'):
                if a.attrib['href'].endswith('.xlsx') and re.match(r'^\d{4}', text_content(a.css('*::text'))):
                    yield a
        if ministry == '厚生労働省':
            for tr in response.css('#contentsInner > div > div > div > div > div > table > tbody > tr'):
                yield tr
        if ministry == '農林水産省':
            for tr in response.css('#main_content table > tbody > tr'):
                head = tr.css('td *::text').get().strip()
                if head and not head.endswith('業番号'):
                    yield tr
            for a in response.css('#main_content ul > li > a'):
                text = text_content(a.css('*::text'))
                if re.match(r'^\d{4}', text) or text.startswith('新'):
                    yield a
        if ministry == '経済産業省':
            for a in response.css('#__main_contents > ul > li > a'):
                text = text_content(a.css('*::text'))
                if text.startswith('一括ダウンロード'):
                    continue
                yield a
        if ministry == '国土交通省':
            for a in response.css('#contents a'):
                text = text_content(a.css('*::text'))
                if text.startswith('一括ダウンロード'):
                    continue
                if text.endswith('【PDF形式】'):
                    continue
                if text.startswith('【'):
                    continue
                if text == '政策評価事前分析表】':
                    continue
                if text.startswith('（'):
                    continue
                if text.startswith('水管理・国土保全局'):
                    continue
                if text == '土地・建設産業局）':
                    continue
                if text == '）':
                    continue
                if text == '050':
                    continue
                if text == '051':
                    continue
                if text == '238':
                    continue
                if text == '334':
                    continue
                if not text.strip():
                    continue
                yield a
        if ministry == '環境省':
            for tr in response.css('#main-body > table > tbody > tr'):
                if len(tr.css('td').getall()) <= 1:
                    continue
                head = text_content(tr.css('td:nth-child(1) *::text')).strip()
                if not head:
                    continue
                yield tr
        if ministry == '原子力規制委員会':
            for tr in response.css('#main table > tbody > tr'):
                if len(tr.css('td').getall()) == 0:
                    continue
                yield tr
        if ministry == '防衛省':
            for tr in response.css('#schedule tr'):
                if len(tr.css('td').getall()) == 0:
                    continue
                yield tr

    def find_project_number(self, response, row):
        ministry = response.meta['ministry']
        report_year = response.meta['report_year']
        target_year = response.meta['target_year']
        if ministry in {'法務省', '外務省', '環境省', '防衛省'}:
            return text_content(row.css('td:nth-child(1) *::text'))
        if ministry in {'財務省', '厚生労働省', '原子力規制委員会'}:
            return text_content(row.css('th:nth-child(1) *::text'))
        if ministry in {'農林水産省'} and report_year == 28:
            return text_content(row.css('td:nth-child(1) *::text'))
        if ministry in {'文部科学省', '農林水産省', '経済産業省'}:
            text = text_content(row.css('*::text'))
            if ministry in {'農林水産省', '経済産業省'} and target_year >= report_year:
                return text[:8]
            return text[:4]
        if ministry in {'国土交通省'}:
            text = text_content(row.css('*::text'))
            if text.startswith('新29-020'):
                return '新29-020'
            if text == '水資源開発事業':
                return '050'
            if text == '世界的水資源問題を踏まえた我が国の対応方策検討調査経費':
                return '051'
            if text == '349建設分野における外国人受入れの円滑化及び適正化（土地・建設産業局）':
                return '349'
            if text == '350建設業における女性活躍の推進（土地・建設産業局）':
                return '350'
            if text == '095気候・海洋情報処理業務（気象庁）':
                return '095'
            if text == '222北東アジア港湾局長会議等に必要な経費（港湾局）':
                return '222'
            if text == '宿泊施設における生産性向上（観光庁）':
                return '238'
            if text == '主要都市における高度利用地の地価分析調査（土地・建設産業局）':
                return '334'
            return text.split()[0]

    def parse_project_number(self, response, project_number):
        report_year = response.meta['report_year']
        target_year = response.meta['target_year']
        if target_year >= report_year:
            for s in ['-', '‐', 'ー', '－']:
                if s in project_number:
                    ns = project_number.split(s)
                    if len(ns) == 2:
                        n1, n2 = ns
                        return (n1, n2, None)
                    return ns
            return ('新{}'.format(target_year), project_number, None)
        else:
            if '-' in project_number:
                n2, n3 = project_number.split('-')
                return (None, n2, n3)
            else:
                return (None, project_number, None)

    def find_url(self, response, row):
        ministry = response.meta['ministry']
        report_year = response.meta['report_year']
        target_year = response.meta['target_year']
        if ministry in {'法務省', '外務省', '財務省', '厚生労働省', '環境省', '原子力規制委員会', '防衛省'}:
            return response.urljoin(row.css('a').attrib['href'])
        if ministry == '農林水産省' and report_year == 28:
            return response.urljoin(row.css('a').attrib['href'])
        if ministry in {'文部科学省', '農林水産省', '経済産業省', '国土交通省'}:
            return response.urljoin(row.attrib['href'])

    def find_project_name(self, response, row):
        ministry = response.meta['ministry']
        report_year = response.meta['report_year']
        target_year = response.meta['target_year']
        if ministry in {'法務省', '外務省', '財務省', '厚生労働省', '防衛省'}:
            return text_content(row.css('td:nth-child(2) *::text'))
        if ministry == '農林水産省' and report_year == 28:
            return text_content(row.css('td:nth-child(2) *::text'))
        if ministry in {'文部科学省'}:
            text = text_content(row.css('*::text'))
            m = re.match(r'^(\d{4})(.+)（.+）', text)
            return m[2].strip()
        if ministry in {'農林水産省', '経済産業省'}:
            text = text_content(row.css('*::text'))
            if report_year >= 32:
                return text.split()[1]
            elif target_year >= report_year:
                m = re.match(r'^(新\d{2}-\d{4}):?(.+)[(（].+[)）]', text)
            elif not text.endswith('）'):
                return text.split()[1]
            else:
                m = re.match(r'^(\d{3,4}):?(.+)[(（].+[)）]', text)
            return m[2].strip()
        if ministry in {'国土交通省'}:
            text = text_content(row.css('*::text'))
            if text.startswith('新29-020'):
                return '公共事業評価の効率的・効果的な実施等に関する調査検討経費'
            if text == '水資源開発事業':
                return '水資源開発事業'
            if text == '世界的水資源問題を踏まえた我が国の対応方策検討調査経費':
                return '世界的水資源問題を踏まえた我が国の対応方策検討調査経費'
            if text == '349建設分野における外国人受入れの円滑化及び適正化（土地・建設産業局）':
                return '建設分野における外国人受入れの円滑化及び適正化'
            if text == '350建設業における女性活躍の推進（土地・建設産業局）':
                return '建設業における女性活躍の推進'
            if text == '02':
                return '総合的なバリアフリー社会の形成の推進'
            if text == '095気候・海洋情報処理業務（気象庁）':
                return '気候・海洋情報処理業務'
            if text == '212 内航海運の効率化に必要な経費（海事局）':
                return '内航海運の効率化に必要な経費'
            if text == '214 港湾整備事業（港湾局）':
                return '港湾整備事業'
            if text == '222北東アジア港湾局長会議等に必要な経費（港湾局）':
                return '北東アジア港湾局長会議等に必要な経費'
            if text == '宿泊施設における生産性向上（観光庁）':
                return '宿泊施設における生産性向上'
            if text == '主要都市における高度利用地の地価分析調査（土地・建設産業局）':
                return '主要都市における高度利用地の地価分析調査'
            return text.split()[1]
        if ministry in {'環境省', '原子力規制委員会'}:
            return text_content(row.css('a::text')).split('[Excel')[0]
