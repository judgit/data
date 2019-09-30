import json
from glob import glob


def main():
    data = [json.load(open(p)) for p in glob('./data/**/**/*.json')]
    print(json.dumps(data, ensure_ascii=False))


if __name__ == '__main__':
    main()
