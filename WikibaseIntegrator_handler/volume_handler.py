from handler import login_instance
from handler import wbi
from handler import general_properties

import handler
import query_handler

class Volume:

    volume_properties = {"volume" : "P27", "title" : "P22", "volume_number" : "P51"}
    qid = "Q10"
    volume_numeric_id = 10
    volume_qid = -1
    volume_title = ""

    def volume_in_db(self):
        self.volume_qid = query_handler.query_db(self.volume_title, "volume")
        return self.volume_qid


    def volume_insert_new(self, data, lang):
        #data = {vol_number : ..., magazine_numeric_id: ..., start: .., end: ..., precision: ...} date in what foramt
        item = wbi.item.new()
        label = self.volume_title
        item.labels.set(language='en', value=label)

        #instance of
        instance_snack = handler.Snak(
            property_number=general_properties["instance_of"],
            datatype="wikibase-item",
            datavalue={
                "value": {
                    "entity-type": "item",
                    "numeric-id": self.volume_numeric_id,
                    "id": self.qid
                },
                "type": "wikibase-entityid"
            }
        )
        instance_claim = handler.Claim()
        instance_claim.mainsnak = instance_snack

        #volume
        volume_snack = handler.Snak(
            property_number=self.volume_properties["volume"],
            datatype="string",
            datavalue={
                "value": data["vol_number"],
                "type" : "string"
            }
        )
        volume_claim=handler.Claim()
        volume_claim.mainsnak = volume_snack

        #part of
        part_of_snak = handler.Snak(
            property_number=general_properties["part_of"],
            datatype="wikibaseitem",
            datavalue={
                "value": {
                    "entity-type": "item",
                    "numeric-id": data["magazine_numeric_id"],
                    "id": "Q" + str(data["magazine_numeric_id"])
                },
                "type" : "wikibase-entityid"
            }
        )
        part_of_claim = handler.Claim()
        part_of_claim.mainsnak = part_of_snak

        #title
        title_snack = handler.Snak(
            property_number=general_properties["title"],
            datatype="monolingualtext",
            datavalue={
                "value": {
                    "text": label,
                    "language": lang
                },
                "type": "monolingualtext"
            }
        )
        title_claim = handler.Claim()
        title_claim.mainsnak = title_snack

        item.add_claims([instance_claim, volume_claim, part_of_claim, title_claim])

        #time
        if "start" in data:
            inception_snack = handler.Snak(
                property_number=general_properties["inception"],
                datatype="time",
                datavalue={
                    "value": {
                        "time": data["start"],
                        "timezone": 0,
                        "before": 0,
                        "after": 0,
                        "precision": data["precision"],
                        "calendarmodel": "http://www.wikidata.org/entity/Q1985727"
                    },
                    "type": "time"
                }
            )
            inception_claim = handler.Claim()
            inception_claim.mainsnak = inception_snack
            item.add_claims(inception_claim)

        if "end" in data:
            dissolved_snack = handler.Snak(
                property_number=general_properties["dissolved"],
                datatype="time",
                datavalue={
                    "value": {
                        "time": data["end"],
                        "timezone": 0,
                        "before": 0,
                        "after": 0,
                        "precision": data["precision"],
                        "calendarmodel": "http://www.wikidata.org/entity/Q1985727"
                    },
                    "type": "time"
                }
            )
            dissolved_claim = handler.Claim()
            dissolved_claim.mainsnak = dissolved_snack
            item.add_claims(dissolved_snack)


        itemEnt = item.write(login=login_instance)
    """
    def volume_handle(self, data): #data magazine title, volume number
        magazine_name = data['name']
        magazine_id = self.magazine_in_db(magazine_name=magazine_name)
        if magazine_id == -1:
            lang = data['lang']
            self.magazine_insert_new(data, lang)
        else:
            if len(data) > 2: #miminum name and lang
                self.magazine_update(data)"""