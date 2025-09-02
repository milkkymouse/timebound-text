import random
from weapons import *
from armour import *

# ==============================
# Classes
# ==============================
class Character:
    """
    Base class for any "combatant" (player or enemy)
    This class handles combat values and logic
    A Character has:
        - a name (str)
        - hp (integer)
        - agility (integer)
        - minimum and maximum damage (integers)
        - critical hit chance (integer, optional, defaults to 0)
        - sickness (dot effect that stacks, integer, defaults to 0)
        - inflict minimum and maximum sickness (sickness that it can give, integer, optional, defaults to 0)
    """
    def __init__(self,
                 name: str,
                 hp: int,
                 agility: int,
                 min_damage: int,
                 max_damage: int,
                 crit_ch: int = 0,
                 sickness: int = 0,
                 inflict_min_sickness: int = 0,
                 inflict_max_sickness: int = 0
                 ) -> None:
        self.name = name
        self.hp = hp
        self.hp_max = hp
        self.agility = agility
        self.min_damage = min_damage
        self.max_damage = max_damage
        self.crit_ch = crit_ch
        self.sickness = sickness
        self.inflict_min_sickness = inflict_min_sickness
        self.inflict_max_sickness = inflict_max_sickness

    def roll_damage(self) -> int:
        # Returns a random damage value between min_damage and max_damage
        return random.randint(self.min_damage, self.max_damage)
    
    def roll_inflict_sickness(self) -> int:
        # Returns a random sickness value between inflict_min_sickness and inflict_max_sickness
        return random.randint(self.inflict_min_sickness, self.inflict_max_sickness)

    def evade(self) -> bool:
        # Roll 1-100
        # The character succeeds in evading if rolled value is under the value of its agility attribute
        roll_evade = random.randint(1, 100)
        return roll_evade <= self.agility
    
    def crit(self) -> bool:
        # Roll 1-100
        # The character deals a critical hit if rolled value is under the value of its crit_ch attribute
        roll_crit = random.randint(1, 100)
        return roll_crit <= self.crit_ch
    
    def deal_crit(self, 
                  damage: int
                  ) -> bool:
        # Doubles damage if crit is triggered
        if self.crit():
            print("CRITICAL HIT")
            return damage * 2
        return damage

    def attack(self, 
               target
               ) -> None:
        # Handles basic attack sequence

        if target.evade():      # check if target dodges the attack
            print(f"{self.name} missed the attack!")
            return
        
        damage = self.roll_damage()         # roll base damage
        damage = self.deal_crit(damage)     # apply crit modifier if crit triggers

        # If this character can inflict sickness
        # Add inflict sickness value to target's sickness attribute
        if self.inflict_max_sickness > 0:
            inflicted_sickness = self.roll_inflict_sickness()
            target.sickness += inflicted_sickness
            print(f"{self.name} has inflicted {inflicted_sickness} sickness onto {target.name}!") 
            target.apply_sickness()     # sickness damage is applied instantly
        else:
            # Otherwise, deal raw damage
            target.take_damage(damage)
            print(f"{self.name} inflicts {target.name} for {damage} damage!")

    def apply_sickness(self) -> None:
        # Applies sickness damage at the start of turn
        if self.sickness > 0:
            self.take_damage(self.sickness)
            print(f"{self.name} suffers {self.sickness} damage from sickness")

    def take_damage(self,
                    damage: int
                    ) -> None:
        # Reduce HP, never go below 0
        self.hp = max(0, self.hp - damage)
        if self.hp <= 0:
            print(f"{self.name} has been put to sleep")
        else:
            print(f"{self.name} has taken {damage} damage and has {self.hp} health remaining!")



