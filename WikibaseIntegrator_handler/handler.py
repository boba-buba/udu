from wikibaseintegrator import WikibaseIntegrator, wbi_login
from wikibaseintegrator.datatypes import Item
from wikibaseintegrator.wbi_config import config as wbi_config

wbi_config['MEDIAWIKI_API_URL'] = 'http://147.231.55.155/w/api.php'
wbi_config['SPARQL_ENDPOINT_URL'] = 'http://147.231.55.155:8834/proxy/wdqs/bigdata/namespace/wdq/sparql'
wbi_config['WIKIBASE_URL'] = 'http://147.231.55.155'
"""
login_instance = wbi_login.OAuth1(consumer_token='f89531493fffb686fd6c08d2f13060b8', consumer_secret='3c5605812084a82738b74244ffd8cfcbb8e7d664',
                                  access_token='b03cc1860432e8e23cfd6cdc90e87ef3', access_secret='fddebff0f2eb3baaa2b47d7cb54ce82bc03b5739',
                                  mediawiki_api_url="http://147.231.55.155/w/api.php", mediawiki_index_url="http://147.231.55.155/w/index.php",
                                  callback_url="http://147.231.55.155/wiki/Special:OAuth/verified")#"""

#login_instance.continue_oauth("http://147.231.55.155/wiki/Special:OAuth/verified")
#login_instance = wbi_login.Login(user='Admin@small_bo', password='2c7r9a81orn77qfa3mtuke6thpta4ekc', mediawiki_api_url="http://147.231.55.155/w/api.php")

login_instance = wbi_login.Clientlogin(user="admin", password="2pigsontheroof", mediawiki_api_url="http://147.231.55.155/w/api.php")

#configure_wb()
wbi = WikibaseIntegrator(login=login_instance)


def get_item(id):
    return wbi.item.get(entity_id=id)

def get_property(id):
    return wbi.property.get(entity_id=id)

def insert_item():
    item = wbi.item.new()

    # Set an english label
    item.labels.set(language='en', value='Artwork')

    # Set a English description
    item.descriptions.set(language='en', value='aesthetic item or artistic creation; object whose value is its beauty only, not practical usefulness')
    item.aliases.set(language='en', values=['artwork', 'piece of art', 'art work'])

    #item.write(allow_anonymous=True)
    itemEnt = item.write(login=login_instance)
    print(itemEnt)

insert_item()


def insert_property(property_info):
    return


#print(my_first_wikidata_item.get_json())
#print(my_first_wikidata_property.get_json())
#print(my_first_wikidata_item.get_entity_url())


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