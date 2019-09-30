import json
from glob import glob


def main():
    data = [json.load(open(p)) for p in glob('./data/**/**/*.json')]
    for item in data:
        print(json.dumps(item, ensure_ascii=False))


if __name__ == '__main__':
    main()
