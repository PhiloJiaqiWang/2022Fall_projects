from dataclasses import dataclass
import pandas as pd
import numpy as np

@dataclass
class Equipment:

    def __init__(self, name):
        """
        Initiate function for the players.
        """
        ep = pd.read_csv('equipments_db.txt', sep=',')
        if name in ep['name'].values:
            self.damage_min = ep[ep.name == name]['damage_min'][0]
            self.damage_max = ep[ep.name == name]['damage_max'][0]
            self.base_crit_chance = ep[ep.name == name]['damage_min'][0]
            self.crit_chance = ep[ep.name == name]['damage_min'][0]
            self.crit_power = ep[ep.name == name]['damage_min'][0]
            self.defense = ep[ep.name == name]['defense'][0]
            self.immunity = ep[ep.name == name]['immunity'][0]
            self.luck = ep[ep.name == name]['luck'][0]
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

    def generate_att_from_equip(self):
        """

        :return:
        """

    def set_player_health_energy(self, health_energy_lis: list):
        """
        to set the health bar and energy bar, the default is 100 and 270, either bar hits zero, the round ends and
        calculate the value.

        :param health_energy_lis: [health, energy]
        """


player1 = Player()
print(player1.player_health_energy)
a = 'Infinity Dagger'
equ = Equipment(a)
print(equ.damage_min)
player1.set_player_equipments([a, '', '', ''])
player1.set_player_att()
print(player1.player_att)
# class Rock:
#
# class Monster:
#
# class Floor:
#
#
# def running_game():
#     return 0