import pandas as pd
import psycopg2
import psycopg2.extras
import math
import pymongo

# Connection string used to login to PostgreSQL and connectionn
connection_string = "host='localhost' dbname='dbms_final_project' user='dbms_project_user' password='dbms_password'"
conn = psycopg2.connect(connection_string, cursor_factory=psycopg2.extras.DictCursor)

# Mongod connection string and client
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]


# Import data
# https://stackoverflow.com/a/56241768
#
def csv_to_json(filename, header=None):
    data = pd.read_csv(filename, header=header)
    return data.to_dict('records')


# Insert County town Pairs
def insert_county_towns(county_town_data):
    mycol = mydb["county_towns"]
    mycol.drop()
    cursor = conn.cursor()
    for item in county_town_data:
        # Parse data into each collum
        county = item.split(":::")[0]
        town = item.split(":::")[1]
        # Debug
        # print(item, county, town)
        # Insert data into databases
        cursor.execute("INSERT INTO county_information(county_name, town_name) VALUES(%s,%s) ON CONFLICT DO NOTHING", (county, town))
        mycol.insert_one({"county": county, "town": town})
    conn.commit()


# Insert planned trout stocking into the main stocking table
# Shared table with actual stocking dataset.
def insert_planned_trout_stocking(current_season_spring_trout_stocking_data):
    mycol = mydb["stocking_information"]
    mycol.drop()
    cursor = conn.cursor()
    for item in current_season_spring_trout_stocking_data[1:]:
        # Get collums from data
        year = item[0]
        county = item[2].lower().title()
        town = item[3].lower().title()
        waterbody = item[4]
        month = item[5]
        number = item[6]
        species_name = item[7]
        size_inches = item[8]
        print(item, county, town)
        # Insert data into databases
        cursor.execute(
            "INSERT INTO stocking_information(year, waterbody, month, number, species, size_inches, future, county_name, town_name) "
            "VALUES(%s,%s,%s,%s,%s,%s,TRUE,%s,%s) ON CONFLICT DO NOTHING",
            (year, waterbody, month, number, species_name, size_inches, county, town))
        mycol.insert_one(
            {"year": year, "waterbody": waterbody, "month": month, "number": number, "species_name": species_name,
             "size_inches": size_inches, "Future": True, "county": county, "town": town})
    conn.commit()


def insert_actual_fish_stocking(fish_stocking_lists_2011_data):
    mycol = mydb["stocking_information"]
    cursor = conn.cursor()
    for item in fish_stocking_lists_2011_data[1:]:
        # Get collum information
        year = item[0]
        # dec = item[1]
        county = item[1].lower().title()
        town = str(item[3]).lower().title()
        waterbody = item[2]
        month = item[4]
        # Check to see if they actually put in any data for stocking.
        if math.isnan(float(str(item[5]))):
            number = 0
        else:
            number = int(item[5])
        species_name = item[6]
        size_inches = item[7]
        # Debug
        print(item, county, town)
        # Insert data into databases
        cursor.execute(
            "INSERT INTO stocking_information(year, waterbody, month, number, species, size_inches, future, county_name, town_name) "
            "VALUES(%s,%s,%s,%s,%s,%s,FALSE,%s,%s) ON CONFLICT DO NOTHING",
            (year, waterbody, month, number, species_name, size_inches, county, town))
        mycol.insert_one(
            {"year": year, "waterbody": waterbody, "month": month, "number": number, "species_name": species_name,
             "size_inches": size_inches, "future": False, "county": county, "town": town})
    conn.commit()


def insert_national_register_of_historic_places_data(national_register_of_historic_places_data):
    mycol1 = mydb["county_historic"]
    mycol1.drop()
    cursor = conn.cursor()
    for item in national_register_of_historic_places_data[1:]:
        # Get collumn information
        resource_name = item[0]
        county = item[1].lower().title()
        # check for nan, set to wild date so we can know there is a problem
        if not isinstance(item[2], str) and math.isnan(float(str(item[2]))):
            nrdate = '11/11/1111'
        else:
            nrdate = item[2]
        nrnumber = item[3]
        location = item[6]
        # debug
        print(item, county, resource_name)
        # Double check for duplicate entries for historic places
        cursor.execute("Select * from county_historic where national_register_number = %s", (str(nrnumber),))
        results = cursor.fetchall()
        if len(results) > 0:
            continue
        # Insert data into databases
        cursor.execute(
            "INSERT INTO county_historic(resource_name, national_register_date, national_register_number, location, county_name) "
            "VALUES(%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING", (resource_name, nrdate, nrnumber, location, county))
        mycol1.insert_one({"resource_name": resource_name, "nrdate": nrdate, "nrnumber": nrnumber, "location": location,
                           "county": county})
    conn.commit()


