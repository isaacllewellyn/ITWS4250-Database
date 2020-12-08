#Information Page / Landing Page
#Used to display content to a user when first starting the applicationn
import psycopg2
import psycopg2.extras
import random
connection_string = "host='localhost' dbname='dbms_final_project' user='dbms_project_user' password='dbms_password'"
conn = psycopg2.connect(connection_string, cursor_factory=psycopg2.extras.DictCursor)

def review_stocking_area():
    year = input("Enter the year to examine [2011-2020]: ")
    bod_num = input("Enter the number of water bodies to examine: ")
    print("\n")
    cursor = conn.cursor()
    cursor.execute("SELECT sum(number) as sum, waterbody FROM stocking_information WHERE year = %s GROUP BY waterbody order by sum desc LIMIT %s", (year, bod_num,))
    result = cursor.fetchall()
    count = 1
    waterbody_names = []
    for x in result:
        print("#" + str(count) + " Stocked Fish: " + str(x[0]) + "  \tLocation: " + str(x[1]))
        waterbody_names.append(x[1])
        count = count + 1
    
    selected_waterbody= input("\nEnter the number of the waterbody you want to list, or enter 'b' to return the start menu: ")
    if (selected_waterbody == 'b'):
        info_page()
    print("\nMake a selection from the following options:\n1. 'i' for more info on the waterbody \n2. 's' for more stocking info\n")
    selected_option = input("Enter the option you want to use: ")
    if (selected_option == 'i'):
        waterbody_name = (waterbody_names[int(selected_waterbody)-1])
        cursor.execute("SELECT * FROM stocking_information WHERE waterbody = %s", (waterbody_name,))
        result = cursor.fetchall()
        fish_set = set()
        for x in result:
            county_name = x[8]
            fish_set.add(x[5])
        print(waterbody_name + " is located in " + county_name + " County.")
        print(str(len(fish_set)) + " type(s) of trout have been recorded in this waterbody, including ", end = '')
        count = 0
        for y in (fish_set):
            print(y, end = '')
            count = count + 1
            if len(fish_set) > 1 and count != len(fish_set):
                print(" and ", end = '.')


    elif (selected_option == 's'):
        waterbody_name = (waterbody_names[int(selected_waterbody)-1])
        cursor.execute("SELECT species, number  FROM stocking_information WHERE year = %s AND waterbody = %s", (year, waterbody_name,))
        result = cursor.fetchall()
        print("In " + str(year) + " the following trout were stocked in " + str(waterbody_name))
        for x in result:
            print(str(x[0]) + ": " + str(x[1]))
    input("\nPress enter to go to main menu: ")
    info_page()

def get_county_options():
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT county_name FROM stocking_information ORDER BY county_name ASC")
    count = 1
    county_list = []
    result = cursor.fetchall()
    for x in result:
        print("#" + str(count) + " " + str(x[0]))
        county_list.append(x[0])
        count = count + 1  
    selected_county = input("Select a county number to get a list of recommended trout fishing spots, or enter 'b' to return the start menu: ")
    if (selected_county == 'b'):
        info_page()
    selected_county =  int(selected_county) - 1
    selected_county_name = county_list[selected_county]
    cursor.execute("SELECT DISTINCT (waterbody_name), county_name, Waterbody_information FROM waterbody_information WHERE county_name ilike %s ORDER BY county_name ASC", (selected_county_name,))
    result = cursor.fetchall()
    print("\nThe following waterbodies are recommended for trout fishing in " + selected_county_name + " County:")
    for x in result:
        print(x[0] + "\t  Site information: " + x[2] )

    cursor.execute(
        "SELECT DISTINCT waterbody,  species FROM stocking_information WHERE county_name ilike %s",
        (selected_county_name,))
    result = cursor.fetchall()
    print("\nThe following stocked fishing spots are recommended in " + selected_county_name + " County:")
    for x in result:
        print("Stocked Body " + x[0] + ", Fish type: "+  x[1])

    cursor.execute(
        "SELECT resource_name FROM county_historic WHERE county_name ilike %s ",
        (selected_county_name,))
    result = cursor.fetchall()
    print("\nHere are 10 random historic places in the county for you to check out in the county: " + selected_county_name + ":")
    i = 0
    random.shuffle(result)
    for x in result:
        i = i + 1
        if i > 10:
            continue
        print(x[0])


    input("\nPress enter to go to main menu: ")
    info_page()


