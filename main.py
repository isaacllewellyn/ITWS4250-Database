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
            # print(x)
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



def menu_select(menu_num):
    if (menu_num == 1):
        review_stocking_area()
    elif (menu_num == 2):
        get_county_options()
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
                      ''\\\\\\\\\\'' ';\\                          1: Review Top Stocking Areas
                                                             2: Get List of Counties To Explore
                                                             
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

###Todo View for top stocking areas
###Todo View for county explorer
###Todo View for fishing spots near histoical landmarks?
###



