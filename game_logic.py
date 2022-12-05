import copy
from dataclasses import dataclass

import numpy as np
import pandas as pd
import numpy
import random
import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

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
            self.base_crit_chance = ep[ep.name == name]['base_crit_chance'].values[0]
            self.crit_chance = ep[ep.name == name]['crit_chance'].values[0]
            self.crit_power = ep[ep.name == name]['crit_power'].values[0]
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
    player_att = []  # the list of attributes
    # [id,name,level,damage_min,damage_max,base_crit_chance,crit_chance,crit_power,defense,immunity,luck]
    player_health_energy = [100, 270]  # [health bar, energy bar]
    player_profession = []
    def __init__(self):
        """
        Initiate function for the players.
        """

    def set_profession(self, profession):
        """
        At 5 level Mininh skills, we can Choose Miner(+1 ore per vein) or Geologist(Chance for gems to appear in pairs)
        >>> player1 = Player()
        >>> player1.set_profession(['Miner'])
        >>> player1.player_pro
        ['Miner']
        """
        self.player_profession = profession
        self.player_pro = self.player_profession
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

    def set_player_att(self, given_lis):
        """
        to set the attributes of this player manually

        """
        self.player_att = given_lis

    def generate_att_from_equip(self):
        """
        to set the attributes of this player. according to the equipments, search for every equipment in the
        equipment_db and add total attributes

        >>> player1 = Player()
        >>> player1.set_player_equipments(['Infinity Dagger', 'Crabshell Ring', '', ''])
        >>> player1.generate_att_from_equip()
        >>> player1.player_att
        [50, 70, 0.06, 4, 0, 8, 0, 0]
        """
        this_damage_min = 0
        this_damage_min_bonus = 0
        this_damage_max = 0
        this_damage_max_bonus = 0
        this_base_crit_chance = 0
        this_crit_chance = 0
        this_crit_power = 0
        this_crit_power_bonus = 0
        this_defense = 0
        this_immunity = 0
        this_luck = 0
        if self.player_equipments:
            for i in range(0, len(self.player_equipments)):
                this_equip = Equipment(self.player_equipments[i])
                if "%" in str(this_equip.damage_min):
                    this_damage_min_bonus += int(this_equip.damage_min[0:2])
                else:
                    this_damage_min += int(this_equip.damage_min)
                print(this_damage_min_bonus)
                if "%" in str(this_equip.damage_max):
                    this_damage_max_bonus += int(this_equip.damage_max[0:2])
                else:
                    this_damage_max += int(this_equip.damage_max)
                this_base_crit_chance += float(this_equip.base_crit_chance)
                this_crit_chance += this_equip.crit_chance
                if "%" in str(this_equip.crit_power):
                    this_crit_power_bonus += int(this_equip.crit_power[0:2])
                else:
                    this_crit_power += float(this_equip.crit_power)
                this_defense += this_equip.defense
                this_immunity += this_equip.immunity
                this_luck += this_equip.luck
            if this_damage_min_bonus != 0:
                this_damage_min = this_damage_min * (100 + this_damage_min_bonus) / 100
            if this_damage_max_bonus != 0:
                this_damage_max = this_damage_max * (100 + this_damage_max_bonus) / 100
            if this_crit_power_bonus != 0:
                this_crit_power = this_crit_power * (100 + this_crit_power_bonus) / 100
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
        """

        :return:
        """
        print("******PLAYER******")
        print("player_skill_level:", self.player_skill_level)
        print("player_equipments:", self.player_equipments)
        att_lis = ["damage_min", "damage_max", "Base_crit_chance", "Crit_Chance", "Crit_Power", "Defense", "Immunity",
                   "Luck"]
        for i in range(0, len(att_lis)):
            print(att_lis[i], ":", self.player_att[i])
        print("player_health_energy:", self.player_health_energy)
        print("******PLAYER******")

    def reset(self):
        """
        reset the health and energy bar

        :return:
        """
        self.player_health_energy = [100, 270]


