from wikibaseintegrator import WikibaseIntegrator, wbi_login
from wikibaseintegrator.datatypes import Item, Property
from wikibaseintegrator.models import Claim, Snak, Qualifiers, Claims
from wikibaseintegrator.wbi_config import config as wbi_config
import query_handler

general_properties = {"instance_of" : "P1", "title" : "P22", "part_of" : "P29", "inception" : "P9", "dissolved" : "P19", "lang_of_work_or_name" : "P18", "width": "P40", "height" : "P41"}


wbi_config['MEDIAWIKI_API_URL'] = 'http://147.231.55.155/w/api.php'
wbi_config['SPARQL_ENDPOINT_URL'] = 'http://147.231.55.155:8834/proxy/wdqs/bigdata/namespace/wdq/sparql'
wbi_config['WIKIBASE_URL'] = 'http://147.231.55.155'

login_instance = wbi_login.Clientlogin(user="admin", password="2pigsontheroof", mediawiki_api_url="http://147.231.55.155/w/api.php")
wbi = WikibaseIntegrator(login=login_instance)

def get_language_numeric_id(lang): #must be in DB
    lang_numeric_id = 0
    if lang == "cs":
        lang_numeric_id = 20
    elif lang == "fr":
        lang_numeric_id = 47
    elif lang == "de":
        lang_numeric_id = 46
    elif lang == "ru":
        lang_numeric_id = 48
    return lang_numeric_id

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