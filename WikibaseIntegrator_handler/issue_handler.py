from handler import login_instance
from handler import wbi
from handler import general_properties
from handler import get_language_numeric_id
import handler
import query_handler
from wikibaseintegrator import wbi_helpers

class Issue:
    issue_properties = {"issue" : "P34", "issue_number": "P52"}
    qid = "Q11"
    issue_numeric_id = 11
    issue_qid = -1
    issue_title = ""

    def issue_in_db(self): # must return QID or -1
        self.issue_qid = query_handler.query_db(self.issue_title, "issue")
        return self.issue_qid

    def issue_insert_new(self, data: dict[str, str], lang: str):
        # minimal format of the data {'label': 'smth', (opt)'label_cs' : 'smth', 'description' : 'smth'}

        item = wbi.item.new()
        label = data["issue_title"]
        item.labels.set(language='en', value=label)


        #instance of
        instance_snak = handler.Snak(
            property_number=general_properties["instance_of"],
            datatype="wikibase-item",
            datavalue={
                "value": {
                    "entity-type": "item",
                    "numeric-id": self.issue_numeric_id,
                    "id": self.qid
                },
                "type": "wikibase-entityid"
            }
        )
        instance_claim = handler.Claim()
        instance_claim.mainsnak = instance_snak

        #issue
        issue_snak = handler.Snak(
            property_number=self.issue_properties["issue"],
            datatype="string",
            datavalue={
                "value": data["issue_number"],
                "type": "string"
            }
        )
        issue_claim=handler.Claim()
        issue_claim.mainsnak = issue_snak

        #part of
        part_of_snak = handler.Snak(
            property_number=general_properties["part_of"],
            datatype="wikibaseitem",
            datavalue={
                "value": {
                    "entity-type": "item",
                    "numeric-id": data["volume_numeric_id"],
                    "id": "Q" + str(data["volume_numeric_id"])
                },
                "type" : "wikibase-entityid"
            }
        )
        part_of_claim = handler.Claim()
        part_of_claim.mainsnak = part_of_snak

        #title
        title_snak = handler.Snak(
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
        title_claim.mainsnak = title_snak

        #lang
        lang_numeric_id = get_language_numeric_id(lang)
        lang_qid = "Q" + str(lang_numeric_id)
        lang_snak = handler.Snak(
            property_number=general_properties["lang_of_work_or_name"],
            datatype="wikibase-item",
            datavalue={
                "value": {
                    "entity-type": "item",
                    "numeric-id": lang_numeric_id,
                    "id": lang_qid
                },
                "type": "wikibase-entityid"
            }
        )
        lang_claim = handler.Claim()
        lang_claim.mainsnak = lang_snak

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

        #author
        if data["author"] != "":
            author_snak = handler.Snak(
                property_number=general_properties["author"],
                datatype="monolingualtext",
                datavalue={
                    "value": {
                        "text" : data["author"],
                        "language" : lang
                    },
                    "type" : "monolingualtext"
                }
            )
            author_claim = handler.Claim()
            author_claim.mainsnak = author_snak
            item.add_claims([author_claim])

        #publisher name
        if data["publisher"] != "":
            publisher_snak = handler.Snak(
                property_number=general_properties["publisher_name"],
                datatype="monolingualtext",
                datavalue={
                    "value": {
                        "text" : data["publisher"],
                        "language" : lang
                    },
                    "type" : "monolingualtext"
                }
            )
            publisher_claim = handler.Claim()
            publisher_claim.mainsnak = publisher_snak
            item.add_claims([publisher_claim])

        #contributor
        if data["contributor"] != "":
            contributor_snak = handler.Snak(
                property_number=general_properties["contributor"],
                datatype="monolingualtext",
                datavalue={
                    "value": {
                        "text" : data["contributor"],
                        "language" : lang
                    },
                    "type" : "monolingualtext"
                }
            )
            contributor_claim = handler.Claim()
            contributor_claim.mainsnak = contributor_snak
            item.add_claims([contributor_claim])

        item.add_claims([instance_claim, issue_claim, part_of_claim, title_claim, lang_claim])
        itemEnt = item.write(login=login_instance)