############
# Rock #
############
class Rock:
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
    The monsters information is here https://stardewvalleywiki.com/Monsters.
    """
    killable, HP, damage, defense, speed, XP, drop_rate = True, 0, 0, 0, 0, 0, {}
    drop_value = {"Diamond": 750, "Prismatic Shard": 2000, "Amethyst": 100, "Dwarf Scroll I": 1, "Dwarf Scroll II": 1,
                  "Dwarf Scroll III": 1, "Dwarf Scroll IV": 1, "Green Algae": 15, "Sap": 2, "Slime": 5, "Jade": 200,
                  "Coal": 15, "Ancient Seed": 5, "Bug Meat": 8, "White Algae": 25, "Bat Wings": 15, "Bomb": 50,
                  "Rare Disc": 300, "Cherry Bomb": 50, "Crab": 100, "Winter Root": 70}

    def __init__(self, level):
        """
        Create a monster with its name.
        """
        self.level = level
        self.if_bottom()

    def if_bottom(self):
        result = self.level == 120
        if result:
            self.drop_rate = {"Diamond": 0.0005, "Prismatic Shard": 0.0005, "nothing": 0.999}
        return result

    def generate_value(self):
        drop_lis = []
        total_val = 0

        for k, v in self.drop_rate.items():
            a = random.choices([k, "nothing"], weights=[v, (1 - v)])
            if a[0] != "nothing":
                drop_lis.append(a[0])

        for i in drop_lis:
            total_val += self.drop_value[i]
        # print(drop_lis)
        return total_val

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
                               "Sap": 0.15, "Slime": 0.8})  # TODO: Slime Hutch?


class FrostJelly(Slime):
    """A FrostJelly is a kind of Slime that could only be found on level 41-79 in the Mines."""
    # TODO: can sometimes be found on other floors? sr. https://stardewvalleywiki.com/Slimes
    HP, damage, defense, XP = 106, 7, 0, 6  # TODO: the attack might grow

    def drop(self):
        self.drop_rate.update({"Dwarf Scroll II": 0.005, "Dwarf Scroll III": 0.015, "Dwarf Scroll IV": 0.001,
                               "Jade": 0.02, "Sap": 0.5, "Slime": 0.75, "Winter Root": 0.08})
        # TODO: Slime Hutch?


class RedSludge(Slime):
    """A GreenSlime is a kind of Slime that could be found on any level in the Mines."""
    HP, damage, defense, XP = 205, 16, 0, 10

    def drop(self):
        self.drop_rate.update({"Coal": 0.01, "Dwarf Scroll III": 0.005, "Dwarf Scroll II": 0.001, "Green Algae": 0.1,
                               "Sap": 0.5, "Slime": 0.8, "White Algae": 0.1})  # TODO: Slime Hutch?
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


class Bat(Monster):
    """
    A Bat is one of the monster categories. It has several variations including FrostBat and LavaBat. Bat itself is
    also a monster that will appear. It only appears on floor 31-39.
    """
    HP, damage, defense, speed, XP = 24, 6, 1, 3, 3

    def drop(self):
        self.drop_rate.update({"Bat Wings": 0.94, "Bomb": 0.02, "Dwarf Scroll I": 0.005,
                               "Dwarf Scroll IV": 0.001, "Rare Disc": 0.01})


class FrostBat(Bat):
    """A FrostBat is a variation of Bat and could only be found on level 41-79 in the Mines."""
    HP, damage, XP = 36, 7, 7

    def drop(self):
        self.drop_rate.update({"Bat Wings": 0.95, "Bomb": 0.02, "Dwarf Scroll II": 0.005,
                               "Dwarf Scroll IV": 0.001, "Rare Disc": 0.01})


class LavaBat(Bat):
    """A LavaBat is a variation of Bat and could only be found on level 81-119 in the Mines."""
    HP, damage, XP = 80, 15, 15

    def drop(self):
        self.drop_rate.update({"Bat Wings": 0.97, "Bomb": 0.02, "Dwarf Scroll III": 0.005,
                               "Dwarf Scroll IV": 0.001, "Rare Disc": 0.01})


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


rc = RockCrab(2)
rc.drop()
rc.generate_value()
print("tt", rc.drop_rate)


class LavaCrab(Crab):
    """A LavaCrab is a variation of Crab and could only be found on level 80-119 in the Mines."""
    HP, damage, defense, speed, XP = 120, 15, 3, 3, 12

    def drop(self):
        self.drop_rate.update({"Bomb": 0.4, "Crab": 0.25, "Dwarf Scroll III": 0.005, "Dwarf Scroll IV": 0.001})


class Floor:
    """
    every floor has [30,50] rocks and [5,10] monsters. So the initiation will create
    a list of rocks and  a list of monsters based on this level.
    """

    def __init__(self, level):
        self.r = pd.read_csv('rock.csv')
        self.r.set_index("item", inplace=True)
        self.level = level
        self.floor_containers = []  # the list of the rocks in this floor
        self.floor_monsters = []  # the list of the monsters
        self.total_value = 0  # total value of all the rocks in this floor

    def randomItem(self, level):
        """
        >>> cur_floor = Floor(5)
        >>> cur_floor.randomItem(5)
        ['nothing']
        """
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
    def generate_rock_list(self, denominator: int, numerator: int, player_pro):
        """
        generate all the rocks in this floor.
        """
        rocks_num = random.randint(30, 50)
        if player_pro == 'Miner':
            rocks_num += 1
        for i in range(0, int((rocks_num / denominator) * numerator)):
            rock = self.randomItem(self.level)[0]
            self.floor_containers.append(rock)
            if player_pro == 'Geologist' and rock in ['Emerald', 'Aquamarine', 'Ruby', 'Amethyst', 'Topaz', 'Jade', 'Diamond']:
                self.total_value += Rock().rockValue(rock) * (Rock().rockNum(rock) + 1)
            else:
                self.total_value += Rock().rockValue(rock) * Rock().rockNum(rock)
        return self.floor_containers, self.total_value

    def generate_monster_list(self):
        """Generate all the monsters in this floor. Probs for defined monsters could be changed to be passed in."""
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
            monsters = {
                1: [GreenSlime(self.level), Bug(self.level), RockCrab(self.level)],
                2: [GreenSlime(self.level), Bat(self.level), Bug(self.level)],
                3: [GreenSlime(self.level), FrostBat(self.level), FrostJelly(self.level)],
                4: [GreenSlime(self.level), LavaBat(self.level), LavaCrab(self.level), RedSludge(self.level)]
            }
            section_i = section_finder(self.level)
            monster = random.choice(monsters[section_i])  # TODO: logic test unperformed
            self.floor_monsters.append(monster)
        return self.floor_monsters


class MainGame:
    """
    running the game
    """
    total_value = 0
    survive_between = [1, 1]
    if_gameover = False

    def __init__(self, level_start, player: Player, profession):
        self.survive_between = [level_start, level_start]
        self.this_player = player
        self.profession = profession
        while True:
            if self.if_gameover:
                break
            self.one_floor(level_start)
            level_start = level_start + 1
            self.survive_between[1] = level_start

    def one_floor(self, level):
        """
        simulate one floor

        :param level:
        :return:
        """
        monsters = Floor(level).generate_monster_list()
        count = 0  # how many monsters have been killed
        for monster in monsters:
            self.one_round_attack(monster, self.this_player)
            monster.drop()
            self.total_value += monster.generate_value()
            count = count + 1
            if self.if_gameover:
                break
        container, total_value = Floor(level).generate_rock_list(len(monsters), count, self.profession)
        if self.if_gameover is not True:
            for one_container in container:
                self.this_player.player_health_energy[1] -= random.choice([1, 2])
                if self.this_player.player_health_energy[1] < 0:
                    self.GameOver()
                    break
            if self.if_gameover is not True:
                self.total_value += total_value
                print("total value in level", level, ":", total_value)

    def GameOver(self):
        self.if_gameover = True
        print("#####GameOver#####")
        print("total_value_gained:", self.total_value)
        print("survived between:", self.survive_between)

    def one_round_attack(self, monster: Monster, player: Player):
        """
        total_damage_player = damage - defense_monster + if_crit*(3 + Crit_Power/50)
        total_damage_monster = damage - defense_player
        todo: immunity and debuff?

        :param monster:
        :param player:
        :return:
        """
        player_damage = random.randint(int(player.player_att[0]), int(player.player_att[1] + 1))
        crit_chance = player.player_att[2] + 0.02 * player.player_att[3]
        if_crit = random.choices([1, 0], weights=(crit_chance, (1-crit_chance)))
        total_damage_player = player_damage - monster.defense + if_crit[0] * (3 + player.player_att[4])/50
        total_damage_monster = monster.damage - player.player_att[3]
        if total_damage_player < 1:
            total_damage_player = 1
        if total_damage_monster < 1:
            total_damage_monster = 1
        while True:
            monster.HP = monster.HP - total_damage_player
            player.player_health_energy[1] -= 1
            if player.player_health_energy[1] < 0:
                self.GameOver()
                break
            if monster.HP < 0:
                self.this_player = player
                break
            player.player_health_energy[0] -= total_damage_monster
            if player.player_health_energy[0] < 0:
                self.GameOver()
                break


def simulation(player: Player, start_level: int, running_num: int, scenario: str, if_drawn: bool, profession):
    """
    Monte Carlo Simulation, playing the game for many times.

    :param player:
    :param start_level:
    :param running_num: the number of simulation
    :param scenario: the number of simulation
    :param if_drawn: if generate the chart
    :return: the average of every simulation
    """
    value_record = []
    for i in range(0, running_num):
        print("########" + str(i) + "########")
        player.reset()
        this_time = MainGame(start_level, player, profession)
        value_record.append(this_time.total_value)
    print(value_record)
    if if_drawn:
        plt.hist(value_record, bins=40)
        plt.savefig(scenario + "-" + "-" + str(running_num))
    print("The average value the player gained in this scenario is:" + str(sum(value_record) / len(value_record)))
    return sum(value_record) / len(value_record)


############
# Validating an MC simulation #
############
# 1. Statistical convergence ---see the output image
# 2. Control all other variables, to see if each component and the outcomes have a logical correlation


def test_correlation_damage():
    """
    Control all other variables, to see if each component and the outcomes have a logical correlation

    :return:
    """
    player_tp = Player()
    x_axis = []
    result_lis = []
    for i in range(10, 100, 5):
        min_damage = i
        max_damage = i + 10
        player_tp.set_player_att([min_damage, max_damage, 0, 0, 0, 0, 0, 0])
        result_lis.append(simulation(player_tp, 1, 100, "correlation_with_damage", False))
        x_axis.append(i)
    print(x_axis)
    print(result_lis)
    plt.plot(x_axis, result_lis, linestyle='dotted')
    plt.savefig("DamagaAndValue")
    corr = np.corrcoef(x_axis, result_lis)
    print(corr)
    return corr


def test_correlation_others(attr: str, profession):
    """
    Control all other variables, to see if each component and the outcomes have a logical correlation

    :return:
    """
    player_tp = Player()
    x_axis = []
    result_lis = []
    for i in range(1, 50):
        if attr == "crit_power":
            player_tp.set_player_att([30, 40, 0, 0.5, i, 0, 0, 0])
        elif attr == "luck":
            player_tp.set_player_att([30, 40, 0, 0, 0, 0, 0, i])
        else:
            return None
        result_lis.append(simulation(player_tp, 1, 100, "correlation_with_damage", False, profession))
        x_axis.append(i)
    print(x_axis)
    print(result_lis)
    plt.plot(x_axis, result_lis, linestyle='dotted')
    plt.savefig(attr + "AndValue")
    corr = np.corrcoef(x_axis, result_lis)
    print(corr)
    return corr


############
# hypothesis1 #
# When equipped with the infinity dagger, it is more rewarding to start from 80th floor than from 0 floor. #
############
# player1 = Player()
# a = 'Sneakers'
# equ = Equipment(a)
# b = "Infinity Dagger"
# equ = Equipment(b)
# player1.set_player_equipments([a, b, '', ''])
# player1.generate_att_from_equip()
# simulation(player1, 1, 1000, "hypothesis1-1", True, profession=None)
# simulation(player1, 80, 1000, "hypothesis1-80", True,profession=None)
############

############
# hypothesis 2 #
# When reaching level 5 of mining skill, it is more rewarding to choose miner than geologist. #
# We set the player equipments Sneakers and Infinity Dagger #
# run the simulation 500 times each for miner and geologist #
# compare the total gold gained from miner and geologist #
# according to diagram and the mean gold value, the geologist can gain more gold than miner.
############

def simulation_hypo2(player: Player, start_level: int, running_num: int, scenario: str, if_drawn: bool, profession):
    """
    Monte Carlo Simulation, playing the game for many times.

    :param player:
    :param start_level:
    :param running_num: the number of simulation
    :param scenario: the number of simulation
    :param if_drawn: if generate the chart
    :return: the average of every simulation
    """
    value_record = []
    for i in range(0, running_num):
        # print("########" + str(i) + "########")
        player.reset()
        this_time = MainGame(start_level, player, profession)
        value_record.append(this_time.total_value)
    # print(value_record)
    if if_drawn:
        plt.hist(value_record, bins=40, label = profession)
        plt.savefig(scenario + "-" + "-" + str(running_num))
        plt.xlabel("Number of Simulation", fontsize=12)
        plt.ylabel("Total Value", fontsize=12)
        handles = [Rectangle((0, 0), 1, 1, color=c) for c in ["Blue", "Orange"]]
        labels = ["Miner", "Geologist"]
        plt.legend(handles, labels)


    print("The average value the player gained in this scenario is:" + str(sum(value_record)/len(value_record)))
    return sum(value_record)/len(value_record)

a = 'Miner'
b = 'Geologist'
Miner_player = Player()
Geologist_player = Player()
Miner_player.set_profession([a])
Geologist_player.set_profession([b])
Miner_player.set_player_equipments(['Sneakers', "Infinity Dagger", '', ''])
Miner_player.generate_att_from_equip()
Geologist_player.set_player_equipments(['', '', '', ''])
Geologist_player.generate_att_from_equip()
simulation_hypo2(Miner_player, 1, 500, "hypothesis2-Miner", True, a)
simulation_hypo2(Miner_player, 1, 500, "hypothesis2-Geologist", True, b)
# simulation_hypo2(Miner_player, 1, 500, "hypothesis2-Geologist", True, a)

############
# hypothesis3 #
# The ruby ring is more useful than the jade ring when equipped with Burglar's Shank. #
############

# player_ruby = Player()
# a3 = 'Sneakers'
# b3 = "Burglar's Shank"
# c3 = "Ruby Ring"
# player_ruby.set_player_equipments([a3, b3, c3, ''])
# player_ruby.generate_att_from_equip()
# simulation(player_ruby, 1, 10, "hypothesis3-RubyRing", True, profession=None)
# player_jade = Player()
# d3 = "Jade Ring"
# player_jade.set_player_equipments([a3, b3, d3, ''])
# player_jade.generate_att_from_equip()
# simulation(player_jade, 1, 10, "hypothesis3-JadeRing", True, profession=None)
############

# test_correlation_others("crit_power", profession = None)
