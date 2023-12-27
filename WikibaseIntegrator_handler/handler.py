from wikibaseintegrator import WikibaseIntegrator, wbi_login
from wikibaseintegrator.datatypes import Item, Property
from wikibaseintegrator.models import Claim, Snak, Qualifiers
from wikibaseintegrator.wbi_config import config as wbi_config
import json

general_properties = {"instance_of" : "P1"}


wbi_config['MEDIAWIKI_API_URL'] = 'http://147.231.55.155/w/api.php'
wbi_config['SPARQL_ENDPOINT_URL'] = 'http://147.231.55.155:8834/proxy/wdqs/bigdata/namespace/wdq/sparql'
wbi_config['WIKIBASE_URL'] = 'http://147.231.55.155'

login_instance = wbi_login.Clientlogin(user="admin", password="2pigsontheroof", mediawiki_api_url="http://147.231.55.155/w/api.php")
wbi = WikibaseIntegrator(login=login_instance)



def get_json_to_file(id):
    with open("wikibase.json", 'w', encoding="utf-8") as f:
        f.write(json.dumps(get_item(id).get_json()))
        f.flush()


def get_item(id):
    return wbi.item.get(entity_id=id)

def get_property(id):
    return wbi.property.get(entity_id=id)


#print(get_item("Q27"))
get_json_to_file("Q30")

#Your OAuth consumer has been created.
#Your tokens are:
#Consumer token
#    f89531493fffb686fd6c08d2f13060b8
#Consumer secret
#    3c5605812084a82738b74244ffd8cfcbb8e7d664
#Access token
#    b03cc1860432e8e23cfd6cdc90e87ef3
#Access secret
#    fddebff0f2eb3baaa2b47d7cb54ce82bc03b5739
#Please record these for future reference. 