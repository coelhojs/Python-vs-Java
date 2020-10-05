import time
import requests
from datetime import datetime
from queries import queries
from json import dump
from json import loads


def fetch(query, json, headers):
    request = requests.post(
        'https://api.github.com/graphql', json=json, headers=headers)
    if request.status_code == 200:
        return request.json()

    time.sleep(1)

    return fetch(query, json, headers)


def run(query, language, page_limit=10):
    token = ''  # INSERT TOKEN
    headers = {"Authorization": "Bearer " + token}
    query_language = query.replace("{LANG}", language)
    final_query = query_language.replace("{AFTER}", "")
    json = {"query": final_query, "variables": {}}

    total_pages = 1

    result = fetch(query, json, headers)

    nodes = result['data']['search']['nodes']
    next_page = result["data"]["search"]["pageInfo"]["hasNextPage"]

    while (next_page and total_pages < page_limit):
        total_pages += 1
        cursor = result["data"]["search"]["pageInfo"]["endCursor"]
        next_query = query
        json["query"] = next_query.replace(
            "{AFTER}", ", after: \"%s\"" % cursor)
        result = fetch(query, json, headers)
        nodes += result['data']['search']['nodes']
        next_page = result["data"]["search"]["pageInfo"]["hasNextPage"]

    return nodes


def QueryTop100(language_name):
    try:
        query = queries[0]

        nodes = run(query, language_name)

        filename = "Top100" + language_name + ".csv"

        with open(filename, 'a') as the_file:
            the_file.write('nameWithOwner;stargazers;mostUsedLanguage\n')

        for node in nodes:
            if (len(node['languages']['edges']) > 0):
                top_language = node['languages']['edges'][0]['node']['name']
            else:
                top_language = "NA"

            with open(filename, 'a') as the_file:
                the_file.write("%s;%s;%s\n" % (
                    node['nameWithOwner'], node['stargazers']['totalCount'], top_language))
    except Exception as ex:
        print(ex)
        pass


QueryTop100("Java")
QueryTop100("Python")
