from handler import login_instance
from handler import wbi
from handler import general_properties

import handler
import query_handler

necessary_properties = {'given_name' : 'P61', 'family_name' : 'P60', 'sec_fam_name' : 'P62', 'pseudonym' : 'P58' ,
                        'birth_date' : 'P2', 'birth_place' : 'P64', 'death_date' : 'P3', 'death_place' : 'P65',
                        'ident' : 'P63', 'birth_country' : 'P66', 'death_country' : 'P67', 'ethnic_gr' : 'P55',
                        'sex' : 'P8', "instance" : "P1", 'img_addr': 'P69', 'wikiart_id': 'P74',
                         'wikiart_url': 'P73', 'active_years_start': 'P75', 'active_years_end': 'P76'}

necessary_items = {'human' : 'Q4', 'male' : 'Q5', 'female' : 'Q6', 'other' : 'Q769'}


class Human:
    def InsertNewHuman(self, data: dict[str, str]):
        item = wbi.item.new()

        label = data["artistName"]
        item.labels.set(language="en", value=label)

        #instance of
        instance_snak = handler.Snak(
        property_number=necessary_properties["instance"],
            datatype="wikibase-item",
            datavalue={
                "value": {
                    "entity-type": "item",
                    "numeric-id": int(necessary_items["human"][1:]),
                    "id": necessary_items["human"]
                },
                "type": "wikibase-entityid"
            }
        )
        instance_claim = handler.Claim()
        instance_claim.mainsnak = instance_snak
        item.claims.add(instance_claim)

        name_surname = data["artistName"].split(' ', 1)

        #given name
        given_name_snak = handler.Snak(
            property_number=necessary_properties['given_name'],
            datatype='string',
            datavalue={
                "value": name_surname[0],
                "type" : "string"
            }
        )
        given_name_claim = handler.Claim()
        given_name_claim.mainsnak = given_name_snak
        item.claims.add(given_name_claim)

        #surname
        surname_snak = handler.Snak(
            property_number=necessary_properties["family_name"],
            datatype="string",
            datavalue={
                "value" : name_surname[-1],
                "type" : "string"
            }
        )
        surname_claim = handler.Claim()
        surname_claim.mainsnak = surname_snak
        item.claims.add(surname_claim)

        #birth
        if "birthDayAsString" in data and data['birthDayAsString'] != '':
            birth_date_snak = handler.Snak(
                property_number=necessary_properties["birth_date"],
                datatype="time",
                datavalue={
                    "value": {
                        "time": data["birthDayAsString"],
                        "timezone": 0,
                        "before": 0,
                        "after": 0,
                        "precision": data["birthDayAsString_precision"],
                        "calendarmodel": "http://www.wikidata.org/entity/Q1985727"
                    },
                    "type": "time"
                }
            )
            birth_date_claim = handler.Claim()
            birth_date_claim.mainsnak = birth_date_snak
            item.claims.add(birth_date_claim)

        #death
        if "deathDayAsString" in data and data['deathDayAsString'] != '':
            death_date_snak = handler.Snak(
                property_number=necessary_properties["death_date"],
                datatype="time",
                datavalue={
                    "value": {
                        "time": data["deathDayAsString"],
                        "timezone": 0,
                        "before": 0,
                        "after": 0,
                        "precision": data["deathDayAsString_precision"],
                        "calendarmodel": "http://www.wikidata.org/entity/Q1985727"
                    },
                    "type": "time"
                }
            )
            death_date_claim = handler.Claim()
            death_date_claim.mainsnak = death_date_snak
            item.claims.add(death_date_claim)

        #active years start
        if "activeYearsStart" in data and data["activeYearsStart"] != '':
            active_start_snak = handler.Snak(
            property_number=necessary_properties["active_years_start"],
            datatype="time",
            datavalue={
                "value": {
                    "time": data["activeYearsStart"],
                    "timezone": 0,
                    "before": 0,
                    "after": 0,
                    "precision": data["activeYearsStart_precision"],
                    "calendarmodel": "http://www.wikidata.org/entity/Q1985727"
                },
                "type": "time"
                }
            )
            active_start_claim = handler.Claim()
            active_start_claim.mainsnak = active_start_snak
            item.claims.add(active_start_claim)

        #active years end
        if "activeYearsCompletion" in data and data["activeYearsCompletion"] != '':
            active_end_snak = handler.Snak(
            property_number=necessary_properties["active_years_end"],
            datatype="time",
            datavalue={
                "value": {
                    "time": data["activeYearsCompletion"],
                    "timezone": 0,
                    "before": 0,
                    "after": 0,
                    "precision": data["activeYearsCompletion_precision"],
                    "calendarmodel": "http://www.wikidata.org/entity/Q1985727"
                },
                "type": "time"
                }
            )
            active_end_claim = handler.Claim()
            active_end_claim.mainsnak = active_end_snak
            item.claims.add(active_end_claim)

        #img_address
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
        item.add_claims([img_addr_claim])

        #gender
        if "gender" in data and data["gender"] != '':
            sex = necessary_items[data["gender"]]
            sex_snak = handler.Snak(
                property_number=necessary_properties["sex"],
                datatype="wikibase-item",
                datavalue={
                    "value": {
                        "entity-type": "item",
                        "numeric-id": int(sex[1:]),
                        "id": sex
                    },
                    "type": "wikibase-entityid"
                }
            )
            sex_claim = handler.Claim()
            sex_claim.mainsnak = sex_snak
            item.claims.add(sex_claim)

        #wikiart id
        wikiart_id_snak = handler.Snak(
            property_number=necessary_properties["wikiart_id"],
            datatype="string",
            datavalue={
                "value": data["id"],
                "type" : "string"
            }
        )
        wikiart_id_claim = handler.Claim()
        wikiart_id_claim.mainsnak = wikiart_id_snak
        item.claims.add(wikiart_id_claim)

        #wikiart url
        url_snak = handler.Snak(
            property_number=necessary_properties["wikiart_url"],
            datatype="external-id",
            datavalue={
                "value": data["url"],
                "type": "string"
            }
        )
        url_claim = handler.Claim()
        url_claim.mainsnak = url_snak
        item.claims.add(url_claim)

        itemEnt = item.write(login=login_instance)

    def Exists(self, name_label: str) -> str:
        query = 'SELECT ?item ?label WHERE { ?item wdt:P1 wd:Q4; rdfs:label ?label. FILTER(LANG(?label) = "en"). FILTER(STRSTARTS(?label, "' + name_label + '")). SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],mul,en". }}'

        qid = query_handler.execute_query(query)
        if qid != -1:
            return qid
        else: return "None"


    def AddToExisting(self, data: dict[str, str], qid: str):
        item = wbi.item.get(entity_id=qid)

        # wikiart_url = item.claims.get('P73')[0].mainsnak.datavalue['value']
        # if wikiart_url != '':
        #     return
        if 'P73' in item.claims:
            return

        #active years start
        if "activeYearsStart" in data and data["activeYearsStart"] != '':
            active_start_snak = handler.Snak(
            property_number=necessary_properties["active_years_start"],
            datatype="time",
            datavalue={
                "value": {
                    "time": data["activeYearsStart"],
                    "timezone": 0,
                    "before": 0,
                    "after": 0,
                    "precision": data["activeYearsStart_precision"],
                    "calendarmodel": "http://www.wikidata.org/entity/Q1985727"
                },
                "type": "time"
                }
            )
            active_start_claim = handler.Claim()
            active_start_claim.mainsnak = active_start_snak
            item.claims.add(active_start_claim)

        #active years end
        if "activeYearsCompletion" in data and data["activeYearsCompletion"] != '':
            active_end_snak = handler.Snak(
            property_number=necessary_properties["active_years_end"],
            datatype="time",
            datavalue={
                "value": {
                    "time": data["activeYearsCompletion"],
                    "timezone": 0,
                    "before": 0,
                    "after": 0,
                    "precision": data["activeYearsCompletion_precision"],
                    "calendarmodel": "http://www.wikidata.org/entity/Q1985727"
                },
                "type": "time"
                }
            )
            active_end_claim = handler.Claim()
            active_end_claim.mainsnak = active_end_snak
            item.claims.add(active_end_claim)

        #img_address
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
        item.add_claims([img_addr_claim])

        #wikiart id
        wikiart_id_snak = handler.Snak(
            property_number=necessary_properties["wikiart_id"],
            datatype="string",
            datavalue={
                "value": data["id"],
                "type" : "string"
            }
        )
        wikiart_id_claim = handler.Claim()
        wikiart_id_claim.mainsnak = wikiart_id_snak
        item.claims.add(wikiart_id_claim)

        #wikiart url
        url_snak = handler.Snak(
            property_number=necessary_properties["wikiart_url"],
            datatype="external-id",
            datavalue={
                "value":data["url"],
                "type": "string"
            }
        )
        url_claim = handler.Claim()
        url_claim.mainsnak = url_snak
        item.claims.add(url_claim)

        itemEnt = item.write(login=login_instance)


#h = Human()

# print(h.Exists("Pablo Picasso"))
#h.AddToExisting({}, h.Exists("Pablo Picasso"))