from dataclasses import dataclass
import pandas as pd
import numpy as np
import random

############
# Player #
############
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

    def print_player_info(self):
        print("******PLAYER******")
        print("player_skill_level:", self.player_skill_level)
        print("player_equipments:", self.player_equipments)
        att_lis = ["damage", "Crit_Chance", "Crit_Power", "Defense", "Immunity", "Luck"]
        for i in range(0, len(att_lis)):
            print(att_lis[i], ":", self.player_att[i])
        print("player_health_energy:", self.player_health_energy)
        print("******PLAYER******")


############
# Rock #
############
class Rock():
    """
    everytime the player crack rocks, it will generate different items, you can find the information here:
    https://stardewvalleywiki.com/The_Mines#Remixed_Rewards
    the basic logic is when we call this class in the main func, it should randomly generate an item, and the
    probability is different in different floors. Also, we need to know the value of the item so that we can calculate
    the total amount.
    """

    # read the rock spreadsheet
    def __init__(self):
        self.r = pd.read_csv('rock.csv')
        self.r.set_index("item", inplace=True)

    # find rock sell price
    def rockValue(self, name):
        value = self.r.loc[name]['price']
        return value

    # generate the number of rock randomly by normal distribution
    def rockNum(self, name):
        min_num = self.r.loc[name]['min_num']
        max_num = self.r.loc[name]['max_num']
        number = round(random.uniform(min_num, max_num), 0)
        return number


############
# Monsters #
############
class Monster(object):
    """
    the monsters information is here https://stardewvalleywiki.com/Monsters. It may need to use inheritance.
    You can try to create a relatively complicated one first.
    """
    killable, HP, damage, defense, speed, XP, drop_rate = True, 0, 0, 0, 0, 0, {}

    def __init__(self, level):
        """
        Create a monster with its name.
        """
        self.level = level
        self.if_bottom()

    def if_bottom(self):
        result = self.level == 120
        if result:
            self.drop_rate = {"Diamond": 0.0005, "Prismatic Shard": 0.0005}
        return result

    def print_monster_info(self):
        print("killable:" + str(self.killable))
        print("HP:" + str(self.HP))
        print("damage:" + str(self.damage))
        print("defense:" + str(self.defense))
        print("speed:" + str(self.speed))
        print("XP:" + str(self.XP))
        print("drop_rate:" + str(self.drop_rate))


class Slime(Monster):
    """
    A Slime is one of the monster categories. It has several specifications including GreenSlime, FrostJelly, and
    RedSludge. A Slime itself is not a kind of monster that will show up in the Mines.
    """
    speed = 2


class GreenSlime(Slime):
    """A GreenSlime is a kind of Slime that could be found on any level in the Mines."""
    HP, damage, defense, XP = 24, 5, 1, 3

    def drop(self):
        self.drop_rate.update({"Amethyst": 0.015, "Dwarf Scroll I": 0.005, "Dwarf Scroll II": 0.001, "Green Algae": 0.1,
                               "Sap": 0.15, "Slime": 0.8})  # TODO: sum != 1; Slime Hutch?


class FrostJelly(Slime):
    """A FrostJelly is a kind of Slime that could only be found on level 41-79 in the Mines."""
    # TODO: can sometimes be found on other floors? sr. https://stardewvalleywiki.com/Slimes
    HP, damage, defense, XP = 106, 7, 0, 6  # TODO: the attack might grow

    def drop(self):
        self.drop_rate.update({"Dwarf Scroll II": 0.005, "Dwarf Scroll III": 0.015, "Dwarf Scroll IV": 0.001,
                               "Jade": 0.02, "Sap": 0.5, "Slime": 0.75, "Winter Root": 0.08})
        # TODO: sum != 1; Slime Hutch?


class RedSludge(Slime):
    """A GreenSlime is a kind of Slime that could be found on any level in the Mines."""
    HP, damage, defense, XP = 205, 16, 0, 10

    def drop(self):
        self.drop_rate.update({"Coal": 0.01, "Dwarf Scroll III": 0.005, "Dwarf Scroll II": 0.001, "Green Algae": 0.1,
                               "Sap": 0.5, "Slime": 0.8, "White Algae": 0.1})  # TODO: sum != 1; Slime Hutch? 1-3 Coal
        self.drop_rate["Diamond"] = 0.01


class Bug(Monster):
    """
    A Bug is a kind of monster that fly up and down or left and right in a fixed path. They will ignore the Player
    and will only follow the same path until slain. They only appear on floor 1-39.
    """
    HP, damage, defense, speed, XP = 1, 8, 0, 2, 1

    def drop(self):
        self.drop_rate.update({"Ancient Seed": 0.005, "Bug Meat": 0.76, "Dwarf Scroll I": 0.005,
                               "Dwarf Scroll IV": 0.001, "White Algae": 0.02})
        # TODO: sum != 1


class Bat(Monster):
    """
    A Bat is one of the monster categories. It has several variations including FrostBat and LavaBat. Bat itself is
    also a monster that will appear. It only appears on floor 31-39.
    """
    HP, damage, defense, speed, XP = 24, 6, 1, 3, 3

    def drop(self):
        self.drop_rate.update({"Bat Wings": 0.94, "Bomb": 0.02, "Dwarf Scroll I": 0.005,
                               "Dwarf Scroll IV": 0.001, "Rare Disc": 0.01})
        # TODO: sum != 1, 1-2 Bat Wings


