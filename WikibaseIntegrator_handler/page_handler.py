from handler import login_instance
from handler import wbi
from handler import general_properties

import handler
import query_handler

class Page:

    page_properties = {"page_number" : "P35", "page_index" : "P36", "num_of_repro" : "P38", "has_text" : "P37"}
    qid = "Q31"
    page_numeric_id = 31
    page_qid = -1
    page_title = ""

    def page_in_db(self):
        self.page_qid = query_handler.query_db(self.page_title, "page")
        return self.page_qid
    #data = page_title, page_number, page_index, num_of_repro, has_text, iss_vol_numeric_id, width_page, height_page
    def page_insert_new(self, data, lang):
        item = wbi.item.new()
        label = data["page_title"]
        item.labels.set(language='en', value=label)


        #instance of
        instance_snak = handler.Snak(
            property_number=general_properties["instance_of"],
            datatype="wikibase-item",
            datavalue={
                "value": {
                    "entity-type": "item",
                    "numeric-id": self.page_numeric_id,
                    "id": self.qid
                },
                "type": "wikibase-entityid"
            }
        )
        instance_claim = handler.Claim()
        instance_claim.mainsnak = instance_snak

        #page number
        page_number_snak = handler.Snak(
            property_number=self.page_properties["page_number"],
            datatype="string",
            datavalue={
                "value": data["page_number"],
                "type": "string"
            }
        )
        page_number_claim=handler.Claim()
        page_number_claim.mainsnak = page_number_snak

        #page index
        if data["page_index"] != "":
            page_index_snak = handler.Snak(
                property_number=self.page_properties["page_index"],
                datatype="string",
                datavalue={
                    "value": data["page_index"],
                    "type": "string"
                }
            )
            page_index_claim=handler.Claim()
            page_index_claim.mainsnak = page_index_snak
            item.add_claims(page_index_claim)

        #part of
        part_of_snak = handler.Snak(
            property_number=general_properties["part_of"],
            datatype="wikibaseitem",
            datavalue={
                "value": {
                    "entity-type": "item",
                    "numeric-id": data["iss_vol_numeric_id"],
                    "id": "Q" + str(data["iss_vol_numeric_id"])
                },
                "type" : "wikibase-entityid"
            }
        )
        part_of_claim = handler.Claim()
        part_of_claim.mainsnak = part_of_snak

        #number of repro
        num_of_repro_snak = handler.Snak(
            property_number=self.page_properties["num_of_repro"],
            datatype="quantity",
            datavalue={
                "value": {
                    "amount": "+" + str(data["num_of_repro"]),
                    "unit": "1"
                },
                "type" : "quantity"
            }
        )
        num_of_repro_claim = handler.Claim()
        num_of_repro_claim.mainsnak = num_of_repro_snak

        #width_page
        width_snak = handler.Snak(
            property_number=handler.general_properties["width"],
            datatype="quantity",
            datavalue={
                "value": {
                    "amount" : "+" + str(data["width_page"]),
                    "unit" : "http://147.231.55.155/entity/Q36"
                },
                "type" : "quantity"
            }
        )
        width_claim = handler.Claim()
        width_claim.mainsnak = width_snak

        #height_page
        height_snak = handler.Snak(
            property_number=handler.general_properties["height"],
            datatype="quantity",
            datavalue={
                "value": {
                    "amount" : "+" + str(data["height_page"]),
                    "unit" : "http://147.231.55.155/entity/Q36"
                },
                "type": "quantity"
            }
        )
        height_claim = handler.Claim()
        height_claim.mainsnak = height_snak

        #has text
        value = "no"
        if data["has_text"] == 1: value = "yes"
        has_text_snak = handler.Snak(
            property_number=self.page_properties["has_text"],
            datatype="string",
            datavalue={
                "value" : value,
                "type": "string"
            }
        )
        has_text_claim = handler.Claim()
        has_text_claim.mainsnak = has_text_snak


        item.add_claims([instance_claim, page_number_claim, part_of_claim, num_of_repro_claim, has_text_claim, width_claim, height_claim])
        itemEnt = item.write(login=login_instance)

    def page_update(self, data):
        self.qid = self.page_in_db(data["title"], "page")
    




