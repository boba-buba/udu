import csv
import pandas as ps
from handler import login_instance
from handler import wbi
import handler
from handler import general_properties
import mapping
from human_handler import Human
#file_name = r"C:\Users\ncoro\Downloads\research_artists.csv"
#file_name = r"C:\Users\ncoro\source\repos\udu\WikibaseIntegrator_Artists_Abart\research_artists_trying.csv"
file_name = r"C:\Users\ncoro\source\repos\udu\WikibaseIntegrator_Artists_Abart\dummy_ex.csv"
#IdOsoby;Prijmeni;Jmeno;DalsiPrijmeni;DruheJmeno;Pseudonymy;Sifry;DatumNarozeniDen;DatumNarozeniMesic;DatumNarozeniRok;ObecNarozeni;StatNarozeni;DatumUmrtiDen;DatumUmrtiMesic;DatumUmrtiRok;ObecUmrti;StatUmrti;Identifikace;Narodnost;Pohlavi;NKAUT;WIKIDATA;VIAF

def parse_date(data, name):
    #yyyy mm dd
    dates_dict = {}
    if len(data) == 3: #dd mm yyyy
        if len(data[0]) == 1:
            data[0] = '0'+data[0]
        if len(data[1]) == 1:
            data[1] = '0'+data[1]
        dates_dict["precision_"+name] = 11
        dates_dict[name] = f"+{data[2]}-{data[1]}-{data[0]}T00:00:00Z"
    elif len(data) == 2:
        if len(data[0]) == 1:
            data[0] = '0'+data[0]
        dates_dict["precision_"+name] = 10
        dates_dict[name] = f"+{data[1]}-{data[0]}-00T00:00:00Z"
    else:
        dates_dict["precision_"+name] = 9
        dates_dict[name] = f"+{data[0]}-00T00:00:00Z"
    return dates_dict


def parse_country(country_name):
    l = country_name.split('(')
    if len(l) == 1:
        return country_name
    country_map = l[0][:-1]
    return  mapping.country_mapping[country_map]


def parse_row(row):
    artist_data = {"abart_id": row["IdOsoby"]}
    if (len(row["Prijmeni"])> 0):
        artist_data["surname"] = row["Prijmeni"]
    if (len(row["Jmeno"]) > 0):
        artist_data["name"] = row["Jmeno"]

    sec_surname = row["DalsiPrijmeni"]
    if (len(sec_surname) > 0):
        artist_data["second_surname"] = sec_surname

    sec_name = row["DruheJmeno"]
    if (len(sec_name) > 0):
        artist_data["second_name"] = sec_name

    pseud = row["Pseudonymy"].split(', ')
    if (len(pseud) > 0 and len(pseud[0]) > 0 ):
        artist_data["pseuds"] = pseud

    sifry = row["Sifry"].split(', ')
    if len(sifry) > 0 and len(sifry[0]) > 0:
        artist_data["aliases"] = sifry

    birth_date = []
    day = row["DatumNarozeniDen"]
    month = row["DatumNarozeniMesic"]
    year = row["DatumNarozeniRok"]
    if (len(day) > 0):
        birth_date.append(day)
    if (len(month) > 0):
        birth_date.append(month)
    if (len(year) > 0):
        birth_date.append(year)
    if len(birth_date) > 0:
        birth = parse_date(birth_date, "birth_date")
        artist_data.update(birth)

    birth_place = row["ObecNarozeni"]
    if len(birth_place) > 0:
        artist_data["birth_place"] = birth_place

    birth_country = row["StatNarozeni"]
    if len(birth_country) > 0:
        artist_data["birth_country"] = parse_country(birth_country)


    death_date = []
    day = row["DatumUmrtiDen"]
    month = row["DatumUmrtiMesic"]
    year = row["DatumUmrtiRok"]
    if (len(day) > 0):
        death_date.append(day)
    if (len(month) > 0):
        death_date.append(month)
    if (len(year) > 0):
        death_date.append(year)
    if len(death_date)>0:
        death = parse_date(death_date, "death_date")
        artist_data.update(death)

    death_place = row["ObecUmrti"]
    if len(death_place) > 0:
        artist_data["death_place"] = death_place

    death_country = row["StatUmrti"]
    if len(death_country) > 0:
        artist_data["death_country"] = parse_country(death_country)

    identifications = []
    ##
    ethnicity = row["Narodnost"]
    if len(ethnicity) > 0:
        artist_data["ethnicity"] = mapping.ethnicity_mapping[ethnicity]

    sex = row["Pohlavi"]
    if len(sex) > 0:
        artist_data["sex"] = mapping.sex_mapping[sex]

    nkaut = row["NKAUT"]
    if len(nkaut) > 0:
        artist_data["nkaut"] = nkaut

    wikidata = row["WIKIDATA"]
    if len(wikidata) > 0:
        artist_data["wikidata"] = wikidata

    viaf = row["VIAF"]
    if len(viaf) > 0:
        artist_data["viaf"] = viaf
    #print(row["\ufeffIdOsoby"])
    Human.person_insert_new(artist_data)


with open(file_name, 'r', encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
           human_data = parse_row(row)

        f.flush()