# NOTE (xi): unfinished, currently only for the use of testing other scripts
#            that rely on this module

from Modules import mkw_classes as classes


def vehicle_id():
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
    return vehicles[classes.RaceDataPlayer.vehicle_id()]


def character_id():
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
    return characters[classes.RaceDataPlayer.character_id()]


def course_slot_abbreviation():
    courses = ["MC", "MMM", "MG", "GV", "TF", "CM", "DKS", "WGM", "LC",
               "DC", "MH", "MT", "BC", "RR", "DDR", "KC", "rPB", "rMC", "rWS", "rDKM",
               "rYF", "rDH", "rPG", "rDS", "rMC3", "rGV2", "rMR", "rSL", "rBC", "rDKJP",
               "rBC3", "rSGB"]
    return courses[classes.RaceDataSettings.course_id()]
