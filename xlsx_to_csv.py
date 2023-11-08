import csv
import openpyxl


def rename_column(name):
    if not name:
        return ''
    return name\
        .replace('平成22年度', '2010年度')\
        .replace('平成23年度', '2011年度')\
        .replace('平成24年度', '2012年度')\
        .replace('平成25年度', '2013年度')\
        .replace('平成26年度', '2014年度')\
        .replace('平成27年度', '2015年度')\
        .replace('平成28年度', '2016年度')\
        .replace('平成29年度', '2017年度')\
        .replace('平成30年度', '2018年度')\
        .replace('平成31年度', '2019年度')\
        .replace('令和元年度', '2019年度')\
        .replace('令和2年度', '2020年度')\
        .replace('令和3年度', '2021年度')\
        .replace('令和4年度', '2022年度')\
        .replace('令和5年度', '2023年度')\
        .replace('令和6年度', '2024年度')\
        .replace('令和7年度', '2025年度')\
        .replace('令和8年度', '2026年度')\
        .replace('令和9年度', '2027年度')\
        .replace('-22年度', '-2010年度')\
        .replace('-23年度', '-2011年度')\
        .replace('-24年度', '-2012年度')\
        .replace('-25年度', '-2013年度')\
        .replace('-26年度', '-2014年度')\
        .replace('-27年度', '-2015年度')\
        .replace('-28年度', '-2016年度')\
        .replace('-29年度', '-2017年度')\
        .replace('-30年度', '-2018年度')\
        .replace('-31年度', '-2019年度')\
        .replace('-2年度', '-2020年度')\
        .replace('-3年度', '-2021年度')\
        .replace('-4年度', '-2022年度')\
        .replace('-5年度', '-2023年度')\
        .replace('-6年度', '-2024年度')\
        .replace('-7年度', '-2025年度')\
        .replace('-8年度', '-2026年度')\
        .replace('-9年度', '-2027年度')


def main():
    for y in range(2015, 2024):
        print(y)
        f = open('csv/database{}.csv'.format(y), 'w')
        writer = csv.writer(f)
        wb = openpyxl.load_workbook('original/database{}.xlsx'.format(y))
        sheet = wb[wb.sheetnames[0]]
        rows = sheet.values
        writer.writerow([rename_column(c) for c in next(rows)])
        f.flush()
        for row in rows:
            writer.writerow(list(row))
            f.flush()


if __name__ == '__main__':
    main()