# Insert data anout reccommended rivers and streams into the waterbody database
def insert_rec_fishing_rivers_and_streams_data(rec_fishing_rivers_and_streams_data):
    mycol = mydb["waterbody_information"]
    mycol.drop()
    cursor = conn.cursor()
    for item in rec_fishing_rivers_and_streams_data[1:]:
        # Get column information
        waterbody_name = item[0]
        fish_species_present = item[1].lower().title()
        comments = item[2]
        special_regulations = item[3]
        county_name = item[4]
        types_of_public_access = item[5]
        public_fishing_access_owner = item[6]
        waterbody_information = item[7]
        lat = item[8]
        long = item[9]
        location = item[10]
        # check for similar locations / duplications to ignore
        string = "Select * from waterbody_information where latitude = %s and longitude = %s"
        cursor.execute(string, (lat, long,))
        results = cursor.fetchall()
        if len(results) > 0:
            continue
        # inserts data to both databases
        cursor.execute(
            "INSERT INTO waterbody_information(waterbody_name, fish_species_present, comments, special_regulations, types_of_public_access, public_fishing_access_owner, latitude, longitude, location, waterbody_information, county_name) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING",
            (waterbody_name, fish_species_present, comments, special_regulations, types_of_public_access,
             public_fishing_access_owner, lat, long, location, waterbody_information, county_name))
        mycol.insert_one(
            {"waterbody_name": waterbody_name, "fish_species_present": fish_species_present, "comments": comments,
             "special_regulations": special_regulations, "types_of_public_access": types_of_public_access, "lat": lat,
             "long": long, "waterbody_information": waterbody_information, "county_name": county_name})
    conn.commit()
    pass


# Main import function
def import_data():
# We only want single versions of the county town pairs, so we use a set.
# For each dataset, extract the town and county info
    # Create the schema
    cursor = conn.cursor()
    print("loading schema")
    cursor.execute(open("schema.sql", "r").read())
    print("done loading schema")
    #Setup everything else
    county_town_data = set()
    current_season_spring_trout_stocking_data = csv_to_json("datasets/Current_Season_Spring_Trout_Stocking.csv")
    for item in current_season_spring_trout_stocking_data:
        mango = ""
        mango += item[2].lower().title()
        mango += ":::"
        mango += item[3].lower().title()
        # print(mango)
        county_town_data.update([mango])
    fish_stocking_lists_2011_data             = csv_to_json("datasets/Fish_Stocking_Lists__Actual___Beginning_2011.csv")
    for item in fish_stocking_lists_2011_data:
        mango = ""
        mango += item[1].lower().title()
        mango += ":::"
        mango += str(item[3]).lower().title()
        county_town_data.update([mango])
    national_register_of_historic_places_data = csv_to_json("datasets/National_Register_of_Historic_Places.csv")
    for item in national_register_of_historic_places_data:
        # county_town_data.update([item[1],""])
        print(item[1])
    rec_fishing_rivers_and_streams_data       = csv_to_json("datasets/Recommended_Fishing_Rivers_And_Streams.csv")
    # for item in rec_fishing_rivers_and_streams_data:
    #     county_town_data.update([item[4],""])

    insert_county_towns(county_town_data)
    insert_planned_trout_stocking(current_season_spring_trout_stocking_data)
    insert_actual_fish_stocking(fish_stocking_lists_2011_data)
    insert_national_register_of_historic_places_data(national_register_of_historic_places_data)
    print(mydb.list_collection_names())

    insert_rec_fishing_rivers_and_streams_data(rec_fishing_rivers_and_streams_data)



import_data()


