from wikibaseintegrator import WikibaseIntegrator, wbi_login
from wikibaseintegrator.datatypes import Item, Property
from wikibaseintegrator.models import Claim, Snak, Qualifiers
from wikibaseintegrator.wbi_config import config as wbi_config

wbi_config['MEDIAWIKI_API_URL'] = 'http://147.231.55.155/w/api.php'
wbi_config['SPARQL_ENDPOINT_URL'] = 'http://147.231.55.155:8834/proxy/wdqs/bigdata/namespace/wdq/sparql'
wbi_config['WIKIBASE_URL'] = 'http://147.231.55.155'

login_instance = wbi_login.Clientlogin(user="admin", password="2pigsontheroof", mediawiki_api_url="http://147.231.55.155/w/api.php")

wbi = WikibaseIntegrator(login=login_instance)


def get_item(id):
    return wbi.item.get(entity_id=id)

def get_property(id):
    return wbi.property.get(entity_id=id)

def insert_item(): # TODO: udelat obecneji a dodat nejaky format pro vlastnosti
    item = wbi.item.new()

    # Set an english label
    item.labels.set(language='en', value='Artwork')

    # Set a English description
    item.descriptions.set(language='en', value='aesthetic item or artistic creation; object whose value is its beauty only, not practical usefulness')
    item.aliases.set(language='en', values=['artwork', 'piece of art', 'art work'])

    #item.write(allow_anonymous=True)
    itemEnt = item.write(login=login_instance)
    print(itemEnt)

#insert_item()

def update_item(): #potrebuje id a nejaky usporadany format pro vlastnosti

    """
    FUNKCI ZNOVU NEPOUSTET DOKUD NEPREDELAM
    Dodelat ty vlastnosti, asi pro kazdou z nich bude potreba vytvorit pekny format snaku
    Pak by to slo jen vyplnovat
    Zatim mam time, tam lze uvest precision, jestli nevime cele datum,
    Dobry navod k zjisteni foramtu snaku je: zkusit dat statement do wikibase v prohlizeci a potom printnout to zde v jsonu, tam najdu format snaku , aky musi byt.
    """
    item_to_update = wbi.item.get("Q2")
    #April 8, 1973
    new_snak = Snak(property_number="P3", datatype="time", datavalue={ "value" : {"time": "+1973-04-08T00:00:00Z", "timezone": 0, "before": 0, "after": 0, "precision": 11, "calendarmodel": "http://www.wikidata.org/entity/Q1985727"}, "type" : "time"})
    #print(new_snak.get_json())
    claim = Claim()
    claim.mainsnak = new_snak
    #print(claim.get_json())

    item_to_update.add_claims(claim)
    #itemEnt = item_to_update.write(login=login_instance)
    #print(itemEnt.get_json())

#update_item()

def insert_property(property_info): #TODO: to udelat obecneji
    property = wbi.property.new()

    property.labels.set()
    return


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