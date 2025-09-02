from weapons import *
from characters import *
from armour import *

# ===============================
# Classes
# ===============================
class Area:
    """
    Represents a single location within the game
    An Area has:
        - a name (string)
        - a description (string)
        - exits (dictionary mapping directions to other area names)
        - any items or enemies (optional)
    """
    def __init__(self,
                 name: str,
                 description: str,
                 item: object = None,
                 enemy: object = None
                 ) -> None:
        self.name = name
        self.description = description
        self.item = item
        self.enemy = enemy
        self.complete = False   # to track if the area has been completed
        self.exits = {}         # dictionary of possible exits
    
    def add_exit(self,
                 action,
                 area_name
                 ) -> None:
        """
        Adds a possible action from an Area to another Area
        direction = the action to take (e.g., "north", "south", "hunt", "forage", etc.)
        area_name = string name of the area to which the action leads to
        """
        self.exits[action] = area_name      


class Region:
    """
    Groups together multiple Areas with a similar theme or location
    Allows for better organisation of the game world
    """
    def __init__(self,
                 name: str
                 ) -> None:
        self.name = name
        self.areas = {}     # dictionary to hold areas by name

    def add_area(self, 
                 area: Area):
        """
        Adds an Area object to this Region's dictionary of areas
        """
        self.areas[area.name] = area    



# ==============================
# Global Area Registry
# ==============================

# This dictionary holds all areas across all regions
# Allows movement between regions
all_areas = {}


def register_region(region):
    """
    Registers a region and its areas into the global area registry.
    This allows the movement system to access all areas even across different regions
    """
    for area in region.areas.values():  # loop through each area in the region
        all_areas[area.name] = area     # add the area to the global registry by name


# ==============================
# Region and Area definitions
# ==============================
#--------------- Savanna ---------------#
savanna = Region(name = "Savanna")


# define areas
short_grasslands = Area(name = "Short Grasslands",
                        description = "You are in a vast expanse of open grasslands. It is eerily quiet",
                        )

tall_grasslands = Area(name = "Tall Grasslands",
                       description = "Your view is obstructed by tall grass, making it hard to see far. A faint rustling can be heard",
                       item = bone
                       )

dense_grasslands = Area(name = "Dense Grasslands",
                        description = "The grass is so thick here that you can barely move. You feel uneasy",
                        item = fur,
                        enemy = wolf
                        )

thornbush = Area(name = "Thornbush Thicket",
                 description = "You push through a maze of dry, tangled thornbushes. The air smells of dust and something metallic",
                 item = brambles,
                 enemy = snakes
                 )

den = Area(name = "Wolf's Den",
           description = "You have stumbled onto the gravesite of many skeletons",
           item = spear,
           enemy = wolves
           )

plains = Area(name = "Open Plains",
              description = "The ground rumbles as dirt is swept up into the air",
              item = deer_armour,
              enemy = megaloceros
              )

tree = Area(name = "Savanna Tree",
            description = "You go rest under a tree. You sit down but stumble as something cumbles under you. Human remains",
            item = LST
            )

northern_grasslands = Area(name = "Northern Grasslands",
                           description = "The ground is littered with carcasses rotting under the sun's heat",
                           item = saber_armour,
                           enemy = smilodon
                           )

southern_grasslands = Area(name = "Southern Grasslands",
                           description = "Large acacia trees provide shade. Large bohemoths take them for food",
                           item = sloth_armour,
                           enemy = megatherium
                           )

watering_hole = Area(name = "Watering Hole",
                     description = "A muddy watering hole surrounded by tall grass. The water is murky, but it is the only source of water for miles",
                     item = alligator_armour,
                     enemy = crocodile
                     )



# add exits
short_grasslands.add_exit("north", "Woodland Edge")
short_grasslands.add_exit("south", "Tall Grasslands")

tall_grasslands.add_exit("north", "Short Grasslands")
tall_grasslands.add_exit("hunt", "Dense Grasslands")
tall_grasslands.add_exit("forage", "Foraging Ground")

dense_grasslands.add_exit("north", "Tall Grasslands")
dense_grasslands.add_exit("east", "Thornbush Thicket")
dense_grasslands.add_exit("west", "Wolf's Den")
dense_grasslands.add_exit("south", "Open Plains")

