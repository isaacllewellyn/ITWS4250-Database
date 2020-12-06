
CREATE TABLE IF NOT EXISTS County_information (

County_name          TEXT ,
Town_name          TEXT,
PRIMARY KEY (County_name, Town_name)

);

CREATE TABLE IF NOT EXISTS Stocking_information (
StockingIDD serial primary key,
Year         INT,
Waterbody         TEXT,
Month        varchar(40),
Number        INT,
Species           TEXT,
Size_Inches       TEXT,
Future         boolean,
County_name          TEXT,
Town_name          TEXT,
FOREIGN KEY (County_name, Town_name)
REFERENCES County_information (County_name, Town_name)
);

CREATE TABLE IF NOT EXISTS Waterbody_information (

Waterbody_Name               TEXT,
Fish_Species_Present       TEXT,
Comments                TEXT,
Special_Regulations        TEXT,
Types_of_Public_Access     TEXT,
Public_Fishing_Access_Owner TEXT,
latitude                float,
longitude               float,
Location                POINT,
Waterbody_information  text,
County_name          TEXT,
PRIMARY KEY(Waterbody_Name, latitude, longitude)

);

CREATE TABLE IF NOT EXISTS County_historic (

Resource_Name             TEXT,
National_Register_Date     DATE,
National_Register_Number   TEXT  PRIMARY KEY,
Location            point,
County_name          TEXT

);