class Enemy(Character):
    def __init__(self,
                 name: str,
                 group_size: int,
                 hp_member: int,
                 agility: int,
                 min_damage: int,
                 max_damage: int,
                 crit_ch: int = 0,
                 sickness: int = 0,
                 inflict_min_sickness: int = 0,
                 inflict_max_sickness: int = 0
                 ) -> None:
        """
        A subclass of Character
        An Enemy can represent a group of enemies
        """
        self.original_group_size = group_size       # store how many enemies the group started with
        self.current_group_size = group_size        # track how mny enemies are left
        self.hp_member = hp_member                  # HP of a single enemy
        self.sickness_member = sickness             # sickness per individual enemy
        total_hp = hp_member * group_size           
        total_sickness = sickness * group_size

        # Call parent class to initialise common attributes
        super().__init__(name = name, 
                         hp = total_hp,
                         agility = agility,
                         min_damage = min_damage,
                         max_damage = max_damage,
                         crit_ch = crit_ch,
                         sickness = total_sickness,
                         inflict_min_sickness = inflict_min_sickness,
                         inflict_max_sickness = inflict_max_sickness
                         )

    def update_group_size(self):
        # Recalculate group size after taking damage
        if self.hp <=0:
            self.current_group_size = 0
        else:
            # Divide remaining HP by hp per enemy to find out how many members are left in the group
            self.current_group_size = max(1, self.hp // self.hp_member)

    def roll_damage(self) -> int:
        # The attacks of each remaining member are summed together
        return sum(random.randint(self.min_damage, self.max_damage)
                   for _ in range(self.current_group_size) 
                   )
    
    def roll_inflict_sickness(self) -> int:
        # Each remaining member can inflict sickness
        return sum(random.randint(self.inflict_min_sickness, self.inflict_max_sickness)
                   for _ in range(self.current_group_size) 
                   )
    
    def attack(self,
               target
               ) -> None:
        # Overrides basic attack method to include group members
        damage = self.roll_damage()
        damage = self.deal_crit(damage)

        if target.evade():
            print(f"{self.name} missed the attack!")
            return
        
        if self.inflict_max_sickness > 0:
            inflicted_sickness = self.roll_inflict_sickness()
            target.sickness += inflicted_sickness
            print(f"{self.name} (Group of {self.current_group_size}) inflicts {inflicted_sickness} sickness onto {target.name}!") 
            target.apply_sickness()     
        else:
            print(f"{self.name} (Group of {self.current_group_size}) attacks {target.name} for {damage} damage!")
            target.take_damage(damage)
    
    def take_damage(self,
                    damage: int
                    ) -> None:
        self.hp = max(0, self.hp - damage)
        self.update_group_size()        # recalculate group size
        if self.hp <= 0:
            print(f"{self.name} has been put to sleep")
        else:
            print(f"{self.name} has taken {damage} damage and has {self.current_group_size} member(s) left with a total of {self.hp} health remaining!")


class Hero(Character):
    def __init__(self,
                 name: str, 
                 sickness: int = 0,
                 inflict_min_sickness: int = 0,
                 inflict_max_sickness: int = 0,
                 ):
        """
        A subclass of Character that handles the player
        Extends the Character class but uses weapons and armour for stats
        """
        self.weapon = fists     # default starting weapon
        self.armour = clothes   # default starting armour
        self.defend = False     # defensive stance toggle
        super().__init__(name = name,
                         hp = self.armour.hp,                       # HP comes from armour
                         agility = self.armour.agility,             # Agility comes from armour
                         min_damage = self.weapon.min_damage,       # Damage comes from weapon
                         max_damage = self.weapon.max_damage,
                         crit_ch = self.weapon.crit_ch,             # Crit Chance comes from weapon
                         sickness = sickness,
                         inflict_min_sickness = inflict_min_sickness,
                         inflict_max_sickness = inflict_max_sickness
                         )
    
    def special_attack(self,
                       target
                       ) -> None:
        # If weapon is a SpecialWeapon, player can choose attack type
        choice = input(f"Use Basic Attack [1] Special Attack [2] with {self.weapon.name}? ").strip()

        if choice == "1":
            # Basic attack
            if target.evade():
                print(f"{self.name} missed the attack!")
                return
            else:
                damage = self.weapon.roll_damage()
                damage = self.deal_crit(damage)
                print(f"{self.name} uses {self.weapon.name}'s BASIC ATTACK for {damage} damage!")
                target.take_damage(damage)

        elif choice == "2":
            # Special attack
            if target.evade():
                print(f"{self.name} missed the attack!")
                return
            else:
                damage = self.weapon.roll_special()
                damage = self.deal_crit(damage)
                print(f"{self.name} uses {self.weapon.name}'s SPECIAL ATTACK for {damage} damage!")
                target.take_damage(damage)

                if self.weapon.inflict_max_sickness > 0:
                    # Apply sickness if weapon has a value for that attribute
                    self.inflict_min_sickness = self.weapon.inflict_min_sickness
                    self.inflict_max_sickness = self.weapon.inflict_max_sickness
                    inflicted_sickness = self.roll_inflict_sickness()
                    target.sickness += inflicted_sickness
                    print(f"{self.name} uses {self.weapon.name}'s SPECIAL ATTACK and inflicts {inflicted_sickness} sickness onto {target.name}!") 
                    target.apply_sickness()

        else:
            # If invalid choice, fallback to main attack function
            print("Invalid choice. Please enter 1 to use the Basic Attack or 2 for the Special Attack")
            self.attack(target)

    def aoe_attack(self,
                   target
                   ) -> None:
        # If weapon is an AOEWeapon, damage is applied per enemy in the group
        if target.evade():
            print(f"{self.name} missed the attack!")
            return
        else:
            damage = self.weapon.roll_damage() * target.current_group_size
            damage = self.deal_crit(damage)
            print(f"{self.name} uses {self.weapon.name} for a total of {damage} damage to all enemies in range!")
            target.take_damage(damage)

    def attack(self, 
               target
               ) -> None:
        # Overrides basic attack method
        # Behaviour depends on weapon type
        if isinstance(self.weapon, SpecialWeapon):
            self.special_attack(target)     # Special weapons allow the user to choose from different attacks

        elif isinstance(self.weapon, AOEWeapon):
            self.aoe_attack(target)         # AOE weapons hits multiple enemies

        else:
            # Normal basic attack
            if target.evade():
                print(f"{self.name} missed the attack!")
                return
            else:
                damage = self.weapon.roll_damage()
                damage = self.deal_crit(damage)
                print(f"{self.name} uses {self.weapon.name} for {damage} damage!")
                target.take_damage(damage)

    def take_damage(self,
                    damage: int
                    ) -> None:
        # Overrides basic take_damage method
        # If user is currently defending, incoming damage is halved
        if self.defend:
            damage = damage / 2
            print(f"{self.name} defends the attack!")
        else: 
            damage = damage

        # Apply damage armour reduction, percentage based
        damage = int(damage * (1 - self.armour.damage_reduction))   

        self.hp = max(0, self.hp - damage)
        if self.hp <= 0:
            print(f"{self.name} has been put to sleep")
        else:
            print(f"{self.name} has taken {damage} damage and has {self.hp} health remaining!")


# ==============================
# Enemy definitions
# ==============================
mictlantecuhtli = Enemy(name = "Mictlantecuhtli",
                   group_size = 1,
                   hp_member = 50000,
                   agility = 10,
                   min_damage = 500,
                   max_damage = 700,
                   crit_ch = 25
                   )

trex = Enemy(name = "T-rex",
             group_size = 1,
             hp_member = 20000,
             agility = 5,
             min_damage = 300,
             max_damage = 300,
             crit_ch = 10
             )

tribe = Enemy(name = "Tribe",
              group_size = random.randint(10, 50),
              hp_member = 100,
              agility = 10,
              min_damage = 5,
              max_damage = 10,
              crit_ch = 10
              )

spack = Enemy(name = "Pack of Saber-toothed Tigers",
              group_size = random.randint(2, 7),
              hp_member = 200,
              agility = 20,
              min_damage = 50,
              max_damage = 100,
              crit_ch = 50
              )

mammoth = Enemy(name = "Wooly Mammoth",
                group_size = 1,
                hp_member = 20000,
                agility = 1,
                min_damage = 50,
                max_damage = 100
                )

titanoboa = Enemy(name = "Titanoboa",
                  group_size = 1,
                  hp_member = 3000,
                  agility = 25,
                  min_damage = 50,
                  max_damage = 100,
                  crit_ch = 20,
                  inflict_min_sickness = 20,
                  inflict_max_sickness = 50
                  )

chieftain = Enemy(name = "Chieftain",
                  group_size = 1,
                  hp_member = 3000,
                  agility = 1,
                  min_damage = 300,
                  max_damage = 700,
                  crit_ch = 20
                  )

crocodile = Enemy(name = "Crocodile",
                  group_size = 1,
                  hp_member = 1000,
                  agility = 0,
                  min_damage = 100,
                  max_damage = 200,
                  crit_ch = 20
                  )

cave_bear = Enemy(name = "Giant Cave Bear",
                  group_size = random.randint(1, 2),
                  hp_member = 1500,
                  agility = 5,
                  min_damage = 80,
                  max_damage = 150,
                  crit_ch = 20
                  )

megatherium = Enemy(name = "Giant Ground Sloth",
                    group_size = 1,
                    hp_member = 2000,
                    agility = 0,
                    min_damage = 20,
                    max_damage = 80
                    )

terror_bird = Enemy(name = "Terror Bird",
                    group_size = 1,
                    hp_member = 500,
                    agility = 80,
                    min_damage = 100,
                    max_damage = 200,
                    crit_ch = 25
                    )

smilodon = Enemy(name = "Saber-toothed tiger",
                 group_size = 1,
                 hp_member = 200,
                 agility = 20,
                 min_damage = 50,
                 max_damage = 100,
                 crit_ch = 50
                 )

snakes = Enemy(name = "Line of Snakes",
              group_size = random.randint(4, 7),
              hp_member = 5,
              agility = 50,
              min_damage = 2,
              max_damage = 5,
              crit_ch = 20,
              inflict_min_sickness = 5,
              inflict_max_sickness = 10
              )

megaloceros = Enemy(name = "Megaloceros",
                    group_size = 1,
                    hp_member = 300,
                    agility = 10,
                    min_damage = 5,
                    max_damage = 10
                    )

wolves = Enemy(name = "Pack of Wolves",
               group_size = random.randint(3, 5),
               hp_member = 20,
               agility = 10,
               min_damage = 5,
               max_damage = 15
               )

wolf = Enemy(name = "Wolf",
             group_size = 1,
             hp_member = 20,
             agility = 10,
             min_damage = 5,
             max_damage = 15
             )

# ==============================
# Player definition
# ==============================
player = Hero(name = "Player")
