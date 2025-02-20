from wikibaseintegrator import wbi_helpers


def split_string(string_to_split):
    qid = string_to_split.split('/')
    return (qid[-1])

def execute_query(query_to_exec: str) -> str :
    result = wbi_helpers.execute_sparql_query(query=query_to_exec, endpoint="http://147.231.55.155:8834/proxy/wdqs/bigdata/namespace/wdq/sparql", max_retries=1)
    bindings = result['results']['bindings']

    if len(bindings) > 0:
        wb_url = bindings[0]['item']['value']
        entity_id = split_string(wb_url).split('-')[0]
        return entity_id
    else:
        return -1

def execute_query_get_multiple_results(query_to_exec: str) -> list[str]:
    result = wbi_helpers.execute_sparql_query(query=query_to_exec, endpoint="http://147.231.55.155:8834/proxy/wdqs/bigdata/namespace/wdq/sparql", max_retries=1)
    bindings = result['results']['bindings']
    result_list = []

    for i in  range(len(bindings)):
        wb_url = bindings[i]['item']['value']
        entity_id = split_string(wb_url).split('-')[0]
        result_list.append(entity_id)

    return result_list


# res = execute_query_get_multiple_results('SELECT ?item WHERE { ?item ?label "Ebru (attributed)"@en .}')

# print(res)