from handler import login_instance
from handler import wbi
from handler import general_properties

import handler
import query_handler

class Caption:

    caption_properties = {"text" : "P49", "on_page": "P47", "repro" : "P50"}
    qid = "Q37"
    caption_numeric_id = 37
    caption_qid = -1
    caption_title = ""

    def caption_in_db(self):
        self.caption_qid = query_handler.query_db(self.caption_title, "caption")
        return self.caption_qid

    #data = { caption_title, text, on_page, repro}
    def caption_insert_new(self, data, lang):
        item = wbi.item.new()
        label = data["caption_title"]
        item.labels.set(language='en', value=label)

        #instance of
        instance_snak = handler.Snak(
            property_number=general_properties["instance_of"],
            datatype="wikibase-item",
            datavalue={
                "value": {
                    "entity-type": "item",
                    "numeric-id": self.caption_numeric_id,
                    "id": self.qid
                },
                "type": "wikibase-entityid"
            }
        )
        instance_claim = handler.Claim()
        instance_claim.mainsnak = instance_snak

        #text
        text_snak = handler.Snak(
            property_number=self.caption_properties["text"],
            datatype="monolingualtext",
            datavalue={
                "value": {
                    "text": data["text"],
                    "language": lang
                },
                "type" : "monolingualtext"
            }
        )
        text_claim = handler.Claim()
        text_claim.mainsnak = text_snak

        #on page
        on_page_snak = handler.Snak(
            property_number=self.caption_properties["on_page"],
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

        #repro
        repro_snak = handler.Snak(
            property_number=self.caption_properties["repro"],
            datatype="wikibase-item",
            datavalue={
                "value" : {
                    "entity-type": "item",
                    "numeric-id": data["repro"],
                    "id": "Q" + str(data["repro"])
                },
                "type": "wikibase-entityid"
            }
        )
        repro_claim = handler.Claim()
        repro_claim.mainsnak = repro_snak

        item.add_claims([instance_claim, text_claim, on_page_claim, repro_claim])
        item.write(login=login_instance)