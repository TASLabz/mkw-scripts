# NOTE (xi): unfinished, currently only for the use of testing other scripts
#            that rely on this module

def vehicle(vehicle_id):
    """
    Translates vehicle_id to a plain vehicle name.
    """
    vehicles = ["Standard Kart S", "Standard Kart M", "Standard Kart L",
                "Booster Seat", "Classic Dragster", "Offroader", "Mini Beast",
                "Wild Wing", "Flame Flyer", "Cheep Charger", "Super Blooper",
                "Piranha Prowler", "Tiny Titan", "Daytripper", "Jetsetter",
                "Blue Falcon", "Sprinter", "Honeycoupe", "Standard Bike S",
                "Standard Bike M", "Standard Bike L", "Bullet Bike",
                "Mach Bike", "Flame Runner", "Bit Bike", "Sugarscoot",
                "Wario Bike", "Quacker", "Zip Zip", "Shooting Star",
                "Magikruiser", "Sneakster", "Spear", "Jet Bubble",
                "Dolphin Dasher", "Phantom"]
    
    return vehicles[vehicle_id]

def character(character_id):
    """
    Translates vehicle_id to a plain character name.
    """
    characters = ["Mario", "Baby Peach", "Waluigi", "Bowser", "Baby Daisy",
                  "Dry Bones", "Baby Mario", "Luigi", "Toad", "Donkey Kong", "Yoshi",
                  "Wario", "Baby Luigi", "Toadette", "Koopa Troopa", "Daisy", "Peach",
                  "Birdo", "Diddy Kong", "King Boo", "Bowser Jr.", "Dry Bowser",
                  "Funky Kong", "Rosalina", "Mii Outfit A (M | Light)",
                  "Mii Outfit A (F | Light)", "Mii Outfit B (M | Light)",
                  "Mii Outfit B (F | Light)", "Mii Outfit C (M | Light)",
                  "Mii Outfit C (F | Light)", "Mii Outfit A (M | Medium)",
                  "Mii Outfit A (F | Medium)", "Mii Outfit B (M | Medium)",
                  "Mii Outfit B (F | Medium)", "Mii Outfit C (M | Medium)",
                  "Mii Outfit C (F | Medium)", "Mii Outfit A (M | Heavy)",
                  "Mii Outfit A (F | Heavy)", "Mii Outfit B (M | Heavy)",
                  "Mii Outfit B (F | Heavy)", "Mii Outfit C (M | Heavy)",
                  "Mii Outfit C (F | Heavy)"]
    
    return characters[character_id]

def course(course_id):
    """
    Translates vehicle_id to a plain course name.
    """
    courses = ["Mario Circuit", "Moo Moo Meadows", "Mushroom Gorge", "Grumble Volcano",
               "Toad's Factory", "Coconut Mall", "DK Summit", "Wario's Gold Mine",
               "Luigi Circuit", "Daisy Circuit", "Moonview Highway", "Maple Treeway",
               "Bowser's Castle", "Rainbow Road", "Dry Dry Ruins", "Koopa Cape",
               "GCN Peach Beach", "GCN Mario Circuit", "GCN Waluigi Stadium",
               "GCN DK Mountain", "DS Yoshi Falls", "DS Desert Hills",
               "DS Peach Gardens", "DS Delfino Square", "SNES Mario Circuit 3",
               "SNES Ghost Valley 2", "N64 Mario Raceway", "N64 Sherbet Land",
               "N64 Bowser's Castle", "N64 DK's Jungle Parkway", "GBA Bowser Castle 3",
               "GBA Shy Guy Beach"]
    return courses[course_id]

def course_abbreviation(course_id):
    """
    Translates vehicle_id to a plain course abbreviation.
    """
    courses = ["MC", "MMM", "MG", "GV", "TF", "CM", "DKS", "WGM", "LC", "DC", "MH",
               "MT", "BC", "RR", "DDR", "KC", "rPB", "rMC", "rWS", "rDKM", "rYF", "rDH",
               "rPG", "rDS", "rMC3", "rGV2", "rMR", "rSL", "rBC", "rDKJP", "rBC3",
               "rSGB"]
    
    return courses[course_id]

def controller(controller_id):
    """
    Translates controller_id to a plain controller name.
    """
    controllers = ["Wii Wheel", "Wii Remote + Nunchuk", "Classic Controller",
                   "GameCube Controller"]
    
    return controllers[controller_id]

def ghost_type(ghost_type_id):
    """
    Translates ghost_type_id to a plain ghost type name.
    """
    ghost_types = [0x00, "Personal Best", "World Record", "Continental Record",
                   "Rival Ghost", "Special Ghost", "Ghost Race", "Friend Ghost 1",
                   "Friend Ghost 2", "Friend Ghost 3", "Friend Ghost 4",
                   "Friend Ghost 5", "Friend Ghost 6", "Friend Ghost 7",
                   "Friend Ghost 8", "Friend Ghost 9", "Friend Ghost 10",
                   "Friend Ghost 11", "Friend Ghost 12", "Friend Ghost 13",
                   "Friend Ghost 14", "Friend Ghost 15", "Friend Ghost 16",
                   "Friend Ghost 17", "Friend Ghost 18", "Friend Ghost 19",
                   "Friend Ghost 20", "Friend Ghost 21", "Friend Ghost 22",
                   "Friend Ghost 23", "Friend Ghost 24", "Friend Ghost 25",
                   "Friend Ghost 26", "Friend Ghost 27", "Friend Ghost 28",
                   "Friend Ghost 29", "Friend Ghost 30", "Normal Staff Ghost",
                   "Expert Staff Ghost"]
    
    return ghost_types[ghost_type_id]