class FrostBat(Bat):
    """A FrostBat is a variation of Bat and could only be found on level 41-79 in the Mines."""
    HP, damage, XP = 36, 7, 7

    def drop(self):
        self.drop_rate.update({"Bat Wings": 0.95, "Bomb": 0.02, "Dwarf Scroll II": 0.005,
                               "Dwarf Scroll IV": 0.001, "Rare Disc": 0.01})
        # TODO: sum != 1, 1-2 Bat Wings


class LavaBat(Bat):
    """A LavaBat is a variation of Bat and could only be found on level 81-119 in the Mines."""
    HP, damage, XP = 80, 15, 15

    def drop(self):
        self.drop_rate.update({"Bat Wings": 0.97, "Bomb": 0.02, "Dwarf Scroll III": 0.005,
                               "Dwarf Scroll IV": 0.001, "Rare Disc": 0.01})
        # TODO: sum != 1, 1-2 Bat Wings


class Crab(Monster):
    """
    A Crab is one of the monster categories. It has several variations including RockCrab and LavaCrab. A Crab itself
    is not a kind of monster that will show up in the Mines.
    """
    pass


class RockCrab(Crab):
    """A RockCrab is a variation of Crab and could only be found on level 1-29 in the Mines."""
    HP, damage, defense, speed, XP = 30, 5, 1, 2, 4

    def drop(self):
        self.drop_rate.update({"Cherry Bomb": 0.4, "Crab": 0.15, "Dwarf Scroll I": 0.005, "Dwarf Scroll IV": 0.001})
        # TODO: sum != 1


class LavaCrab(Crab):
    """A LavaCrab is a variation of Crab and could only be found on level 80-119 in the Mines."""
    HP, damage, defense, speed, XP = 120, 15, 3, 3, 12

    def drop(self):
        self.drop_rate.update({"Bomb": 0.4, "Crab": 0.25, "Dwarf Scroll III": 0.005, "Dwarf Scroll IV": 0.001})
        # TODO: sum != 1


class Floor:
    """
    every floor has [30,50] rocks and [5,10] monsters. So the initiation will create
    a list of rocks and  a list of monsters based on this level.
    """
    floor_containers = []  # the list of the rocks in this floor
    floor_monsters = []  # the list of the monsters
    total_value = 0  # total value of all the rocks in this floor

    def __init__(self, level):
        self.r = pd.read_csv('rock.csv')
        self.r.set_index("item", inplace=True)
        self.level = level
        self.generate_rock_list()

    def randomItem(self, level):
        if level <= 39:
            columnName = '0-39'
        elif 40 <= level <= 79:
            columnName = '40-79'
        elif 80 <= level:
            columnName = '80+'
        possibility_list = self.r[columnName].values.tolist()
        item_list = self.r.index.tolist()
        output = random.choices(item_list, weights=possibility_list, k=1)
        return output

    # @staticmethod
    # generate the list of rock and the total value in this floor
    def generate_rock_list(self):
        """
        generate all the rocks in this floor.
        """
        rocks_num = random.randint(30, 50)
        for i in range(0, rocks_num):
            rock = self.randomItem(self.level)[0]
            self.floor_containers.append(rock)
            self.total_value += Rock().rockValue(rock) * Rock().rockNum(rock)
        return self.floor_containers, self.total_value

    def generate_monster_list(self):
        """Generate all the monsters in this floor. Probs for defined monsters could be changed to be passed in."""
        monsters = {
            1: [GreenSlime, Bug, RockCrab],
            2: [GreenSlime, Bat, Bug],
            3: [GreenSlime, FrostBat, FrostJelly],
            4: [GreenSlime, LavaBat, LavaCrab, RedSludge]
        }
        monsters_num = random.randint(5, 10)

        def section_finder(level):
            """Find the section number for the level."""
            if level < 30:
                return 1
            elif level < 40:
                return 2
            elif level < 80:
                return 3
            return 4

        for i in range(0, monsters_num):
            section_i = section_finder(self.level)
            monster = random.choice(monsters[section_i])  # TODO: logic test unperformed
            self.floor_monsters.append(monster)
        return self.floor_monsters


aa, bb = Floor(44).generate_rock_list()
mon = Floor(33).generate_monster_list()
print(mon[1].HP)
print('floor container', aa)
print('total value in this floor', bb)


class MainGame:
    """
    running the game
    """

    def __init__(self, level_start, level_end):
        pass

    def one_floor(self, level, player: Player):
        container, total_value = Floor(level).generate_rock_list()
        monsters = Floor(level).generate_monster_list()
        for monster in monsters:
            print(monster)
            monster.print_monster_info(monster)

    def one_round_attack(self, monster:Monster, player: Player):
        """
        total_damage_player = damage - defense_monster + if_crit*(3 + Crit_Power/50)
        total_damage_monster = damage - defense_player
        todo: immunity and debuff?

        :param monster:
        :param player:
        :return:
        """



player1 = Player()
print(player1.player_health_energy)
a = 'Sneakers'
equ = Equipment(a)
print(equ.damage_min)
player1.set_player_equipments([a, '', '', ''])
player1.generate_att_from_equip()
print(player1.player_att)
one = MainGame(0, 12)
player1.print_player_info()
one.one_floor(2, player1)
