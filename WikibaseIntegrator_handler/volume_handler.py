from handler import login_instance
from handler import wbi
from handler import general_properties

import handler

class Volume:

    volume_properties = {"volume" : "P27", "part_of" : "P29", "title" : "P22"}
    volume_qid = "Q10"
    volume_numeric_id = 10

    def volume_insert_new(self, data):
        #data = {vol_number : ..., magazine_name : ... , publication date start: ..., publication date end: ...} date in what foramt
        item = wbi.item.new()
        label = data['magazine'] + ", Vol." + data["vol_number"]
        item.labels.set(language='en', value=label)

        #description ???
        #######
        instance_snack = handler.Snack(
            property_number=general_properties["instance_of"],
            datatype="wikibase-item",
            datavalue={
                "value": {
                    "entity-type": "item",
                    "numeric-id": self.volume_numeric_id,
                    "id": self.volume_qid
                },
                "type": "wikibase-entityid"
            }
        )
        instance_claim = handler.Claim()
        instance_claim.mainsnak = instance_snack
        ######
        volume_snack = handler.Snak(
            property_number=self.volume_properties["volume"],
            datatype="string",
            datavalue={
                "value": data["vol_number"],
                "type": "string"
            }
        )
        volume_claim=handler.Claim()
        volume_claim.mainsnak = volume_snack
    #####
    ## publication date 
    # start time
    # end time

    # Q116172661
    #SELECT ?item ?itemLabel ?itemDescription ?book ?bookLabel WHERE {
    #   ?item wdt:P31 wd:Q1238720 .
    #   ?item wdt:P361 ?book .
    #   ?book wdt:P31 wd:Q41298 .
    # SERVICE bla bla
    # }

        item.add_claims([instance_claim, volume_claim])

        itemEnt = item.write(login=login_instance)

    def volume_handle(self, data): #data magazine title, volume number
        magazine_name = data['name']
        magazine_id = self.magazine_in_db(magazine_name=magazine_name)
        if magazine_id == -1:
            lang = data['lang']
            self.magazine_insert_new(data, lang)
        else:
            if len(data) > 2: #miminum name and lang
                self.magazine_update(data)