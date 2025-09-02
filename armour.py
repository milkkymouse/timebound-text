# ==============================
# Classes
# ==============================
class Armour:
    def __init__(self,
                 name: str,
                 description: str,
                 hp: int,
                 agility: int,
                 damage_reduction: float,
                 ) -> None:
        """
        Base class for all armour in the game
        Armour have:
            - a name (string)
            - a description (string)
            - hp (integer)
            - agility (integer)
            - damage reduction (float)
        """
        self.name = name
        self.description = description
        self.hp = hp
        description = description
        self.agility = agility
        self.damage_reduction = damage_reduction


# ==============================
# Armour definitions
# ==============================
primal_armour = Armour(name = "Primal Scale",
                       description = "A suit from the deadliest creature to roam the earth",
                       hp = 3000,
                       agility = 15,
                       damage_reduction = 0.2
                       )

mammoth_armour = Armour(name = "Colossus Hide",
                        description = "A thick hide from the remains of a large beast",
                        hp = 2000,
                        agility = 3,
                        damage_reduction = 0.3
                        )

iron_armour = Armour(name = "Iron Armour",
                     description = "A heavy suit of medieval craftsmanship",
                     hp = 1000,
                     agility = 1,
                     damage_reduction = 0.5
                     )

chainmail_armour = Armour(name = "Chainmail Armour",
                          description = "A suit of chainmail effective against slashing attacks",
                          hp = 750,
                          agility = 50,
                          damage_reduction = 0.35
                          )

bird_armour = Armour(name = "Gryphon's Mantle",
                     description = "A super lightweight suit of armour",
                     hp = 750,
                     agility = 70,
                     damage_reduction = 0.2
                     )

alligator_armour = Armour(name = "Alligator Plate",
                          description = "Hard and tough skin from the remains of an alligator",
                          hp = 1000,
                          agility = 5,
                          damage_reduction = 0.5
                          )

bear_armour = Armour(name = "Odin's Pelt",
                     description = "A thick pelt from a ferocious bear",
                     hp = 1000,
                     agility = 5,
                     damage_reduction = 0.25
                     )

sloth_armour = Armour(name = "Giant's Furcoat",
                      description = "The fur of a giant terrestial mammal",
                      hp = 1000,
                      agility = 0,
                      damage_reduction = 0.1
                      )

saber_armour = Armour(name = "Predator's Embrace",
                      description = "A sleek armour made from the hide of a saber-toothed cat",
                      hp = 500,
                      agility = 20,
                      damage_reduction = 0.2
                      )

deer_armour = Armour(name = "Venison Hide",
                     description = "A simple coat made from the hide of a deer",
                     hp = 300,
                     agility = 10,
                     damage_reduction = 0.2
                     )

vine_armour = Armour(name = "Living Vines",
                     description = "A mysterious armour that seems to be alive",
                     hp = 200,
                     agility = 25,
                     damage_reduction = 0
                     )

fur = Armour(name = "Fur Coat",
             description = "A simple fur coat taken from a small wolf",
             hp = 100,
             agility = 50,
             damage_reduction = 0
             )

clothes = Armour(name = "Clothing",
                 description = "Basic clothing that provides minimal protection",
                 hp = 25,
                 agility = 20,
                 damage_reduction = 0
                 )