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
        if '事業番号4' not in item:
            item['事業番号4'] = None
        if '事業番号5' not in item:
            item['事業番号5'] = None
        if '事業番号' not in item:
            item['事業番号'] = '-'.join([item[key] for key in [f'事業番号{i}' for i in range(1, 6)] if item[key]])
        write_json(item)


if __name__ == '__main__':
    main()