thornbush.add_exit("west", "Dense Grasslands")
thornbush.add_exit("straight", "Open Plains")

den.add_exit("east", "Dense Grasslands")
den.add_exit("straight", "Open Plains")

plains.add_exit("back", "Dense Grasslands")
plains.add_exit("north", "Northern Grasslands")
plains.add_exit("south", "Southern Grasslands")
plains.add_exit("rest", "Savanna Tree")

northern_grasslands.add_exit("back", "Open Plains")
northern_grasslands.add_exit("rest", "Savanna Tree")

southern_grasslands.add_exit("back", "Open Plains")
southern_grasslands.add_exit("rest", "Savanna Tree")

tree.add_exit("explore", "Watering Hole")
tree.add_exit("hunt", "Outer Region")
tree.add_exit("forage", "Foraging Ground")

# add areas to the region
savanna.add_area(short_grasslands)  
savanna.add_area(tall_grasslands)  
savanna.add_area(dense_grasslands)
savanna.add_area(thornbush)
savanna.add_area(den)
savanna.add_area(plains)
savanna.add_area(tree)
savanna.add_area(northern_grasslands)
savanna.add_area(southern_grasslands)
savanna.add_area(watering_hole)

# adds the region's areas into the global dictionary
register_region(savanna)

#--------------- Jungle ---------------#
jungle = Region(name = "Jungle")

# define areas
edge = Area(name = "Woodland Edge",
            description = "Large jungle trees are looming ahead of you",
            item = vine_armour
            )

dense_forest = Area(name = "Dense Forest",
                    description = "The dense foliage only lets individual rays of light to penetrate",
                    item = dagger
                    )

clearing = Area(name = "Open Clearing",
                description = "The jungle opens up to a large empty space",
                item = deer_armour,
                enemy = megaloceros
                )

river = Area(name = "River",
             description = "A small river flows. A log is placed up on two rocks, maybe as a bridge?"
             )

# add exits
edge.add_exit("south", "Short Grasslands")
edge.add_exit("forage", "Foraging Ground")
edge.add_exit("deeper", "Dense Forest")

dense_forest.add_exit("back", "Woodland Edge")
dense_forest.add_exit("deeper", "Open Clearing")

clearing.add_exit("back", "Dense Forest")
clearing.add_exit("deeper", "River")

river.add_exit("back", "Open Clearing")
river.add_exit("bridge", "Secret Gate")
river.add_exit("follow river", "Village Outskirts")

# add areas to the region
jungle.add_area(edge)
jungle.add_area(dense_forest) 
jungle.add_area(clearing)
jungle.add_area(river)

# adds the region's areas into the global dictionary
register_region(jungle)

#--------------- Ruins ---------------#
ruins = Region(name = "Ruins")

# define areas
secret = Area(name = "Secret Gate",
              description = "A door covered in vines... and maybe some other green critters",
              item = poisoned_dagger,
              enemy = snakes
              )

grounds = Area(name = "Open Grounds",
               description = "An open sanctuary within the walls of the ruins"
               )

watch_tower = Area(name = "Watch Tower Remains",
                   description = "The crumbled debris of what seems to be a watchtower",
                   item = MCB
                   )

statues = Area(name = "Courtyard of Statues",
               description = "Eerie humanoid statues. Some are even decorated!.. with some limbs missing",
               item = chainmail_armour
               )

stairwell = Area(name = "Dusty Stairwell",
                 description = "A small hole in the ground reveals itself to be a way to go deeper"
                 )

hall = Area(name = "Hall of Echoes",
            description = "SOunD iS heAEaVily dISTorted. don't get caught off guard"
            )

passage = Area(name = "Passage",
               description = "The passage is littered with bones. It's not too late to turn back",
               item = LST,
               enemy = smilodon
               )

chambers = Area(name = "Flooded Chambers",
                description = "Stagnant water fills the room, softly rippling beneath the surface",
                item = alligator_armour,
                enemy = crocodile
                )

crypt = Area(name = "Collapsed Crypt",
             description = "Stone slabs lie broken. The air is stale, heavy with a musk of territorial aggression.",
             item = bear_armour,
             enemy = cave_bear
             )

