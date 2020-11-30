import pandas as pd
import psycopg2
import psycopg2.extras
import math
import pymongo


conn = psycopg2.connect(connection_string, cursor_factory=psycopg2.extras.DictCursor)

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]

def tearDown(self):
    print('done')

def query( query, parameters=()):
    cursor = conn.cursor()
    cursor.execute(query, parameters)
    return cursor.fetchall()


###TODO NoSQL Database Installation


#Import data
#https://stackoverflow.com/a/56241768
#
def csv_to_json(filename, header=None):
    data = pd.read_csv(filename, header=header)
    return data.to_dict('records')


def insert_county_towns(county_town_data):
    mycol = mydb["county_towns"]
    cursor = conn.cursor()
    for item in county_town_data:
        county = item.split(":::")[0]
        town = item.split(":::")[1]
        print(item, county, town)
        cursor.execute("INSERT INTO county_information(county_name, town_name) VALUES(%s,%s)", (county, town))
        mycol.insert_one({"county" : county, "town" : town})
    conn.commit()


def insert_planned_trout_stocking(current_season_spring_trout_stocking_data):
    mycol = mydb["stocking_information"]
    cursor = conn.cursor()
    for item in current_season_spring_trout_stocking_data[1:]:
        year = item[0]
        # dec = item[1]
        county = item[2].lower().title()
        town = item[3].lower().title()
        waterbody = item[4]
        month = item[5]
        number = item[6]
        species_name = item[7]
        size_inches = item[8]
        print(item, county, town)
        cursor.execute("INSERT INTO stocking_information(year, waterbody, month, number, species, size_inches, future, county_name, town_name) "
                       "VALUES(%s,%s,%s,%s,%s,%s,TRUE,%s,%s)", (year, waterbody, month, number, species_name, size_inches, county, town))
        mycol.insert_one({"year": year, "waterbody": waterbody, "month" : month, "number" : number, "species_name": species_name, "size_inches":size_inches, "Future": True, "county":county, "town":town})

    conn.commit()


def insert_actual_fish_stocking(fish_stocking_lists_2011_data):
    mycol = mydb["stocking_information"]
    cursor = conn.cursor()
    for item in fish_stocking_lists_2011_data[1:]:
        year = item[0]
        # dec = item[1]
        county = item[1].lower().title()
        town = str(item[3]).lower().title()
        waterbody = item[2]
        month = item[4]
        if math.isnan(float(str(item[5]))):
            number = 0
        else:
            number = int(item[5])
        species_name = item[6]
        size_inches = item[7]

        print(item, county, town)
        cursor.execute("INSERT INTO stocking_information(year, waterbody, month, number, species, size_inches, future, county_name, town_name) "
                       "VALUES(%s,%s,%s,%s,%s,%s,FALSE,%s,%s)", (year, waterbody, month, number, species_name, size_inches, county, town))
        mycol.insert_one({"year": year, "waterbody": waterbody, "month" : month, "number" : number, "species_name": species_name, "size_inches":size_inches, "future" : False, "county":county, "town":town})

    conn.commit()


def insert_national_register_of_historic_places_data(national_register_of_historic_places_data):
    mycol1 = mydb["county_historic"]
    cursor = conn.cursor()
    x = 0
    for item in national_register_of_historic_places_data[1:]:

        resource_name = item[0]
        county = item[1].lower().title()

        if not isinstance(item[2], str) and math.isnan(float(str(item[2]))):
             nrdate = '11/11/1111'
        else:
            nrdate = item[2]
        nrnumber = item[3]
        location = item[6]

        print(item, county, resource_name)
        string = "Select * from county_historic where national_register_number = '" + nrnumber + "'"
        cursor.execute(string)
        results = cursor.fetchall()
        if len(results) > 0:
            continue

        cursor.execute("INSERT INTO county_historic(resource_name, national_register_date, national_register_number, location, county_name) "
                       "VALUES(%s,%s,%s,%s,%s)", (resource_name, nrdate, nrnumber, location , county))
        mycol1.insert_one({"resource_name": resource_name, "nrdate": nrdate, "nrnumber" : nrnumber, "location" : location, "county": county})


    conn.commit()



def insert_rec_fishing_rivers_and_streams_data(rec_fishing_rivers_and_streams_data):
    mycol = mydb["waterbody_information"]

    cursor = conn.cursor()
    for item in rec_fishing_rivers_and_streams_data[1:]:
        waterbody_name = item[0]
        fish_species_present = item[1].lower().title()
        comments = item[2]
        special_regulations = item[3]
        county_name = item[4]
        types_of_public_access   = item[5]
        public_fishing_access_owner = item[6]
        waterbody_information  = item[7]
        lat = item[8]
        long =  item[9]
        location = item[10]

        string = "Select * from waterbody_information where latitude = '" + lat + "'" + "and longitude = '" + long + "'"
        cursor.execute(string)
        results = cursor.fetchall()
        if len(results) > 0:
            continue

        print(item)

        cursor.execute("INSERT INTO waterbody_information(waterbody_name, fish_species_present, comments, special_regulations, types_of_public_access, public_fishing_access_owner, latitude, longitude, location, waterbody_information, county_name) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                       (waterbody_name, fish_species_present, comments, special_regulations, types_of_public_access, public_fishing_access_owner, lat, long, location, waterbody_information, county_name))
        mycol.insert_one(   {"waterbody_name": waterbody_name, "fish_species_present": fish_species_present, "comments" : comments, "special_regulations" : special_regulations, "types_of_public_access": types_of_public_access, "lat" : lat, "long" : long, "waterbody_information":waterbody_information, "county_name":county_name})

    conn.commit()

    pass


def import_data():
    county_town_data = set()
    current_season_spring_trout_stocking_data = csv_to_json("data/Current_Season_Spring_Trout_Stocking.csv")
    for item in current_season_spring_trout_stocking_data:
        mango = ""
        mango += item[2].lower().title()
        mango += ":::"
        mango += item[3].lower().title()
        # print(mango)
        county_town_data.update([mango])
    fish_stocking_lists_2011_data             = csv_to_json("data/Fish_Stocking_Lists__Actual___Beginning_2011.csv")
    for item in fish_stocking_lists_2011_data:
        mango = ""
        mango += item[1].lower().title()
        mango += ":::"
        mango += str(item[3]).lower().title()
        county_town_data.update([mango])
    national_register_of_historic_places_data = csv_to_json("data/National_Register_of_Historic_Places.csv")
    for item in national_register_of_historic_places_data:
        # county_town_data.update([item[1],""])
        print(item[1])
    rec_fishing_rivers_and_streams_data       = csv_to_json("data/Recommended_Fishing_Rivers_And_Streams.csv")
    # for item in rec_fishing_rivers_and_streams_data:
    #     county_town_data.update([item[4],""])

    insert_county_towns(county_town_data)
    insert_planned_trout_stocking(current_season_spring_trout_stocking_data)
    insert_actual_fish_stocking(fish_stocking_lists_2011_data)
    insert_national_register_of_historic_places_data(national_register_of_historic_places_data)
    print(mydb.list_collection_names())

    # insert_rec_fishing_rivers_and_streams_data(rec_fishing_rivers_and_streams_data)



import_data()


