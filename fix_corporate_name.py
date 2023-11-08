import csv
import json
from glob import glob
from import_data import write_json


def main():
    corporate_names = {
        row[1]: row[6]
        for row in csv.reader(open('./tmp/00_zenkoku_all_20231031.csv'))
    }
    data = [json.load(open(p)) for p in glob('./data/**/**/*.json')]
    for item in data:
        for payee in item['支出先']:
            cn = payee['法人番号']
            if cn is not None and cn in corporate_names:
                payee['支出先名'] = corporate_names[cn]
        write_json(item)


if __name__ == '__main__':
    main()
