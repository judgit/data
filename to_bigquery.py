from glob import glob
import json


def convert(src):
    dest = {}
    dest['id'] = src['ID']
    dest['project_id'] = src['事業ID']
    dest['url'] = src['url']
    dest['report_year'] = src['公開年度']
    dest['project_name'] = src['事業名']
    dest['start_year'] = src['開始年度']
    dest['end_year'] = src['終了年度']
    dest['ministry'] = src['府省庁']
    dest['project_number1'] = src['事業番号1']
    dest['project_number2'] = src['事業番号2']
    dest['project_number3'] = src['事業番号3']
    dest['bureau'] = src['担当部局庁']
    dest['department'] = src['担当課室']
    dest['author'] = src['作成責任者']
    dest['accounting_category'] = src['会計区分']
    dest['objective'] = src['事業目的']
    dest['summary'] = src['事業概要']
    dest['method'] = src['実施方法']
    dest['categories'] = src['主要施策']
    dest['budget'] = [
        {
            'year': item.get('年度'),
            'original': item.get('当初予算'),
            'supplementary': item.get('補正予算'),
            'brought': item.get('前年度から繰越し'),
            'carried': item.get('翌年度へ繰越し'),
            'reserve': item.get('予備費等'),
            'total': item.get('予算計'),
            'executed': item.get('執行額'),
            'request': item.get('要求額'),
        }
        for item in src['予算']
    ]
    dest['payee'] = [
        {
            'year': item['年度'],
            'group': item['グループ'],
            'number': item['番号'],
            'name': item['支出先名'],
            'corporate_number': item['法人番号'],
            'description': item['業務概要'],
            'amount': item['支出額'],
            'primary': False,
        }
        for item in src['支出先']
    ]
    dest['outcome'] = [
        {
            'goal': item['成果目標'],
            'indicator': item['成果指標'],
            'unit': item['単位'],
            'target': str(item['目標値']),
            'target_year': item['目標最終年度'],
            'items': [
                {
                    'year': item2['年度'],
                    'achievement': str(item2['成果実績']),
                    'target': str(item2['目標値']),
                }
                for item2 in item['成果実績']
            ],
        }
        for item in src['アウトカム']
    ]
    dest['outcome_difficulty_reason'] = src.get('定量的な目標が設定できない理由')
    dest['output'] = [
        {
            'indicator': item['活動指標'],
            'unit': item['単位'],
            'items': [
                {
                    'year': item2['年度'],
                    'achievement': str(item2['活動実績']),
                    'expected': str(item2['当初見込み']),
                }
                for item2 in item['活動実績']
            ],
        }
        for item in src['アウトプット']
    ]
    return dest


def main():
    data = [json.load(open(p)) for p in glob('./data/**/**/*.json')]
    for item in data:
        print(json.dumps(convert(item), ensure_ascii=False))


if __name__ == '__main__':
    main()
