import json
from glob import glob
from import_data import write_json


def main():
    data = [json.load(open(p)) for p in glob('./data/**/**/*.json')]
    max_id = max(item['ID'] for item in data if item['ID'] is not None)
    for item in data:
        if item['ID'] is None:
            max_id += 1
            item['ID'] = max_id
            write_json(item)


if __name__ == '__main__':
    main()
