from handler import login_instance
from handler import wbi
from handler import general_properties
from query_handler import execute_query, execute_query_get_multiple_results

import handler
import query_handler

necessary_properties = {"instance" : "P1", 'img_addr': 'P69', 'wikiart_id': 'P74',
                         'wikiart_url': 'P73', 'completion_date': 'P77', 'width': 'P40',
                         'height': 'P41', 'artist': 'P78'}

necessary_items = {'artwork' : 'Q3'}


class ArtWork:
    def InsertNew(self, data: dict[str, str]):
        item = wbi.item.new()

        label = data["title"]
        item.labels.set(language='en', value=label)

        #instance of
        instance_snak = handler.Snak(
        property_number=necessary_properties["instance"],
            datatype="wikibase-item",
            datavalue={
                "value": {
                    "entity-type": "item",
                    "numeric-id": int(necessary_items["artwork"][1:]),
                    "id": necessary_items["artwork"]
                },
                "type": "wikibase-entityid"
            }
        )
        instance_claim = handler.Claim()
        instance_claim.mainsnak = instance_snak
        item.claims.add(instance_claim)

        #title
        title_snack = handler.Snak(
            property_number=general_properties["title"],
            datatype="monolingualtext",
            datavalue={
                "value": {
                    "text": data["title"],
                    "language": 'en'
                },
                "type": "monolingualtext"
            }
        )
        title_claim = handler.Claim()
        title_claim.mainsnak = title_snack
        item.claims.add(title_claim)

        #wikiart id
        wikiart_id_snak = handler.Snak(
            property_number=necessary_properties["wikiart_id"],
            datatype="string",
            datavalue={
                "value": data["contentId"],
                "type" : "string"
            }
        )
        wikiart_id_claim = handler.Claim()
        wikiart_id_claim.mainsnak = wikiart_id_snak
        item.claims.add(wikiart_id_claim)

        #artist
        artist_snak = handler.Snak(
        property_number=necessary_properties["artist"],
            datatype="wikibase-item",
            datavalue={
                "value": {
                    "entity-type": "item",
                    "numeric-id": int(data["artist_qid"][1:]),
                    "id": data["artist_qid"]
                },
                "type": "wikibase-entityid"
            }
        )
        artist_claim = handler.Claim()
        artist_claim.mainsnak = artist_snak
        item.claims.add(artist_claim)

        #completetion year
        if "completitionYear" in data and data["completitionYear"] != '':
            completion_snak = handler.Snak(
            property_number=necessary_properties["completion_date"],
            datatype="time",
            datavalue={
                "value": {
                    "time": data["completitionYear"],
                    "timezone": 0,
                    "before": 0,
                    "after": 0,
                    "precision": data["completitionYear_precision"],
                    "calendarmodel": "http://www.wikidata.org/entity/Q1985727"
                },
                "type": "time"
                }
            )
            completion_claim = handler.Claim()
            completion_claim.mainsnak = completion_snak
            item.claims.add(completion_claim)


        #width
        width_snak = handler.Snak(
            property_number=necessary_properties["width"],
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
        item.claims.add(width_claim)

        #height
        height_snak = handler.Snak(
            property_number=necessary_properties["height"],
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
        item.claims.add(height_claim)

        #image
        img_addr_snak = handler.Snak(
            property_number=necessary_properties["img_addr"],
            datatype="monolingualtext",
            datavalue={
                "value": {
                    "text" : data["image"],
                    "language" : "en"
                },
                "type" : "monolingualtext"
            }
        )
        img_addr_claim = handler.Claim()
        img_addr_claim.mainsnak = img_addr_snak
        item.claims.add(img_addr_claim)

        itemEnt = item.write(login=login_instance)

    def Exists(self, name: str, wikiart_id: str) -> bool:
        query = 'SELECT ?item WHERE { ?item ?label "' + name +'"@en .}'
        retval = execute_query_get_multiple_results(query)
        if retval == []:
            return False
        else:
            for i in range(len(retval)):
                item = wbi.item.get(entity_id=retval[i])
                if 'P74' in item.claims and item.claims.get('P74')[0].mainsnak.datavalue['value'] == wikiart_id:
                    return True

        return False