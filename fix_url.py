import csv
import json
from import_data import project_dest_path, write_json
import os


def main():
    for row in csv.DictReader(open('./urls.csv')):
        path = project_dest_path({
            '公開年度': row['year'],
            '府省庁': row['ministry'],
            '事業番号1': row['project_number1'],
            '事業番号2': row['project_number2'],
            '事業番号3': row['project_number3'],
        })
        if os.path.exists(path):
            obj = json.load(open(path))
            obj['url'] = row['url']
            write_json(obj)


if __name__ == '__main__':
    main()