murals = Area(name = "Hall of Murals",
              description = "The doorway crumples behind you. Walls are lined with tales of ancient beasts, roaring lizards, colied serpents, tusked giants.",
              item = mammoth_armour
              )

garden = Area(name = "Pillar Garden",
              description = "Dozens of pillars rise from the floor. Something darts between them, too fast to notice...",
              item = bird_armour,
              enemy = terror_bird
              )

archway = Area(name = "Obsidian Archway",
               description = "A black arch stands alone. Deep grooves mark the floor, as if something dragged itself along, again and again",
               item = snake_toothed,
               enemy= titanoboa
               )

god = Area(name = "Statue of the Gods",
           description = "A towering figure looms, arms stretched forward as if asking for an offering",
           item = HOG,
           enemy = mammoth
           )

sunken_arena = Area(name = "Sunken Arena",
                    description = "An pit opens wide, walls marked with claws. The ground shakes. Something ancient stirs below",
                    item = primal_armour,
                    enemy = trex
                    )


# add exits
secret.add_exit("back", "River")
secret.add_exit("enter", "Open Grounds")

grounds.add_exit("back", "Secret Gate")
grounds.add_exit("left", "Watch Tower Remains")
grounds.add_exit("straight", "Courtyard of Statues")
grounds.add_exit("right", "Dusty Stairwell")

watch_tower.add_exit("right", "Open Grounds")
watch_tower.add_exit("straight", "Courtyard of Statues")

statues.add_exit("back", "Open Grounds")
statues.add_exit("left", "Watch Tower Remains")
statues.add_exit("right", "Dusty Stairwell")

stairwell.add_exit("back", "Open Grounds")
stairwell.add_exit("enter", "Hall of Echoes")

hall.add_exit("back", "Dusty Stairwell")
hall.add_exit("deeper", "Passage")

passage.add_exit("back", "Hall of Echoes")
passage.add_exit("left", "Flooded Chambers")
passage.add_exit("right", "Collapsed Crypt")

chambers.add_exit("back", "Passage")
chambers.add_exit("deeper", "Hall of Murals")

crypt.add_exit("back", "Passage")
crypt.add_exit("deeper", "Hall of Murals")

murals.add_exit("left", "Pillar Garden")
murals.add_exit("right", "Obsidian Archway")

garden.add_exit("back", "Hall of Murals")
garden.add_exit("deeper", "Statue of the Gods")

archway.add_exit("back", "Hall of Murals")
archway.add_exit("deeper", "Statue of the Gods")

god.add_exit("deeper", "Sunken Arena")

sunken_arena.add_exit("deeper", "$#*!!-^")

# add areas to the region
ruins.add_area(secret)
ruins.add_area(grounds)
ruins.add_area(watch_tower)
ruins.add_area(statues)
ruins.add_area(stairwell)
ruins.add_area(hall)
ruins.add_area(passage)
ruins.add_area(chambers)
ruins.add_area(crypt)
ruins.add_area(murals)
ruins.add_area(garden)
ruins.add_area(archway)
ruins.add_area(god)
ruins.add_area(sunken_arena)

# adds the region's areas into the global dictionary
register_region(ruins)

#--------------- Settlement ---------------#
settlement = Region(name = "Settlement")

# define areas
foraging_ground = Area(name = "Foraging Ground",
                       description = "While foraging for food, you run into a group of cavemen. They seem friendly",
                       item = spear
                       )

outskirts = Area(name = "Village Outskirts",
                 description = "A vast settlement, with structures more advanced than any caveman could create, fades into view",
                 )

gate = Area(name = "Village Gate",
            description = "Guards fitted in attire unbefitting the time period greets you."
            )

guards = Area(name = "Guards",
              description = "You learn that many face your same fate, brought back to the stone age from their own time periods"
              )

city_centre = Area(name = "City Centre",
                   description = "You are in the middle of the settlement. Many paths and buildings await you",
                   item = chainmail_armour
                   )

town_hall = Area(name = "Town Hall",
                 description = "The town hall's marble walls amaze you, a feat of Ancient Greek architecture"
                 )

gallery = Area(name = "Gallery",
               description = "You see records of familiar names - Greek Gods",
               item = trident
               )