def drift_type(drift_type_id):
    """
    Translates drift_type_id to a plain drift type name.
    """
    drift_types = ["Manual", "Automatic"]

    return drift_types[drift_type_id]

def country(country_code):
    """
    Translates country_code to a plain country name.
    """
    countries = [0x00, "Japan", 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, "Anguilla",
                 "Antigua and Barbuda", "Argentina", "Aruba", "Bahamas", "Barbados",
                 "Belize", "Bolivia", "Brazil", "British Virgin Islands", "Canada",
                 "Cayman Islands", "Chile", "Colombia", "Costa Rica", "Dominica",
                 "Dominican Republic", "Ecuador", "El Salvador", "French Guiana",
                 "Grenada", "Guadeloupe", "Guatemala", "Guyana", "Haiti", "Honduras",
                 "Jamaica", "Martinique", "Mexico", "Montserrat",
                 "Netherlands Antilles", "Nicaragua", "Panama", "Paraguay", "Peru",
                 "St. Kitts and Nevis", "St. Lucia", "St. Vincent and the Grenadines",
                 "Suriname", "Trinidad and Tobago", "Turks and Caicos Islands",
                 "United States", "Uruguay", "US Virgin Islands", "Venezuela", 0x35,
                 0x36, 0x37, 0x38, 0x39, 0x3A, 0x3B, 0x3C, 0x3D, 0x3E, 0x3F, "Albania",
                 "Australia", "Austria", "Belgium", "Bosnia and Herzegovina",
                 "Botswana", "Bulgaria", "Croatia", "Cyprus", "Czech Republic",
                 "Denmark", "Estonia", "Finland", "France", "Germany", "Greece",
                 "Hungary", "Iceland", "Ireland",  "Italy", "Latvia", "Lesotho",
                 "Lichtenstein", "Lithuania", "Luxembourg", "F.Y.R. of Macedonia",
                 "Malta", "Montenegro", "Mozambique", "Namibia", "Netherlands",
                 "New Zealand", "Norway", "Poland", "Portugal", "Romania", "Russia",
                 "Serbia", "Slovakia", "Slovenia", "South Africa", "Spain", "Swaziland",
                 "Sweden", "Switzerland", "Turkey", "United Kingdom", "Zambia",
                 "Zimbabwe", "Azerbaijan", "Mauritania", "Mali", "Niger", "Chad",
                 "Sudan", "Eritrea", "Djibouti", "Somalia", 0x7A, 0x7B, 0x7C, 0x7D,
                 0x7E, 0x7F, "Taiwan", 0x81, 0x82, 0x83, 0x84, 0x85, 0x86, 0x87,
                 "South Korea", 0x89, 0x8A, 0x8B, 0x8C, 0x8D, 0x8E, 0x8F, "Hong Kong",
                 "Macao", 0x92, 0x93, 0x94, 0x95, 0x96, 0x97, "Indonesia", "Singapore",
                 "Thailand", "Phillipines", "Malaysia", 0x9B, 0x9C, 0x9F, "China", 0xA1,
                 0xA2, 0xA3, 0xA4, 0xA5, 0xA6, 0xA7, "U.A.E.", "India", "Egypt", "Oman",
                 "Qatar", "Kuwait", "Saudi Arabia", "Syria", "Bahrain", "Jordan", 0xB2,
                 0xB3, 0xB4, 0xB5, 0xB6, 0xB7, 0xB8, 0xB9, 0xBA, 0xBB, 0xBC, 0xBD, 0xBE,
                 0xBF, 0xC0, 0xC1, 0xC2, 0xC3, 0xC4, 0xC5, 0xC6, 0xC7, 0xC8, 0xC9, 0xCA,
                 0xCB, 0xCC, 0xCD, 0xCE, 0xCF, 0xD0, 0xD1, 0xD2, 0xD3, 0xD4, 0xD5, 0xD6,
                 0xD7, 0xD8, 0xD9, 0xDA, 0xDB, 0xDC, 0xDD, 0xDE, 0xDF, 0xE0, 0xE1, 0xE2,
                 0xE3, 0xE4, 0xE5, 0xE6, 0xE7, 0xE8, 0xE9, 0xEA, 0xEB, 0xEC, 0xED, 0xEE,
                 0xEF, 0xF0, 0xF1, 0xF2, 0xF3, 0xF4, 0xF5, 0xF6, 0xF7, 0xF8, 0xF9, 0xFA,
                 0xFB, 0xFC, 0xFD, 0xFE, 0xFF]
    
    return countries[country_code]

def subregion(state_code):
    """
    Translates state_code to a plain town/state/province name.
    There are over 1600 region IDs, so this isn't going to be made any time soon.
    """
    pass