def get_newest_historic_places():
    cursor = conn.cursor()
    cursor.execute(
        "select Resource_Name, National_Register_Date, County_name from County_historic order by National_Register_Date desc limit 10")
    result = cursor.fetchall()
    print(
        "\nHere are the top 10 newest historic places in New York:")
    for row in result:
        print(row[0], " Register Date: " + str(row[1]) +" County: " + row[2])

    date = input("\n Enter a date to check for the newest historic places up untill that date, otherwise, press enter to go to the main menu\n (year) or (year/mm/day) : ")
    if len(str(date)) == 4:
        date = date+"-01-01"
    cursor.execute(
        "select Resource_Name, National_Register_Date, County_name from County_historic where National_Register_Date < %s order by National_Register_Date desc limit 10", (date,))
    result = cursor.fetchall()
    print(
        "\nHere are the top 10 newest historic places in New York before " + date)
    for row in result:
        print(row[0], " Register Date: " + str(row[1]) +" County: " + row[2])

    input("Press enter to return back to the main menu")
    info_page()

def get_spots_in_town():
    print("Here's a list of all NYS counties:")
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT county_name FROM County_information ORDER BY county_name ASC")
    count = 1
    county_list = []
    result = cursor.fetchall()
    for x in result:
        print("#" + str(count) + " " + str(x[0]))
        county_list.append(x[0])
        count = count + 1  
    selected_county = input("Select a county number, or enter 'b' to return the start menu: ")
    if (selected_county == 'b'):
        info_page()
    selected_county =  int(selected_county) - 1
    selected_county_name = county_list[selected_county]
    cursor.execute("SELECT DISTINCT town_name FROM County_information WHERE county_name = %s ORDER BY town_name ASC", (selected_county_name,))
    count = 1
    town_list = []
    result = cursor.fetchall()
    for x in result:
        print("#" + str(count) + " " + str(x[0]))
        town_list.append(x[0])
        count = count + 1      
    selected_town = input("\nSelect a town by number: ")
    selected_town =  int(selected_town) - 1
    selected_town_name = town_list[selected_town]
    cursor.execute(
        "SELECT DISTINCT(a.waterbody), B.town_name, B.county_name FROM stocking_information a, county_information b WHERE a.county_name = %s and b.town_name = %s and a.county_name = b.county_name and a.town_name = b.town_name;", (selected_county_name,selected_town_name,))
    result = cursor.fetchall()
    print("Check out these spots for stocked fishing in " + selected_town_name + ":")
    for row in result:
        print(row[0])
    selected_county = input("Enter 'b' to return the start menu, or enter anything else to find the largest single trout recorded in your searched town: ")
    if (selected_county == 'b'):
        info_page()
    #This search ignores ranges (ex: 9-10 inches) and only returns the largest trout recorded)
    cursor.execute("SELECT DISTINCT(a.waterbody), CAST(size_inches AS float) FROM stocking_information a, county_information b WHERE a.county_name = %s and b.town_name = %s and a.county_name = b.county_name and a.town_name = b.town_name and size_inches NOT LIKE '%%-%%' ORDER BY size_inches DESC LIMIT 1;", (selected_county_name,selected_town_name,))
    result = cursor.fetchone()
    print("The largest recorded trout in " + selected_town_name + " was " +  str(result[1]) + " inches large in the " + str(result[0]) + " waterbody.")
    info_page()
    
    
def menu_select(menu_num):
    if (menu_num == 1):
        review_stocking_area()
    elif (menu_num == 2):
        get_county_options()
    elif (menu_num == 3):
        get_newest_historic_places()
    elif (menu_num == 4):
        get_spots_in_town()
    else:
        print("Error, selection is not valid!")
        menu_enter()
        
def menu_enter():
    menu_num = int(input("Enter a number: "))
    menu_select(menu_num)
    
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
                    >::::::::;;\\\\\\                 To select a menu, enter a number: 
                      ''\\\\\\\\\\'' ';\\                    1: Review Top Stocking Areas
                                                                2: Get List of Counties To Explore
                                                                    3: Get the newest historic places to check out!
                                                                4. Get a list of stocked places in a town, and
                                                                        largest trout recorded in a waterbody 
                                                   /         
                                                  /--\\ /                                      \\
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
    menu_enter()

info_page()



