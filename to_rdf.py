import json
from glob import glob
import rdflib
from rdflib.namespace import FOAF


base = 'http://rdf.judgit.net'

ministry_code = {
    '個人情報保護委員会': 'ppc',
    '公正取引委員会': 'jtfc',
    '内閣官房': 'cas',
    '内閣府': 'cao',
    '厚生労働省': 'mhlw',
    '原子力規制委員会': 'nsr',
    '国土交通省': 'mlit',
    '外務省': 'mofa',
    '復興庁': 'reconstruction',
    '文部科学省': 'mext',
    '法務省': 'moj',
    '消費者庁': 'caa',
    '環境省': 'env',
    '経済産業省': 'meti',
    '総務省': 'mic',
    '警察庁': 'npa',
    '財務省': 'mof',
    '農林水産省': 'maff',
    '金融庁': 'fsa',
    '防衛省': 'mod',
}


def project_number(item):
    nums = []
    if item['事業番号1']:
        nums.append('n' + item['事業番号1'][1:])
    if item['事業番号2']:
        nums.append(item['事業番号2'])
    if item['事業番号3']:
        nums.append(item['事業番号3'])
    return '-'.join(nums)


def project_uri(project):
    return rdflib.URIRef('{}/project/{}/{}/{}'.format(base, project['公開年度'], ministry_code[project['府省庁']], project_number(project)))


def ministry_uri(ministry):
    return rdflib.URIRef('{}/ministry/{}'.format(base, ministry_code[ministry]))


def pay_uri(project, payee):
    return rdflib.URIRef('{}/pay/{}/{}/{}/{}/{}'.format(base, project['公開年度'], ministry_code[project['府省庁']], project_number(project), payee['グループ'], payee['番号']))


def payee_uri(payee):
    if not payee['法人番号']:
        return None
    return rdflib.URIRef('{}/payee/{}'.format(base, payee['法人番号']))


def budget_uri(project, budget):
    return rdflib.URIRef('{}/budget/{}/{}/{}/{}'.format(base, project['公開年度'], ministry_code[project['府省庁']], project_number(project), budget['年度']))


def outcome_uri(project, i):
    return rdflib.URIRef('{}/outcome/{}/{}/{}/{}'.format(base, project['公開年度'], ministry_code[project['府省庁']], project_number(project), i))


def outcome_achievement_uri(project, i, outcome):
    return rdflib.URIRef('{}/outcome_achievement/{}/{}/{}/{}/{}'.format(base, project['公開年度'], ministry_code[project['府省庁']], project_number(project), i, outcome['年度']))


def output_uri(project, i):
    return rdflib.URIRef('{}/output/{}/{}/{}/{}'.format(base, project['公開年度'], ministry_code[project['府省庁']], project_number(project), i))


def output_achievement_uri(project, i, output):
    return rdflib.URIRef('{}/output_achievement/{}/{}/{}/{}/{}'.format(base, project['公開年度'], ministry_code[project['府省庁']], project_number(project), i, output['年度']))


def property_uri(property):
    return rdflib.URIRef('{}/property/{}'.format(base, property))


