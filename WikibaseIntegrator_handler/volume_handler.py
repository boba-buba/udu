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

    def volume_general_query(self, query):
        return query_handler.execute_general_query(query)

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
            start_time_snack = handler.Snak(
                property_number=general_properties["start_time"],
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
            start_time_claim = handler.Claim()
            start_time_claim.mainsnak = start_time_snack
            item.add_claims(start_time_claim)

        if "end" in data:
            end_time_snack = handler.Snak(
                property_number=general_properties["end_time"],
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
            end_time_claim = handler.Claim()
            end_time_claim.mainsnak = end_time_snack
            item.add_claims(end_time_claim)

        itemEnt = item.write(login=login_instance)

    def volume_update_date(self, new_values):
        # implementation
        item = wbi.item.get(self.volume_qid)

        if "start" in new_values:
            item.claims.remove(general_properties["start_time"])

            start_time_snack = handler.Snak(
                property_number=general_properties["start_time"],
                datatype="time",
                datavalue={
                    "value": {
                        "time": new_values["start"],
                        "timezone": 0,
                        "before": 0,
                        "after": 0,
                        "precision": new_values["precision"],
                        "calendarmodel": "http://www.wikidata.org/entity/Q1985727"
                    },
                    "type": "time"
                }
            )

            start_time_claim = handler.Claim()
            start_time_claim.mainsnak = start_time_snack
            item.add_claims(start_time_claim)

        if "end" in new_values:
            item.claims.remove(general_properties["end_time"])

            end_time_snack = handler.Snak(
                property_number=general_properties["end_time"],
                datatype="time",
                datavalue={
                    "value": {
                        "time": new_values["end"],
                        "timezone": 0,
                        "before": 0,
                        "after": 0,
                        "precision": new_values["precision"],
                        "calendarmodel": "http://www.wikidata.org/entity/Q1985727"
                    },
                    "type": "time"
                }
            )
            end_time_claim = handler.Claim()
            end_time_claim.mainsnak = end_time_snack
            item.add_claims(end_time_claim)

        item.write(login=login_instance)
