import random

# =================================
# Classes
# =================================
class Weapon:
    """
    Base class for all weapons in the game
    A Weapon has:
        - a name (string)
        - a description (string)
        - minimum and maximum damage (integers)
        - critical hit chance (integer, optional, defaults to 0)
    """
    def __init__(self, 
                 name: str, 
                 description:str,
                 min_damage: int,
                 max_damage: int,
                 crit_ch: int = 0,
                 ) -> None:
        self.name = name
        self.description = description
        self.min_damage = min_damage
        self.max_damage = max_damage
        self.crit_ch = crit_ch
    
    def roll_damage(self) -> int:
        # Returns a random number between min_damage and max_damage to simulate attack damage
        return random.randint(self.min_damage, self.max_damage)

class SpecialWeapon(Weapon):
    """
    A subclass of Weapon
    Adds another attack with different values
    Adds special effects like inflicting sickness (poison)
    """
    def __init__(self, 
                 name: str, 
                 description: str,
                 min_damage: int,
                 max_damage: int,
                 min_special: int,
                 max_special: int,
                 crit_ch: int = 0,
                 inflict_min_sickness: int = 0,
                 inflict_max_sickness: int = 0
                 ) -> None:
        self.min_special = min_special
        self.max_special = max_special
        self.inflict_min_sickness = inflict_min_sickness
        self.inflict_max_sickness = inflict_max_sickness

        # Call parent class to initialise common attributes
        super().__init__(name = name, 
                         description = description,
                         min_damage = min_damage,
                         max_damage = max_damage,
                         crit_ch = crit_ch
                         )
    
    def roll_special(self) -> int:
        # Returns a random number between min_special and max_special to simulate a unique attack
        return random.randint(self.min_special, self.max_special)
    
    def roll_inflict_sickness(self)-> int:
        # Returns a random number between inflict_min_sickness and inflict_max_sickness to simulate sickness inflicted on the enemy
        return random.randint(self.inflict_min_sickness, self.inflict_max_sickness)
    
class AOEWeapon(Weapon):
    """
    A subclass of Weapon that represents Area of Effect weapons
    Does not add any new attributes
    Used to differentiate between single target weapons and aoe weapons when attacking
    """
    def __init__(self, 
                 name: str, 
                 description: str,
                 min_damage: int = 0,
                 max_damage: int = 0,
                 crit_ch: int = 0
                 ) -> None:
        super().__init__(name = name, 
                         description = description,
                         min_damage = min_damage,
                         max_damage = max_damage,
                         crit_ch = crit_ch
                         )


# ==============================
# Weapons
# ==============================
HOG = SpecialWeapon(name = "Hand of God",
                    description = "A powerful weapon forged in the flames of Gods",
                    min_damage = 1000,
                    max_damage = 2000,
                    min_special = 10,
                    max_special = 20000
                    )

scythe = SpecialWeapon(name = "Death's Scythe",
                       description = "Forged from the souls of the damnedt",
                       min_damage = 700,
                       max_damage = 1000,
                       min_special = 200,
                       max_special = 500,
                       crit_ch = 50,
                       inflict_min_sickness = 400,
                       inflict_max_sickness = 700
                       )

fireworks = AOEWeapon(name = "Fireworks",
                      description = "Strange rockets from Ancient China, deals AOE",
                      min_damage = 20,
                      max_damage = 50,
                      crit_ch = 50
                      )

prehistoric_slayer = Weapon(name = "Prehistoric Slayer",
                            description = "Masterpiece of the prehistoric age",
                            min_damage = 500,
                            max_damage = 1000,
                            crit_ch = 20
                            )

snake_toothed = SpecialWeapon(name = "Snake Toothed Sword",
                              description = "A blade crafted from the fangs of a giant snake",
                              min_damage = 400,
                              max_damage = 700,
                              min_special = 200,
                              max_special = 400,
                              crit_ch = 20,
                              inflict_min_sickness = 50,
                              inflict_max_sickness = 100
                              )

mammoth_blade = Weapon(name = "Mammoth Blade",
                       description = "A massive blade made from the tusk of a mammoth",
                       min_damage = 500,
                       max_damage = 800,
                       )

chainsaw = Weapon(name = "Chainsaw",
                  description = "A tool from the modern era",
                  min_damage = 200,
                  max_damage = 300,
                  crit_ch = 80
                  )

trident = Weapon(name = "Poseidon's Trident",
                 description = "An interesting looking fork",
                 min_damage = 150,
                 max_damage = 250,
                 crit_ch = 50
                 )

LST = Weapon(name = "Light Saber",
             description = "A sword made from the canines of a saber tooth tiger",
             min_damage = 100,
             max_damage = 200,
             crit_ch = 50
             )

katana = Weapon(name = "Katana",
                description = "A blade wielded with honour",
                min_damage = 80,
                max_damage = 150,
                crit_ch = 50
                )
             
MCB = Weapon(name = "Mechanical Crossbow",
             description = "A crossbow crafted with advanced middle age technology",
             min_damage = 70,
             max_damage = 200,
             crit_ch = 30
             )

sword = Weapon(name = "Long Sword",
               description = "A standard weapon for the nobelest of knights",
               min_damage = 100,
               max_damage = 200,
               crit_ch = 10
               )

battle_hammer = Weapon(name = "Battle Hammer",
                       description = "A heavy weapon wielded by warriors",
                       min_damage = 50,
                       max_damage = 100
                       )

poisoned_dagger = SpecialWeapon(name = "Poisoned Dagger",
                                description = "A dagger coated with a deadly poison",
                                min_damage = 20,
                                max_damage = 40,
                                min_special = 10,
                                max_special = 25,
                                inflict_min_sickness = 5,
                                inflict_max_sickness = 20,
                                )

spear = Weapon(name = "Spear",
               description = "A long weapon with a sharp point",
               min_damage = 30,
               max_damage = 60,
               crit_ch = 20
               )

dagger = Weapon(name = "Dagger",
                description = "A small blade used for quick and stealthy attacks",
                min_damage = 20,
                max_damage = 40,
                crit_ch = 50
                )

brambles = AOEWeapon(name = "Brambles",
                    description = "A weapon made from the thorns of a prickly bush, deals AOE",
                    min_damage = 5,
                    max_damage = 15,
                    )

bone = Weapon(name = "Bone",
              description = "From the carcass of an unknown creature",
              min_damage = 10,
              max_damage = 24,
              )

fists = Weapon(name = "Fists",
               description = "Your fists, the most basic of weapons",
               min_damage = 2,
               max_damage = 5,
               )
