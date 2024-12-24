from wikibaseintegrator import wbi_helpers


def split_string(string_to_split):
    qid = string_to_split.split('/')
    return (qid[-1])

def execute_query(query_to_exec: str) -> str :
    result = wbi_helpers.execute_sparql_query(query=query_to_exec, endpoint="http://147.231.55.155:8834/proxy/wdqs/bigdata/namespace/wdq/sparql", max_retries=1)
    bindings = result['results']['bindings']

    if len(bindings) > 0:
        wb_url = bindings[0]['item']['value']
        entity_id = split_string(wb_url)
        return entity_id
    else:
        return -1