from wikibaseintegrator import WikibaseIntegrator
import json
from wikibaseintegrator.wbi_config import config as wbi_config

wbi_config['USER_AGENT'] = "Boba-buba-Bot/1.0 (https://www.wikidata.org/wiki/User:Boba-buba)"

wbi = WikibaseIntegrator()
my_first_wikidata_item = wbi.item.get(entity_id='Q116172775')

# to check successful installation and retrieval of the data, you can print the json representation of the item

with open("wikidata.json", 'w', encoding="utf-8") as f:
    f.write(json.dumps(my_first_wikidata_item.get_json()))
    f.flush()