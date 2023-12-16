from handler import login_instance
from handler import wbi
from handler import general_properties
import handler

magazine_properties = {"inception" : "P9", "country" : "P10", "country_origin" : "P17", "lang" : "P18", "dissolved" : "P19", "publisher" : "P20", "title" : "P22", "editor" : "P24", "printed_by" : "P24", "reference" : "P25"  }
magazine_qid = "Q7"
magazine_numeric_id = 7

def insert_new_magazine(data, lang):
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

def update_magazine(data):
    magazine_item = handler.get_item()