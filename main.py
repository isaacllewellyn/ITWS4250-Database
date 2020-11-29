import pandas as pd
import psycopg2
import psycopg2.extras
import math


conn = psycopg2.connect(connection_string, cursor_factory=psycopg2.extras.DictCursor)

def tearDown(self):
    print('done')

def query( query, parameters=()):
    cursor = conn.cursor()
    cursor.execute(query, parameters)
    return cursor.fetchall()


###TODO NoSQL Database Installation

#Information Page / Landing Page
#Used to display content to a user when first starting the applicationn
def info_page():

    print("""                                                                                                                       
                                                                                           ____
                                                                                         /  o   \\
                                                                                       < ____     \\                  _
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|     |~~~~~~_~~~~~~~~/
^^^^ ^^^  ^^^   ^^^    ^^^^      ^^^^ ^^^  ^^^   ^^^    ^^^^      ^^^^ ^^^  ^^^   ^^^    ^^^^|     |^^^ /   \\^^^  |
^^^^      ^^^^     ^^^    ^^     ^^^^      ^^^^     ^^^    ^^     ^^^^      ^^^^     ^^^    ^^     ^^^^      ^^^^     ^
^^      ^^^^      ^^^    ^^^^^^  ^^      ^^^^      ^^^    ^^^^^^  ^^      ^^^^      ^^^    ^^^^^^  ^^      ^^^^      ^^
               .:/
            ,,///;,   ,;/
          o:::::::;;///
         >::::::::;;\\\\\\                                                                                ..\\,
           ''\\\\\\\\\\'' ';\\                                                                            >='   ('>
                                                                                                      '''/''          
                          .:/
                       ,,///;,   ,;/
                     o:::::::;;///          Welcome To Our Database Systems Project!
                    >::::::::;;\\\\\\
                      ''\\\\\\\\\\'' ';\\
                                                   /
                                                  /--\\ /                                          \\
                                                 <o)  =<                                      \\ /--\\
                                                  \\__/ \\                                      >=  (o>
               \\:.                                 \\                                          / \\__/  T~~
        \\;,   ,;\\\\\\,,                             / \\                                             /   |
          \\\\\\;;:::::::o                          <')_=<                                              /^\\
          ///;;::::::::<                          \\_/                                               /   \\
         /;` ``/////``                             \\                                    _   _   _  /     \\  _   _   _  
                                                                                       [ ]_[ ]_[ ]/ _   _ \\[ ]_[ ]_[ ] 
          \\                                                                            |_=__-_ =_|_[ ]_[ ]_|_=-___-__|
         / \\                 /,                   )            (                        | _- =  | =_ = _(   |= _=   |
       >=_('>               <')=<                (              )                   )   |= -[]  |- = _ = )  |_-=_[] |
         \\_/                 \\`                   )            (              (    (    | =_    |= - ___(   | =_ =  |
          /                 (                    (              )              )    )   )=  []- |-  /| | )  |=_ =[] |
                             )                    )            (              (    (   (|- =_   | =| | |(|  |- = -  |
                            (                    (              )              )    )   )_______|__|_|_| )__|_______|

""")

#Import data
#https://stackoverflow.com/a/56241768
#
def csv_to_json(filename, header=None):
    data = pd.read_csv(filename, header=header)
    return data.to_dict('records')


def insert_county_towns(county_town_data):
    cursor = conn.cursor()
    for item in county_town_data:
        county = item.split(":::")[0]
        town = item.split(":::")[1]
        print(item, county, town)
        cursor.execute("INSERT INTO county_information(county_name, town_name) VALUES(%s,%s)", (county, town))
        # cursor.execute("INSERT INTO county(recipe, quantity, kosher) VALUES('Chicken Sandwich', 1, FALSE)")
    conn.commit()

    pass


def insert_planned_trout_stocking(current_season_spring_trout_stocking_data):
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
    conn.commit()


def insert_actual_fish_stocking(fish_stocking_lists_2011_data):
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
    conn.commit()

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
    pass

info_page()


def setUp():
    import_data()



setUp()