tavern = Area(name = "Tavern",
              description = "The tavern is empty. People are gathering food for the settlement. Maybe you can look around while noone's watching"
              )

kitchen = Area(name = "Kitchen",
               description = "The kitchen is up to medieval standards",
               item = poisoned_dagger,
               enemy = snakes
               )

barracks = Area(name = "Barracks",
                description = "Where people train or learn the different techniques or weapons from different cultures"
                )

north_train = Area(name = "Northern Training Grounds",
                   description = "Specialised in Nordic combat",
                   item = battle_hammer
                   )

south_train = Area(name = "Southern Training Grounds",
                   description = "Specialised in Ranged combat",
                   item = MCB
                   )

east_train = Area(name = "Eastern Training Grounds",
                  description = "Specialised in Asian combat",
                  item = katana
                  )

west_train = Area(name = "Western Training Grounds",
                  description = "Specialised in Medieval combat",
                  item = sword
                  )

storage = Area(name = "Storage Room",
               description = "An empty room filled with random junk",
               item = fireworks
               )


# add exits
foraging_ground.add_exit("follow tribe", "Village Outskirts")

outskirts.add_exit("ahead", "Village Gate")

gate.add_exit("enter", "City Centre")

city_centre.add_exit("town hall", "Town Hall")
city_centre.add_exit("tavern", "Tavern")
city_centre.add_exit("barracks", "Barracks")
city_centre.add_exit("storage", "Storage Room")
city_centre.add_exit("hunt", "Outer Region")

town_hall.add_exit("back", "City Centre")
town_hall.add_exit("gallery", "Gallery")

tavern.add_exit("back", "City Centre")
tavern.add_exit("kitchen", "Kitchen")

barracks.add_exit("back", "City Centre")
barracks.add_exit("north", "Northern Training Grounds")
barracks.add_exit("south", "Southern Training Grounds")
barracks.add_exit("east", "Eastern Training Grounds")
barracks.add_exit("west", "Western Training Grounds")

storage.add_exit("back", "City Centre")

kitchen.add_exit("back", "Tavern")

north_train.add_exit("back", "Barracks")
south_train.add_exit("back", "Barracks")
east_train.add_exit("back", "Barracks")
west_train.add_exit("back", "Barracks")

gallery.add_exit("back", "Town Hall")


# add areas to the region
settlement.add_area(foraging_ground)
settlement.add_area(outskirts)
settlement.add_area(gate)
settlement.add_area(guards)
settlement.add_area(city_centre)
settlement.add_area(town_hall)
settlement.add_area(gallery)
settlement.add_area(tavern)
settlement.add_area(kitchen)
settlement.add_area(barracks)
settlement.add_area(north_train)
settlement.add_area(south_train)
settlement.add_area(east_train)
settlement.add_area(west_train)
settlement.add_area(storage)

# adds the region's areas into the global dictionary
register_region(settlement)

#--------------- Hunting Grounds ---------------#
hunting_grounds = Region(name = "Hunting Grounds")

# define areas
outer_grounds = Area(name = "Outer Region",
                      description = "The outskirts of the native's traditional hunting grounds",
                      item = bird_armour,
                      enemy = terror_bird
                      )

main_grounds = Area(name = "Main Hunting Grounds",
                    description = "Traditional hunting grounds of the natives. Rich with food and predators"
                    )

southern_grounds = Area(name = "Southern Hunting Grounds",
                        description = "Massive stand alone trees are littered across the region",
                        item = sloth_armour,
                        enemy = megatherium
                        )

northern_grounds = Area(name = "Northern Hunting Grounds",
                        description = "The weather sends chills down your spine. Snow falls as the earth quakes beneath your feet",
                        item = mammoth_armour,
                        enemy = mammoth
                        )

# add exits
outer_grounds.add_exit("ahead", "Main Hunting Grounds")

main_grounds.add_exit("back", "Outer Region")
main_grounds.add_exit("north", "Northern Hunting Grounds")
main_grounds.add_exit("south", "Southern Hunting Grounds")
main_grounds.add_exit("explore", "Rival Hunting Grounds")

northern_grounds.add_exit("south", "Main Hunting Grounds")
northern_grounds.add_exit("east", "Rival Hunting Grounds")

