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

        item.add_claims([instance_claim, title_claim])

        itemEnt = item.write(login=login_instance)

    def magazine_update(self, data):
        magazine_item = handler.get_item()
    """
    def magazine_handle(self, data, request):
        magazine_name = data['name']
        magazine_id = self.magazine_in_db(magazine_name=magazine_name)
        if magazine_id == -1:
            lang = data['lang']
            self.magazine_insert_new(data, lang)
        else:
            if len(data) > 2: #miminum name and lang
                self.magazine_update(data)
    """



