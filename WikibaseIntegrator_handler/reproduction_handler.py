from handler import login_instance
from handler import wbi
from handler import general_properties

import handler
import query_handler

class Repro:

    repro_properties = {"area" : "P46", "on_page" : "P47", "page_placement" : "P48", "x1": "P42", "y1" : "P43", "x2" : "P44", "y2": "P45", "width": "P40", "height" : "P41" }
    qid = "Q33"
    repro_numeric_id = 33
    repro_qid = -1
    repro_title = ""

    def repro_in_db(self):
        self.repro_qid = query_handler.query_db(self.repro_title, "repro")
        return self.repro_qid

    # data = { repro_title, area, on_page, x1, y1, x2, y2, width, height }
    def repro_insert_new(self, data, lang):
        item = wbi.item.new()
        label = data["repro_title"]
        item.labels.set(language='en', value=label)

        #instance of
        instance_snak = handler.Snak(
            property_number=general_properties["instance_of"],
            datatype="wikibase-item",
            datavalue={
                "value": {
                    "entity-type": "item",
                    "numeric-id": self.repro_numeric_id,
                    "id": self.qid
                },
                "type": "wikibase-entityid"
            }
        )
        instance_claim = handler.Claim()
        instance_claim.mainsnak = instance_snak

        #area
        area_snak = handler.Snak(
            property_number=self.repro_properties["area"],
            datatype="quantity",
            datavalue={
                "value": {
                    "amount" : "+" + str(data["area"]),
                    "unit" : "http://147.231.55.155/entity/Q35" # or get it through query?
                },
                "type" : "quantity"
            }
        )
        area_claim = handler.Claim()
        area_claim.mainsnak = area_snak

        #on_page
        on_page_snak = handler.Snak(
            property_number=self.repro_properties["on_page"],
            datatype="wikibase-item",
            datavalue={
                "value" : {
                    "entity-type": "item",
                    "numeric-id": data["on_page"],
                    "id": "Q" + str(data["on_page"])
                },
                "type" : "wikibase-entityid"
            }
        )
        on_page_claim = handler.Claim()
        on_page_claim.mainsnak = on_page_snak

        #width
        width_snak = handler.Snak(
            property_number=self.repro_properties["width"],
            datatype="quantity",
            datavalue={
                "value": {
                    "amount" : "+" + str(data["width"]),
                    "unit" : "http://147.231.55.155/entity/Q36"
                },
                "type" : "quantity"
            }
        )
        width_claim = handler.Claim()
        width_claim.mainsnak = width_snak

        #height
        height_snak = handler.Snak(
            property_number=self.repro_properties["height"],
            datatype="quantity",
            datavalue={
                "value": {
                    "amount" : "+" + str(data["height"]),
                    "unit" : "http://147.231.55.155/entity/Q36"
                },
                "type": "quantity"
            }
        )
        height_claim = handler.Claim()
        height_claim.mainsnak = height_snak

        #TODO page placement

        item.add_claims([instance_claim, area_claim, on_page_claim, width_claim, height_claim])
        itemEnt = item.write(login=login_instance)