southern_grounds.add_exit("north", "Main Hunting Grounds")
southern_grounds.add_exit("east", "Rival Hunting Grounds")

# add areas to the region
hunting_grounds.add_area(outer_grounds)
hunting_grounds.add_area(main_grounds)
hunting_grounds.add_area(southern_grounds)
hunting_grounds.add_area(northern_grounds)

# adds the region's areas into the global dictionary
register_region(hunting_grounds)

#--------------- Rival ---------------#
rival = Region(name = "Rival Tribe")

# define areas
rival_hunting_ground = Area(name = "Rival Hunting Grounds",
                            description = "You stumble into a different area. People in prehistoric attire surround you",
                            item = scythe,
                            enemy = tribe
                            )

rival_settlement = Area(name = "Rival Settlement",
                        description = "You stumble into a village fit for the time period. Clay huts and campfires surround you",
                        item = mammoth_blade
                        )

hut = Area(name = "Prehistoric Hut",
           description = "A clay structure. There is noone home",
           item = bear_armour
           )

tent = Area(name = "Chieftain's Tent",
            description = "Somebody's home...",
            item = prehistoric_slayer,
            enemy = chieftain
            )

# add exits
rival_hunting_ground.add_exit("back", "Main Hunting Grounds")
rival_hunting_ground.add_exit("raid", "Rival Settlement")


rival_settlement.add_exit("hut", "Prehistoric Hut")
rival_settlement.add_exit("tent", "Chieftain's Tent")
rival_settlement.add_exit("leave", "Rough Dirt Path")

hut.add_exit("back", "Rival Settlement")

tent.add_exit("back", "Rival Settlement")

# add areas to the region
rival.add_area(rival_hunting_ground)
rival.add_area(rival_settlement)
rival.add_area(hut)
rival.add_area(tent)

# adds the region's areas into the global dictionary
register_region(rival)

#--------------- Temple ---------------#
temple = Region(name = "Temple")

# define areas
path = Area(name = "Rough Dirt Path",
            description = "You follow a rough path, plants start to surround you, their shadows blocking out the sun. It's not too late to turn back",
            )

entrance = Area(name = "Temple Entrance",
                description = "You hit a sudden wall. A structure, covered in vines and dirt seems to snarl back at you",
                enemy = spack
                )

room = Area(name = "Mysterious Room",
              description = "It stinks... Your foot hits something on the ground. The floor is littered with remains"
              )

remains = Area(name = "Remains",
               description = "A mangled remain. You cannot tell apart ribs from teeth...",
               item = chainsaw
               )

hallway = Area(name = "Spacious Hallways",
               description = "You follow the wall until you find to openings. The left is shrouded in darkness. The right exudes a suspicious light"
               )

twilight = Area(name = "Twilight Room",
                description = "The roof is torn open, rubble covers the ground... A pedestal is illuminated by the moon's gaze",
                item = snake_toothed,
                enemy = titanoboa
                )

pedestal = Area(name = "Pedestal",
                description = "It glows under the moonlight",
                item = HOG
                )

darkness = Area(name = "...",
                description = "there is nothing here",
                )

arena = Area(name = "$#*!!-^",
             description = "g<!dd |u<k",
             enemy = mictlantecuhtli
             )

# add exits
path.add_exit("deeper", "Temple Entrance")

entrance.add_exit("deeper", "Mysterious Room")

room.add_exit("inspect", "Remains")
room.add_exit("deeper", "Spacious Hallways")

remains.add_exit("deeper", "Spacious Hallways")

hallway.add_exit("back", "Mysterious Room")
hallway.add_exit("left", "...")
hallway.add_exit("right", "Twilight Room")

twilight.add_exit("back", "Spacious Hallways")
twilight.add_exit("inspect", "Pedestal")

pedestal.add_exit("back", "Spacious Hallways")

darkness.add_exit("back", "$#*!!-^")
darkness.add_exit("deeper", "$#*!!-^")

# add areas to the region
temple.add_area(path)
temple.add_area(entrance)
temple.add_area(room)
temple.add_area(remains)
temple.add_area(hallway)
temple.add_area(twilight)
temple.add_area(pedestal)
temple.add_area(darkness)
temple.add_area(arena)

# adds the region's areas into the global dictionary
register_region(temple)