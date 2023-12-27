from enum import Enum
from handler import login_instance
from handler import wbi
from handler import general_properties
import handler
from wikibaseintegrator import wbi_helpers



class magazine_request(Enum):
    insert = 1
    update = 2

class Magazine:
    magazine_properties = {"inception" : "P9", "country" : "P10", "country_origin" : "P17", "lang" : "P18", "dissolved" : "P19", "publisher" : "P20", "title" : "P22", "editor" : "P24", "printed_by" : "P24", "reference" : "P25"  }
    magazine_qid = "Q7"
    magazine_numeric_id = 7

    # check if already in wiki
    # query =
    # SELECT ?item
    # WHERE {
    #   ?item wdt:P1 wd:Q7;
    #         wdt:P22 ?title .
    #   FILTER(STR(?title) = magazine_name).
    #   SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
    # }

    def magazine_in_db(self, magazine_name): # must return QID or -1
        query = 'SELECT ?item WHERE { ?item wdt:P1 wd:Q7; wdt:P22 ?title . FILTER(STR(?title) ="' +  magazine_name + '"). SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}'
        #print(query)
        result = wbi_helpers.execute_sparql_query(query=query, prefix="", endpoint="http://147.231.55.155:8834/proxy/wdqs/bigdata/namespace/wdq/sparql", max_retries=1)
        print(result)

    def magazine_insert_new(self, data, lang):
        # minimal format of the data {'label': 'smth', 'description' : 'smth'}
        #
        item = wbi.item.new()

        # Set an english label and description
        item.labels.set(language='en', value=data['label'])
        item.descriptions.set(language='en', value=data['description'])

        if lang == "cs":
            item.labels.add(language='cs', value=data['label_cs'])
            item.descriptions.add(language_value='cs', value=data['description_cs'])

        instance_snack = handler.Snack(
            property_number=general_properties["instance_of"],
            datatype="wikibase-item",
            datavalue={
                "value": {
                    "entity-type": "item",
                    "numeric-id": magazine_numeric_id,
                    "id": magazine_qid
                },
                "type": "wikibase-entityid"
            }
        )
        instance_claim = handler.Claim()
        instance_claim.mainsnak = instance_snack

        item.add_claims(instance_claim)

        itemEnt = item.write(login=login_instance)
        #print(itemEnt)

    def magazine_update(self, data):
        magazine_item = handler.get_item()

    def magazine_handle(self, data, request):
        magazine_name = data['name']
        magazine_id = self.magazine_in_db(magazine_name=magazine_name)
        if magazine_id == -1:
            lang = data['lang']
            self.magazine_insert_new(data, lang)
        else:
            if len(data) > 2: #miminum name and lang
                self.magazine_update(data)


mag = "Volné směry"
mag2 = "Volne smery"
Magazine.magazine_in_db(mag2)
#Volné směry


