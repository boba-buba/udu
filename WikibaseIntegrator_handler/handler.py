from wikibaseintegrator import WikibaseIntegrator, wbi_login
from wikibaseintegrator.datatypes import Item, Property
from wikibaseintegrator.models import Claim, Snak, Qualifiers
from wikibaseintegrator.wbi_config import config as wbi_config

import json

wbi_config['MEDIAWIKI_API_URL'] = 'http://147.231.55.155/w/api.php'
wbi_config['SPARQL_ENDPOINT_URL'] = 'http://147.231.55.155:8834/proxy/wdqs/bigdata/namespace/wdq/sparql'
wbi_config['WIKIBASE_URL'] = 'http://147.231.55.155'

login_instance = wbi_login.Clientlogin(user="admin", password="2pigsontheroof", mediawiki_api_url="http://147.231.55.155/w/api.php")

wbi = WikibaseIntegrator(login=login_instance)


def get_item(id):
    return wbi.item.get(entity_id=id)

def get_property(id):
    return wbi.property.get(entity_id=id)

def insert_new_item(data): # dict
    # minimal format of the data {'label': 'smth', 'description' : 'smth', 'aliases' : ['smth', ...]}
    item = wbi.item.new()

    # Set an english label
    item.labels.set(language='en', value=data['label'])

    # Set a English description
    item.descriptions.set(language='en', value=data['description'])
    item.aliases.set(language='en', values=data['aliases']) #list

    itemEnt = item.write(login=login_instance)
    #print(itemEnt)

def update_item_time_property(item_id, property_id, time_precision, time_formatted):
    # https://www.wikidata.org/wiki/Help:Dates for precision and format

    item_to_update = wbi.item.get(item_id)
    new_snak = Snak(property_number=property_id, datatype="time", datavalue={ "value" : {"time": time_formatted, "timezone": 0, "before": 0, "after": 0, "precision": time_precision, "calendarmodel": "http://www.wikidata.org/entity/Q1985727"}, "type" : "time"})

    claim = Claim()
    claim.mainsnak = new_snak

    item_to_update.add_claims(claim)
    itemEnt = item_to_update.write(login=login_instance)
    #print(itemEnt.get_json())

def update_item_place():
    #setting instance of place
    #setting country
    #coordinates
    return

property_data = {"label" : "place of death", "description" : "most specific known (e.g. city instead of country, or hospital instead of city) death location of a person, animal or fictional character",
        "aliases" : [ "deathplace", "died in", "death place", "POD", "location of death" ]  }

def insert_new_property(data):
    new_property = wbi.property.new()

    new_property.labels.set(language='en', value=data['label'])
    new_property.descriptions.set(language='en', value=data['description'])
    new_property.aliases.set(language='en', values=data['aliases'])
    new_property.datatype = "wikibase-item"
    new_property.write(login=login_instance)
    return

def update_property_wikidataPID(property_id, wikidataPID):
    property_to_update = wbi.property.get(property_id)
    new_snak = Snak(property_number="P5", datatype="external-id", datavalue={"value" : wikidataPID, "type" : "string"})

    claim = Claim()
    claim.mainsnak = new_snak

    property_to_update.add_claims(claim)
    itemEnt = property_to_update.write(login=login_instance)


#insert_new_property(data=property_data)
#update_property_wikidataPID("P14")

'''
with open("prm.json", 'a', encoding="utf-8") as f:
    f.write(json.dumps(get_property("P13").get_json()))
    f.write(json.dumps(get_property("P11").get_json()))
    f.flush()
'''


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