import argparse
import csv
import json
import os


def convert_era(v, era):
    if v is None:
        return None
    offset = {
        '昭和': 1925,
        '平成': 1988,
    }
    return int(v) + offset[era]


def to_year(s):
    if s.startswith('①'):
        s = s[1:]
    ignore = {
        '昭和元年度以前',
        '不明',
        '終了予定なし',
        '',
    }
    digits = {
        '元': '1',
        '0': '0',
        '1': '1',
        '2': '2',
        '3': '3',
        '4': '4',
        '5': '5',
        '6': '6',
        '7': '7',
        '8': '8',
        '9': '9',
        '０': '0',
        '１': '1',
        '２': '2',
        '３': '3',
        '４': '4',
        '５': '5',
        '６': '6',
        '７': '7',
        '８': '8',
        '９': '9',
    }
    if s in ignore:
        return None
    era = int(''.join(digits[c] for c in s if c in digits))
    return convert_era(era, s[:2])


def or_none(s, default=None):
    if s in ['-', '―', '－', '　', '', '記入不要']:
        return default
    return str(s).strip()


def first(s):
    a = s.split()
    if a:
        return a[0]
    return ''


def try_float(s):
    try:
        return float(s)
    except ValueError:
        return None


def load_projects_ja(base_year, inpath):
    base_era = base_year - 1988
    data = csv.reader(open(inpath))
    header = next(data)
    indices = {h: [i for i, h2 in enumerate(header) if h == h2] for h in header}

    for i, item in enumerate(data):
        row = {h: item[ix[0]] if len(ix) == 1 else [item[i] for i in ix] for h, ix in indices.items()}
        obj = {}
        obj['公開年度'] = base_year
        obj['事業名'] = row['事業名'].strip()
        if not obj['事業名']:
            continue
        if '事業開始年度' in row:
            obj['開始年度'] = to_year(row['事業開始年度'])
            obj['終了年度'] = to_year(row['事業終了（予定）年度'])
        if '府省庁' in row:
            obj['府省庁'] = row['府省庁']
        elif '府省' in row:
            obj['府省庁'] = row['府省']
        if obj['府省庁'] == '特定個人情報保護委員会':
            obj['府省庁'] = '個人情報保護委員会'
        if '事業番号-1' in row:
            obj['事業番号1'] = or_none(row['事業番号-1'])
            obj['事業番号2'] = or_none(row['事業番号-2'])
            obj['事業番号3'] = or_none(row['事業番号-3'])
        else:
            obj['事業番号2'] = or_none(row['事業番号'])
        obj['事業番号2'] = '{:04}'.format(int(obj['事業番号2']))
        if obj['事業番号3'] == '0':
            obj['事業番号3'] = None
        obj['担当部局庁'] = or_none(row['担当部局庁'])
        obj['担当課室'] = or_none(row['担当課室'])
        obj['作成責任者'] = or_none(row['作成責任者'])
        obj['会計区分'] = [s for s in row['会計区分'].split('、') if s]
        if '事業の目的（目指す姿を簡潔に。3行程度以内）' in row:
            obj['事業目的'] = row['事業の目的（目指す姿を簡潔に。3行程度以内）']
        elif '事業の目的' in row:
            obj['事業目的'] = row['事業の目的']
        if '事業概要（5行程度以内。別添可）' in row:
            obj['事業概要'] = row['事業概要（5行程度以内。別添可）']
        elif '事業概要' in row:
            obj['事業概要'] = row['事業概要']
        obj['実施方法'] = [s for s in row['実施方法'].replace('，', '、').split('、') if s]
        if '主要政策・施策' in row:
            obj['主要施策'] = or_none(row['主要政策・施策'], 'その他').split('、')
        elif '主要施策' in row:
            obj['主要施策'] = or_none(row['主要施策'], 'その他').split('、')
        obj['予算'] = [
            {
                '年度': base_year - 3,
                '当初予算': float(or_none(row['予算額・執行額（単位:百万円）-{}年度-予算の状況-当初予算'.format(base_era - 3)], 0)),
                '補正予算': float(or_none(row['予算額・執行額（単位:百万円）-{}年度-予算の状況-補正予算'.format(base_era - 3)], 0)),
                '前年度から繰越し': float(or_none(row['予算額・執行額（単位:百万円）-{}年度-予算の状況-前年度から繰越し'.format(base_era - 3)], 0)),
                '翌年度へ繰越し': float(or_none(row['予算額・執行額（単位:百万円）-{}年度-予算の状況-翌年度へ繰越し'.format(base_era - 3)], 0)),
                '予備費等': float(or_none(row['予算額・執行額（単位:百万円）-{}年度-予算の状況-予備費等'.format(base_era - 3)], 0)),
                '予算計': float(or_none(row['予算額・執行額（単位:百万円）-{}年度-予算の状況-計'.format(base_era - 3)], 0)),
                '執行額': float(or_none(row['予算額・執行額（単位:百万円）-{}年度-執行額'.format(base_era - 3)], 0)),
            },
            {
                '年度': base_year - 2,
                '当初予算': float(or_none(row['予算額・執行額（単位:百万円）-{}年度-予算の状況-当初予算'.format(base_era - 2)], 0)),
                '補正予算': float(or_none(row['予算額・執行額（単位:百万円）-{}年度-予算の状況-補正予算'.format(base_era - 2)], 0)),
                '前年度から繰越し': float(or_none(row['予算額・執行額（単位:百万円）-{}年度-予算の状況-前年度から繰越し'.format(base_era - 2)], 0)),
                '翌年度へ繰越し': float(or_none(row['予算額・執行額（単位:百万円）-{}年度-予算の状況-翌年度へ繰越し'.format(base_era - 2)], 0)),
                '予備費等': float(or_none(row['予算額・執行額（単位:百万円）-{}年度-予算の状況-予備費等'.format(base_era - 2)], 0)),
                '予算計': float(or_none(row['予算額・執行額（単位:百万円）-{}年度-予算の状況-計'.format(base_era - 2)], 0)),
                '執行額': float(or_none(row['予算額・執行額（単位:百万円）-{}年度-執行額'.format(base_era - 2)], 0)),
            },
            {
                '年度': base_year - 1,
                '当初予算': float(or_none(row['予算額・執行額（単位:百万円）-{}年度-予算の状況-当初予算'.format(base_era - 1)], 0)),
                '補正予算': float(or_none(row['予算額・執行額（単位:百万円）-{}年度-予算の状況-補正予算'.format(base_era - 1)], 0)),
                '前年度から繰越し': float(or_none(row['予算額・執行額（単位:百万円）-{}年度-予算の状況-前年度から繰越し'.format(base_era - 1)], 0)),
                '翌年度へ繰越し': float(or_none(row['予算額・執行額（単位:百万円）-{}年度-予算の状況-翌年度へ繰越し'.format(base_era - 1)], 0)),
                '予備費等': float(or_none(row['予算額・執行額（単位:百万円）-{}年度-予算の状況-予備費等'.format(base_era - 1)], 0)),
                '予算計': float(or_none(row['予算額・執行額（単位:百万円）-{}年度-予算の状況-計'.format(base_era - 1)], 0)),
                '執行額': float(or_none(row['予算額・執行額（単位:百万円）-{}年度-執行額'.format(base_era - 1)], 0)),
            },
            {
                '年度': base_year,
                '当初予算': float(or_none(row['予算額・執行額（単位:百万円）-{}年度-予算の状況-当初予算'.format(base_era)], 0)),
                '補正予算': float(or_none(row['予算額・執行額（単位:百万円）-{}年度-予算の状況-補正予算'.format(base_era)], 0)),
                '前年度から繰越し': float(or_none(row['予算額・執行額（単位:百万円）-{}年度-予算の状況-前年度から繰越し'.format(base_era)], 0)),
                '翌年度へ繰越し': float(or_none(row['予算額・執行額（単位:百万円）-{}年度-予算の状況-翌年度へ繰越し'.format(base_era)], 0)),
                '予備費等': float(or_none(row['予算額・執行額（単位:百万円）-{}年度-予算の状況-予備費等'.format(base_era)], 0)),
                '予算計': float(or_none(row['予算額・執行額（単位:百万円）-{}年度-予算の状況-計'.format(base_era)], 0)),
            },
            {
                '年度': base_year + 1,
                '要求額': float(or_none(row['予算額・執行額（単位:百万円）-{}年度要求-予算の状況-計'.format(base_era + 1)], 0)),
            },
        ]
        payee = []
        for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuv':
            for n in range(1, 31):
                if not or_none(row['支出先上位１０者リスト-{}.支払先-{}-支出先'.format(c, n)]):
                    continue
                payee.append({
                    '年度': base_year - 1,
                    'グループ': c,
                    '番号': n,
                    '支出先名': row['支出先上位１０者リスト-{}.支払先-{}-支出先'.format(c, n)],
                    '法人番号': or_none(row['支出先上位１０者リスト-{}.支払先-{}-法人番号'.format(c, n)]) if '支出先上位１０者リスト-{}.支払先-{}-法人番号'.format(c, n) in row else None,
                    '業務概要': row['支出先上位１０者リスト-{}.支払先-{}-業務概要'.format(c, n)],
                    '支出額': float(or_none(row['支出先上位１０者リスト-{}.支払先-{}-支出額（百万円）'.format(c, n)].replace('¥', ''), 0)),
                })
        obj['支出先'] = payee

        obj['アウトカム'] = [
            {
                '成果目標': row['成果目標及び成果実績（アウトカム）-定量的な成果目標'][i],
                '成果指標': row['成果目標及び成果実績（アウトカム）-成果指標'][i],
                '単位': row['成果目標及び成果実績（アウトカム）-単位-成果実績'][i],
                '目標値': or_none(row['成果目標及び成果実績（アウトカム）-目標最終年度-目標値'][i]),
                '目標最終年度': convert_era(or_none(row['成果目標及び成果実績（アウトカム）-目標最終年度-年度'][i]), '平成'),
                '成果実績': [
                    {
                        '年度': base_year - 3,
                        '成果実績': try_float(row['成果目標及び成果実績（アウトカム）-{}年度-成果実績'.format(base_era - 3)][i]),
                        '目標値': try_float(row['成果目標及び成果実績（アウトカム）-{}年度-目標値'.format(base_era - 3)][i]),
                    },
                    {
                        '年度': base_year - 2,
                        '成果実績': try_float(row['成果目標及び成果実績（アウトカム）-{}年度-成果実績'.format(base_era - 2)][i]),
                        '目標値': try_float(row['成果目標及び成果実績（アウトカム）-{}年度-目標値'.format(base_era - 2)][i]),
                    },
                    {
                        '年度': base_year - 1,
                        '成果実績': try_float(row['成果目標及び成果実績（アウトカム）-{}年度-成果実績'.format(base_era - 1)][i]),
                        '目標値': try_float(row['成果目標及び成果実績（アウトカム）-{}年度-目標値'.format(base_era - 1)][i]),
                    },
                ],

            }
            for i in range(len(row['成果目標及び成果実績（アウトカム）-定量的な成果目標']))
            if or_none(row['成果目標及び成果実績（アウトカム）-定量的な成果目標'][i])
        ]
        obj['定量的な目標が設定できない理由'] = or_none(row['定量的な成果目標の設定が困難な場合-定量的な目標設定ができない理由及び定性的な成果目標-定量的な目標が設定できない理由'])

        obj['アウトプット'] = [
            {
                '活動指標': row['活動指標及び活動実績（アウトプット）-活動指標'][i],
                '単位': row['活動指標及び活動実績（アウトプット）-単位-活動実績'][i],
                '活動実績': [
                    {
                        '年度': base_year - 3,
                        '活動実績': try_float(row['活動指標及び活動実績（アウトプット）-{}年度-活動実績'.format(base_era - 3)][i]),
                        '当初見込み': try_float(row['活動指標及び活動実績（アウトプット）-{}年度-当初見込み'.format(base_era - 3)][i]),
                    },
                    {
                        '年度': base_year - 2,
                        '活動実績': try_float(row['活動指標及び活動実績（アウトプット）-{}年度-活動実績'.format(base_era - 2)][i]),
                        '当初見込み': try_float(row['活動指標及び活動実績（アウトプット）-{}年度-当初見込み'.format(base_era - 2)][i]),
                    },
                    {
                        '年度': base_year - 1,
                        '活動実績': try_float(row['活動指標及び活動実績（アウトプット）-{}年度-活動実績'.format(base_era - 1)][i]),
                        '当初見込み': try_float(row['活動指標及び活動実績（アウトプット）-{}年度-当初見込み'.format(base_era - 1)][i]),
                    },
                ],
            }
            for i in range(len(row['活動指標及び活動実績（アウトプット）-活動指標']))
            if or_none(row['活動指標及び活動実績（アウトプット）-活動指標'][i])
        ]

        yield obj


