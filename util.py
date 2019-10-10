import json
import os


def project_number(item):
    return '-'.join([v for v in [item['事業番号{}'.format(i)] for i in range(1, 4)] if v])


def project_dest_path(item):
    return 'data/{}/{}/{}.json'.format(item['公開年度'], item['府省庁'], project_number(item))


def write_json(item):
    path = project_dest_path(item)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(item, open(path, 'w'), ensure_ascii=False, indent=2)
