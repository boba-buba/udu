from wikibaseintegrator import wbi_helpers

def query_db(title, entity):
    query = ""
    if entity == "magazine":
        query = 'SELECT ?item WHERE { ?item wdt:P1 wd:Q7; wdt:P22 ?title . FILTER(STR(?title) ="' +  title + '"). SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}'
    elif entity == "volume":
        query = 'SELECT ?item WHERE { ?item wdt:P1 wd:Q10; wdt:P22 ?title . FILTER(STR(?title) ="' +  title + '"). SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}'
    elif entity == "issue":
        query = 'SELECT ?item WHERE { ?item wdt:P1 wd:Q11; wdt:P22 ?title . FILTER(STR(?title) ="' +  title + '"). SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}'
    elif entity == "lang":
        query = 'SELECT ?item WHERE { ?item ?label "' + title +'"@en .}' #must be Czech, French, Russian, German
    elif entity == "page":
        query = 'SELECT ?item WHERE { ?item ?label "' + title +'"@en .}'
    elif entity == "repro":
        query = 'SELECT ?item WHERE { ?item ?label "' + title +'"@en .}'
    elif entity == "caption":
        query = 'SELECT ?item WHERE { ?item ?label "' + title +'"@en .}' # jestli label neni unikatni, je potreba hledat podle textu
    else:
        return -1
    result = execute_query(query)
    return result

def split_string(string_to_split):
    qid = string_to_split.split('/')
    return (qid[-1])

def execute_query(query_to_exec):
    result = wbi_helpers.execute_sparql_query(query=query_to_exec, endpoint="http://147.231.55.155:8834/proxy/wdqs/bigdata/namespace/wdq/sparql", max_retries=1)
    bindings = result['results']['bindings']

    if len(bindings) > 0:
        wb_url = bindings[0]['item']['value']
        entity_id = split_string(wb_url)
        return entity_id
    else:
        return -1


"""
mag = "Volné směry"
print(query_db(mag, "magazine"))
print(query_db(mag + ", Vol. XXXVII", "volume"))
print(query_db(mag+", ročník XXXVII, číslo 1", "issue"))
print(query_db("Independent directions, vol. XXXVII, issue 1", "issue"))
print(query_db("mag", "magazine"))
print(query_db(mag, "issue"))
print(query_db(mag, "page"))#"""

#print(query_db("Czech", "lang"))