def load_projects_from_files(paths):
    for path in paths:
        year = int(os.path.basename(path)[8:12])
        print(year)
        for obj in load_projects_ja(year, path):
            yield obj


def project_number(item):
    return '-'.join([v for v in [item['事業番号{}'.format(i)] for i in range(1, 4)] if v])


def project_dest_path(item):
    return 'data/{}/{}/{}.json'.format(item['公開年度'], item['府省庁'], project_number(item))


def copy_rec(src, dst, overwrite):
    if isinstance(src, list):
        keys = range(len(src))
    if isinstance(src, dict):
        keys = src.keys()
    for key in keys:
        if isinstance(src[key], list):
            copy_rec(src[key], dst[key], overwrite)
            continue
        if isinstance(src[key], dict):
            copy_rec(src[key], dst[key], overwrite)
            continue
        if key not in dst or overwrite:
            dst[key] = src[key]


def save_project(project, overwrite):
    path = project_dest_path(project)
    if not os.path.exists(path):
        json.dump(project, open(path, 'w'), ensure_ascii=False, indent=2)
        return
    with open(path) as f:
        dst = json.load(f)
    copy_rec(project, dst, overwrite)
    with open(path, 'w') as f:
        json.dump(dst, f, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(dest='files', nargs='+')
    parser.add_argument('--overwrite-property', dest='overwrite', action='store_true')
    args = parser.parse_args()
    for obj in load_projects_from_files(args.files):
        save_project(obj, args.overwrite)


if __name__ == '__main__':
    main()