def add_project(graph, data):
    project = project_uri(data)

    project_properties = [
        ('publish_year', '公開年度'),
        ('start_year', '開始年度'),
        ('end_year', '終了年度'),
        ('project_number1', '事業番号1'),
        ('project_number2', '事業番号2'),
        ('project_number3', '事業番号3'),
        ('bureau', '担当部局庁'),
        ('department', '担当課室'),
        ('author', '作成責任者'),
        ('objective', '事業目的'),
        ('overview', '事業概要'),
        ('outcome_difficulty_reason', '定量的な目標が設定できない理由'),
        ('original_url', 'url'),
    ]
    for property_name, key in project_properties:
        if data[key] is not None:
            graph.add((project, property_uri(property_name), rdflib.Literal(data[key])))

    project_list_properties = [
        ('accounting_category', '会計区分'),
        ('implementation_method', '実施方法'),
        ('policy_category', '主要施策'),
    ]
    for property_name, key in project_list_properties:
        for value in data[key]:
            graph.add((project, property_uri(property_name), rdflib.Literal(value)))

    budget_properties = [
        ('year', '年度'),
        ('request', '要求額'),
        ('original', '当初予算'),
        ('supplementary', '補正予算'),
        ('brought', '前年度から繰越し'),
        ('carried', '翌年度へ繰越し'),
        ('reserved', '予備費等'),
        ('total', '予算計'),
        ('executed', '執行額'),
    ]
    for item in data['予算']:
        budget = budget_uri(data, item)
        graph.add((project, property_uri('budget'), budget))
        for property_name, key in budget_properties:
            if key in item:
                graph.add((budget, property_uri(property_name), rdflib.Literal(item[key])))

    pay_properties = [
        ('year', '年度'),
        ('group', 'グループ'),
        ('number', '番号'),
        ('overview', '業務概要'),
        ('amount', '支出額'),
        ('payee_name', '支出先名'),
    ]
    for item in data['支出先']:
        pay = pay_uri(data, item)
        graph.add((pay, property_uri('project'), project))
        for property_name, key in pay_properties:
            graph.add((pay, property_uri(property_name), rdflib.Literal(item[key])))

        payee = payee_uri(item)
        if payee:
            graph.add((pay, property_uri('payee'), payee))
            graph.add((payee, FOAF.name, rdflib.Literal(item['支出先名'])))
            graph.add((payee, property_uri('corporate_number'), rdflib.Literal(item['法人番号'])))

    outcome_properties = [
        ('goal', '成果目標'),
        ('indicator', '成果指標'),
        ('unit', '単位'),
        ('target', '目標値'),
        ('target_year', '目標最終年度'),
    ]
    outcome_achievement_properties = [
        ('year', '年度'),
        ('amount', '成果実績'),
        ('target', '目標値'),
    ]
    for i, item in enumerate(data['アウトカム']):
        outcome = outcome_uri(data, i + 1)
        graph.add((project, property_uri('outcome'), outcome))
        for property_name, key in outcome_properties:
            if key in item and item[key] is not None:
                graph.add((outcome, property_uri(property_name), rdflib.Literal(item[key])))
        for item2 in item['成果実績']:
            outcome_achievement = outcome_achievement_uri(data, i + 1, item2)
            graph.add((outcome, property_uri('achievement'), outcome_achievement))
            for property_name, key in outcome_achievement_properties:
                if key in item2 and item2[key] is not None:
                    graph.add((outcome_achievement, property_uri(property_name), rdflib.Literal(item2[key])))

    output_properties = [
        ('indicator', '活動指標'),
        ('unit', '単位'),
    ]
    output_achievement_properties = [
        ('year', '年度'),
        ('amount', '活動実績'),
        ('expected', '目標値'),
    ]
    for i, item in enumerate(data['アウトプット']):
        output = output_uri(data, i + 1)
        graph.add((project, property_uri('output'), output))
        for property_name, key in output_properties:
            if key in item and item[key] is not None:
                graph.add((output, property_uri(property_name), rdflib.Literal(item[key])))
        for item2 in item['活動実績']:
            output_achievement = output_achievement_uri(data, i + 1, item2)
            graph.add((output, property_uri('achievement'), output_achievement))
            for property_name, key in output_achievement_properties:
                if key in item2 and item2[key] is not None:
                    graph.add((output_achievement, property_uri(property_name), rdflib.Literal(item2[key])))

    graph.add((project, FOAF.name, rdflib.Literal(data['事業名'])))
    graph.add((project, property_uri('ministry'), ministry_uri(data['府省庁'])))


def main():
    data = [json.load(open(p)) for p in glob('./data/**/**/*.json')]
    graph = rdflib.Graph()
    for item in data:
        add_project(graph, item)
    print(graph.serialize(format='turtle').decode())


if __name__ == '__main__':
    main()
