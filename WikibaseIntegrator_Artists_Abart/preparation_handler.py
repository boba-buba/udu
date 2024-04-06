import csv
import pandas as ps
from handler import login_instance
from handler import wbi
import handler
from handler import general_properties
file_name = r"C:\Users\ncoro\Downloads\research_artists.csv"
output_file = r"ethicities.txt"
ethnicities = []
with open(file_name, 'r', encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=';')


        for row in reader:
            eth = row["Narodnost"]
            if eth not in ethnicities:
                  ethnicities.append(eth)
        f.flush()

out = open(output_file, "a",  encoding="utf-8")
for eth in ethnicities:
      out.write(eth)
      out.write("\n")
out.close()

# description = "Ethnic group"

# def create_ethnic_group(name):
#     item = wbi.item.new()
#     item.labels.set(language='en', value=name)

#     #instance of
#     instance_snack = handler.Snak(
#         property_number=general_properties["instance_of"],
#         datatype="wikibase-item",
#         datavalue={
#             "value": {
#                 "entity-type": "item",
#                 "numeric-id": 517,
#                 "id": "Q517"
#             },
#             "type": "wikibase-entityid"
#         }
#     )
#     instance_claim = handler.Claim()
#     instance_claim.mainsnak = instance_snack

#     item.add_claims([instance_claim])

#     itemEnt = item.write(login=login_instance)
#     print(name)

# with open(output_file, 'r', encoding="utf-8") as f:
#     Lines = f.readlines()
#     for line in Lines:
#         create_ethnic_group(line[:-1])
#     f.flush()

## Countries
countries = []
count_file = r"countries.txt"
with open(file_name, 'r', encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=';')


        for row in reader:
            c = row["StatNarozeni"]
            if c not in countries:
                  countries.append(c)
            c2 = row["StatUmrti"]
            if c2 not in countries:
                  countries.append(c2)
        f.flush()


out = open(count_file, "a",  encoding="utf-8")
for c in countries:
      out.write(c)
      out.write("\n")
out.close()

# def create_ethnic_group(name):
#     item = wbi.item.new()
#     item.labels.set(language='en', value=name)

#     #instance of
#     instance_snack = handler.Snak(
#         property_number=general_properties["instance_of"],
#         datatype="wikibase-item",
#         datavalue={
#             "value": {
#                 "entity-type": "item",
#                 "numeric-id": 18,
#                 "id": "Q18"
#             },
#             "type": "wikibase-entityid"
#         }
#     )
#     instance_claim = handler.Claim()
#     instance_claim.mainsnak = instance_snack

#     item.add_claims([instance_claim])

#     itemEnt = item.write(login=login_instance)
#     print(name)

# with open(count_file, 'r', encoding="utf-8") as f:
#     Lines = f.readlines()
#     for line in Lines:
#         create_ethnic_group(line[:-1])
#     f.flush()


#output_file = r"occs.txt"
# occupations = []
# with open(file_name, 'r', encoding="utf-8") as f:
#         reader = csv.DictReader(f, delimiter=';')
#         for row in reader:
#             occs = row["Identifikace"].split(',')
#             for o in occs:
#                 if o not in occupations:
#                     occupations.append(o)

#         f.flush()
# print(len(occupations))
# out = open(output_file, "a",  encoding="utf-8")

# for occ in occupations:
#       out.write(occ)
#       out.write("\n")
# out.close()



