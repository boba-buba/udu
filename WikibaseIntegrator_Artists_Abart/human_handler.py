from handler import login_instance
from handler import wbi
from handler import general_properties

import handler
import query_handler

necessary_properties = {'given_name' : 'P61', 'family_name' : 'P60', 'sec_fam_name' : 'P62', 'pseudonym' : 'P58' ,
                        'birth_date' : 'P2', 'birth_place' : 'P64', 'death_date' : 'P3', 'death_place' : 'P65',
                        'ident' : 'P63', 'birth_country' : 'P66', 'death_country' : 'P67', 'ethnic_gr' : 'P55',
                        'sex' : 'P8', 'abart_id' : 'P59', 'nkaut' : 'P56', 'wikidata' : 'P4', 'viaf' : 'P57', "instance" : "P1"}
necessary_items = {'human' : 'Q4', 'male' : 'Q5', 'female' : 'Q6', 'other' : 'Q769'}

class Human:
    def person_insert_new(data):
        item = wbi.item.new()
        label = ""
        if "name" in data:
            label += data["name"]
        if "surname" in data:
            label += ' ' + data["surname"]
        item.labels.set(language='en', value=label)
        if "aliases" in data:
            item.aliases.set(language='en', values=data['aliases'])

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

        if "name" in data:
            given_name_snak = handler.Snak(
                property_number=necessary_properties['given_name'],
                datatype='string',
                datavalue={
                    "value": data["name"],
                    "type" : "string"
                }
            )
            given_name_claim = handler.Claim()
            given_name_claim.mainsnak = given_name_snak
            item.claims.add(given_name_claim)

        if "second_name" in data: #?
            given_name_snak = handler.Snak(
                property_number=necessary_properties['given_name'],
                datatype='string',
                datavalue={
                    "value": data["second_name"],
                    "type" : "string"
                }
            )
            given_name_claim = handler.Claim()
            given_name_claim.mainsnak = given_name_snak
            item.claims.add(given_name_claim)

        if "surname" in data:
            surname_snak = handler.Snak(
                property_number=necessary_properties["family_name"],
                datatype="string",
                datavalue={
                    "value" : data["surname"],
                    "type" : "string"
                }
            )
            surname_claim = handler.Claim()
            surname_claim.mainsnak = surname_snak
            item.claims.add(surname_claim)

        if "second_surname" in data:
            sec_sur_snak = handler.Snak(
                property_number=necessary_properties["sec_fam_name"],
                datatype="string",
                datavalue={
                    "value" : data["second_surname"],
                    "type" : "string"
                }
            )
            sec_sur_claim = handler.Claim()
            sec_sur_claim.mainsnak = sec_sur_snak
            item.claims.add(sec_sur_claim)

        if "pseuds" in data: #?
            for ps in data["pseuds"]:
                pseud_snak = handler.Snak(
                    property_number=necessary_properties["pseudonym"],
                    datatype="string",
                    datavalue={
                        "value" : ps,
                        "type" : "string"
                    }
                )
                pseud_claim = handler.Claim()
                pseud_claim.mainsnak= pseud_snak
                item.claims.add(pseud_claim)

        if "birth_date" in data:
            birth_date_snak = handler.Snak(
                property_number=necessary_properties["birth_date"],
                datatype="time",
                datavalue={
                    "value": {
                        "time": data["birth_date"],
                        "timezone": 0,
                        "before": 0,
                        "after": 0,
                        "precision": data["precision_birth_date"],
                        "calendarmodel": "http://www.wikidata.org/entity/Q1985727"
                    },
                    "type": "time"
                }
            )
            birth_date_claim = handler.Claim()
            birth_date_claim.mainsnak = birth_date_snak
            item.claims.add(birth_date_claim)

        if "birth_place" in data:
            birth_place_snak = handler.Snak(
                property_number=necessary_properties["birth_place"],
                datatype="monolingualtext",
                datavalue={
                    "value": {
                        "text" : data["birth_place"],
                        "language" : "cs"
                    },
                    "type" : "monolingualtext"
                }
            )
            birth_place_claim = handler.Claim()
            birth_place_claim.mainsnak = birth_place_snak
            item.claims.add(birth_place_claim)

        if "birth_country" in data:
            #Get country quid
            id = query_handler.execute_query('SELECT ?item WHERE { ?item wdt:P1 wd:Q18. ?item ?label "' + data['birth_country'] + '"@en .}')
            birth_country_snak = handler.Snak(
                property_number=necessary_properties["birth_country"],
                datatype="wikibase-item",
                datavalue={
                    "value": {
                        "entity-type": "item",
                        "numeric-id": int(id[1:]),
                        "id": id
                    },
                    "type": "wikibase-entityid"
                }
            )
            birth_country_claim = handler.Claim()
            birth_country_claim.mainsnak = birth_country_snak
            item.claims.add(birth_country_claim)

        if "death_date" in data:
            death_date_snak = handler.Snak(
                property_number=necessary_properties["death_date"],
                datatype="time",
                datavalue={
                    "value": {
                        "time": data["death_date"],
                        "timezone": 0,
                        "before": 0,
                        "after": 0,
                        "precision": data["precision_death_date"],
                        "calendarmodel": "http://www.wikidata.org/entity/Q1985727"
                    },
                    "type": "time"
                }
            )
            death_date_claim = handler.Claim()
            death_date_claim.mainsnak = death_date_snak
            item.claims.add(death_date_claim)

        if "death_place" in data:
            death_place_snak = handler.Snak(
                property_number=necessary_properties["death_place"],
                datatype="monolingualtext",
                datavalue={
                    "value": {
                        "text" : data["death_place"],
                        "language" : "cs"
                    },
                    "type" : "monolingualtext"
                }
            )
            death_place_claim = handler.Claim()
            death_place_claim.mainsnak = death_place_snak
            item.claims.add(death_place_claim)

        if "death_country" in data:
            #Get country quid
            id = query_handler.execute_query('SELECT ?item WHERE { ?item wdt:P1 wd:Q18. ?item ?label "' + data['death_country'] + '"@en .}')
            death_country_snak = handler.Snak(
                property_number=necessary_properties["death_country"],
                datatype="wikibase-item",
                datavalue={
                    "value": {
                        "entity-type": "item",
                        "numeric-id": int(id[1:]),
                        "id": id
                    },
                    "type": "wikibase-entityid"
                }
            )
            death_country_claim = handler.Claim()
            death_country_claim.mainsnak = death_country_snak
            item.claims.add(death_country_claim)

        if "ethnicity" in data:
            # get ethn id
            id = query_handler.execute_query('SELECT ?item WHERE { ?item wdt:P1 wd:Q517. ?item ?label "' + data['ethnicity'] + '"@en .}')
            ethn_snak = handler.Snak(
                property_number=necessary_properties["ethnic_gr"],
                datatype="wikibase-item",
                datavalue={
                    "value": {
                        "entity-type": "item",
                        "numeric-id": int(id[1:]),
                        "id": id
                    },
                    "type": "wikibase-entityid"
                }
            )
            ethn_claim = handler.Claim()
            ethn_claim.mainsnak = ethn_snak
            item.claims.add(ethn_claim)

        if "sex" in data:
            sex = necessary_items[data["sex"]]
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

        if "identification" in data:
            ident_snak = handler.Snak(
                property_number=necessary_properties['ident'],
                datatype='string',
                datavalue={
                    "value": data["identification"],
                    "type" : "string"
                }
            )
            ident_claim = handler.Claim()
            ident_claim.mainsnak = ident_snak
            item.claims.add(ident_claim)

        abart_snak = handler.Snak(
            property_number=necessary_properties["abart_id"],
            datatype="string",
            datavalue={
                "value": data["abart_id"],
                "type" : "string"
            }
        )
        abart_claim = handler.Claim()
        abart_claim.mainsnak = abart_snak
        item.claims.add(abart_claim)

        if "nkaut" in data:
            nkaut_snak = handler.Snak(
                property_number=necessary_properties["nkaut"],
                datatype="external-id",
                datavalue={
                    "value":data["nkaut"],
                    "type": "string"
                }
            )
            nkaut_claim = handler.Claim()
            nkaut_claim.mainsnak = nkaut_snak
            item.claims.add(nkaut_claim)

        if "wikidata" in data:
            wikidata_snak = handler.Snak(
                property_number=necessary_properties["wikidata"],
                datatype="external-id",
                datavalue={
                    "value":data["wikidata"],
                    "type": "string"
                }
            )
            wikidata_claim = handler.Claim()
            wikidata_claim.mainsnak = wikidata_snak
            item.claims.add(wikidata_claim)

        if "viaf" in data:
            viaf_snak = handler.Snak(
                property_number=necessary_properties["viaf"],
                datatype="external-id",
                datavalue={
                    "value":data["viaf"],
                    "type": "string"
                }
            )
            viaf_claim = handler.Claim()
            viaf_claim.mainsnak = viaf_snak
            item.claims.add(viaf_claim)

        itemEnt = item.write(login=login_instance)

