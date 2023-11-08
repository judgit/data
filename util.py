import json
import os


def project_number(item):
    if '事業番号' in item:
        return item['事業番号']
    return '-'.join([v for v in [item[f'事業番号{i}'] for i in range(1, 6) if f'事業番号{i}' in item] if v])


def project_dest_path(item):
    return 'data/{}/{}/{}.json'.format(item['公開年度'], item['府省庁'], project_number(item))


def write_json(item):
    path = project_dest_path(item)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(item, open(path, 'w'), ensure_ascii=False, indent=2)
