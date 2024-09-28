from handler import login_instance
from handler import wbi
from handler import general_properties
import handler
import query_handler
from wikibaseintegrator import wbi_helpers




class Magazine:
    magazine_properties = {"inception" : "P9", "country" : "P10", "country_origin" : "P17", "lang" : "P18", "dissolved" : "P19", "publisher" : "P20", "title" : "P22", "editor" : "P24", "printed_by" : "P24", "reference" : "P25"  }
    qid = "Q7"
    magazine_numeric_id = 7
    magazine_qid = -1
    magazine_name = ""

    def magazine_in_db(self): # must return QID or -1
        self.magazine_qid = query_handler.query_db(self.magazine_name, "magazine")
        return self.magazine_qid


    def magazine_insert_new(self, lang):
        # minimal format of the data {'label': 'smth', (opt)'label_cs' : 'smth', 'description' : 'smth'}

        item = wbi.item.new()

        # Set an english label and description

        #item.descriptions.set(language='en', value=data['description'])


        item.labels.set(language='en', value=self.magazine_name) #default option is english


        #instance of
        instance_snack = handler.Snak(
            property_number=general_properties["instance_of"],
            datatype="wikibase-item",
            datavalue={
                "value": {
                    "entity-type": "item",
                    "numeric-id": self.magazine_numeric_id,
                    "id": self.qid
                },
                "type": "wikibase-entityid"
            }
        )
        instance_claim = handler.Claim()
        instance_claim.mainsnak = instance_snack

        #title
        title_snack = handler.Snak(
            property_number=general_properties["title"],
            datatype="monolingualtext",
            datavalue={
                "value": {
                    "text": self.magazine_name,
                    "language": lang
                },
                "type": "monolingualtext"
            }
        )
        title_claim = handler.Claim()
        title_claim.mainsnak = title_snack

        #country
        id = query_handler.execute_query('SELECT ?item WHERE { ?item wdt:P1 wd:Q18. ?item ?label "' + lang + '"@en .}')
        country_snak = handler.Snak(
            property_number=general_properties["country"],
            datatype="wikibase-item",
            datavalue={
                "value": {
                    "entity-type": "item",
                    "numeric-id": int(id[1:]),
                    "id": id
                },
                "type": "wikibase-entityid"
            }
        )
        country_claim = handler.Claim()
        country_claim.mainsnak = country_snak

        item.add_claims([instance_claim, title_claim, country_claim])

        itemEnt = item.write(login=login_instance)

    def magazine_update(self, data):
        magazine_item = handler.get_item()
