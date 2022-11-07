from dataclasses import dataclass
import pandas as pd
import numpy as np
import random

@dataclass
class Equipment:

    def __init__(self, name):
        """
        Initiate function for the players.
        """
        self.name = name
        ep = pd.read_csv('equipments_db.txt', sep=',')
        if name in ep['name'].values:
            self.damage_min = ep[ep.name == name]['damage_min'].values[0]
            self.damage_max = ep[ep.name == name]['damage_max'].values[0]
            self.base_crit_chance = ep[ep.name == name]['damage_min'].values[0]
            self.crit_chance = ep[ep.name == name]['damage_min'].values[0]
            self.crit_power = ep[ep.name == name]['damage_min'].values[0]
            self.defense = ep[ep.name == name]['defense'].values[0]
            self.immunity = ep[ep.name == name]['immunity'].values[0]
            self.luck = ep[ep.name == name]['luck'].values[0]
        else:
            self.damage_min = 0
            self.damage_max = 0
            self.base_crit_chance = 0
            self.crit_chance = 0
            self.crit_power = 0
            self.defense = 0
            self.immunity = 0
            self.luck = 0


class Player:
    """
    This is a Class for the Player, it should contain information including the items the player equips
    and the mining skill level. The health and energy bar should be monitored and easily changed.
    """
    player_skill_level = 0  # mining skill level
    player_equipments = []  # the list of equipments [weapon, footwear, ring_one, ring_two]
    player_att = []  # the list of attributes [damage, Crit_Chance, Crit_Power, Defense, Immunity, Luck]
    player_health_energy = [100, 270]  # [health bar, energy bar]

    def __init__(self):
        """
        Initiate function for the players.
        """

    def set_skill_level(self, skill_level: int):
        """
        to set the mining skill level. 10 levels in total, but only 5 level and 10 level will make a difference.
        5 level: Choose Miner(+1 ore per vein) or Geologist(Chance for gems to appear in pairs)
        10 level: If choosing Miner in level 5, here choose between Blacksmith(Copper, Iron, Gold, Iridium,
        & Radioactive worth 50% more) and Prospector(Chance to find coal doubled). If choosing Geologist before, choose
        Excavator(Chance to find geodes doubled) or Gemologist(Gems worth 30% more)

        :param skill_level: the mining skill level, 0-10
        """
        self.player_skill_level = skill_level

    def set_player_equipments(self, equipments: list):
        """
        to set the equipments the player is wearing.
        :param equipments: [weapon, footwear, ring_one, ring_two]
        """
        self.player_equipments = equipments

    def set_player_att(self):
        """
        to set the attributes of this player. according to the equipments, search for every equipment in the
        equipment_db and add total attributes

        """

    def generate_att_from_equip(self):
        """
        to set the attributes of this player. according to the equipments, search for every equipment in the
        equipment_db and add total attributes

        >>> player1 = Player()
        >>> player1.set_player_equipments(['Infinity Dagger', 'Crabshell Ring', '', ''])
        >>> player1.generate_att_from_equip()
        >>> player1.player_att
        [50, 70, 50, 50, 50, 8, 0, 0]
        """
        this_damage_min = 0
        this_damage_max = 0
        this_base_crit_chance = 0
        this_crit_chance = 0
        this_crit_power = 0
        this_defense = 0
        this_immunity = 0
        this_luck = 0
        if self.player_equipments:
            for i in range(0, len(self.player_equipments)):
                this_equip = Equipment(self.player_equipments[i])
                this_damage_min += this_equip.damage_min
                this_damage_max += this_equip.damage_max
                this_base_crit_chance += this_equip.base_crit_chance
                this_crit_chance += this_equip.crit_chance
                this_crit_power += this_equip.crit_power
                this_defense += this_equip.defense
                this_immunity += this_equip.immunity
                this_luck += this_equip.luck
            self.player_att = [this_damage_min, this_damage_max, this_base_crit_chance, this_crit_chance,
                               this_crit_power, this_defense, this_immunity, this_luck]

    def set_player_health_energy(self, health_energy_lis: list):
        """
        to set the health bar and energy bar, the default is 100 and 270, either bar hits zero, the round ends and
        calculate the value.

        :param health_energy_lis: [health, energy]
        """
        self.player_health_energy = health_energy_lis



player1 = Player()
print(player1.player_health_energy)
a = 'Sneakers'
equ = Equipment(a)
print(equ.damage_min)
player1.set_player_equipments([a, '', '', ''])
player1.set_player_att()
print(player1.player_att)
class Rock:
    """
    everytime the player crack rocks, it will generate different items, you can find the information here:
    https://stardewvalleywiki.com/The_Mines#Remixed_Rewards
    the basic logic is when we call this class in the main func, it should randomly generate an item, and the
    probability is different in different floors. Also, we need to know the value of the item so that we can calculate
    the total amount.
    """
    def __init__(self):

class Monster:
    """
    the monsters information is here https://stardewvalleywiki.com/Monsters. It may need to use inheritance.
    You can try to create a relatively complicated one first.
    """


class Floor:
    """
    every floor has [30,50] rocks and [5,10] monsters. So the initiation will create
    a list of rocks and  a list of monsters based on this level.
    """
    floor_containers = []  # the list of the rocks in this floor
    floor_monsters = []  # the list of the monsters

    def __init__(self, level):
        self.level = level
        self.generate_rock_list(level)

    @staticmethod
    def generate_rock_list(self):
        """
        generate all the rocks in this floor.
        """
        rocks_num = random.randint(30, 50)
        for i in range(0, rocks_num):
            rock = Rock(self.level)
            self.floor_containers.append(rock)

    def generate_monster_list(self):
        """
        generate all the monsters in this floor.
        """
        monsters_num = random.randint(5, 10)
        for i in range(0, monsters_num):
            monster = Monster(self.level)
            self.floor_monsters.append(monster)


class MainGame:
    """
    running the game
    """
    def __init__(self, level_start, level_end):

    def one_floor(self):