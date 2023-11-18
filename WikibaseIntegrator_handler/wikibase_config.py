from wikibaseintegrator.wbi_config import config as wbi_config

def configure_wb():
    wbi_config['MEDIAWIKI_API_URL'] = 'http://147.231.55.155/w/api.php'
    wbi_config['SPARQL_ENDPOINT_URL'] = 'http://147.231.55.155:8834/proxy/wdqs/bigdata/namespace/wdq/sparql'
    wbi_config['WIKIBASE_URL'] = 'http://147.231.55.155'