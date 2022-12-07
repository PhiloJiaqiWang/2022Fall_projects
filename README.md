# 2022Fall_projects
## Game Background
Stardew Valley is an open-ended country-life RPG! You’ve inherited your grandfather’s old farm plot in Stardew Valley. There is one part in this game that you can take adventures under the mines. There are 120 floors (sometimes called levels) in the Mines. Ore type and quantity increases as The Player moves deeper into the Mines. The Mines are filled with rocks and dirt patches. Rocks can be mined with a Pickaxe in order to obtain Stone, ore and Geodes. To advance deeper in the Mines, a ladder must be revealed on each floor. The ladder will appear after breaking rocks or after defeating an enemy (killing enemies is the stamina-free option to finding ladders). 
## The Mines
Elements
Floor
There are 120 floors in total, the map is drawn randomly with different types, and there are random rocks scattered in the floor.
To get to the next floor, you need to find the ladder which is hid under a random rock.
There is an elevator to get you to 10, 20, 30…, those floors have treasure chest with different items
Rocks
Rocks are randomly scattered in the floor. You need a pickaxe to crack the rock. Stone, ore and Geodes will be gained with a set probability. The probability is listed on the Stardew Valley Wiki. The geodes require extra step to be cracked again (money cost) to gain actual items.
There is one rock under which is the ladder
Equipment
The player can equip a weapon, a pair of footwear and two rings, which affects the attacking attributes.
Skill level
There are five different skills in the game, but only the mining skills is considered in out simulation.
There are 10 levels in total, when achieving level 5, you can choose different occupation, and each will lead to different rewards in the next 5 levels.
Monster
There will be monsters in each floor. The types of monsters vary through the depth of the floor, and different monsters have unique traits. After killing a monster, items will be dropped.
Attack
Attack happens between the player and the monsters.
The attributes include : Attack, Crit. Chance, Crit. Power, Defense, Immunity, Luck, Magnetism, Speed, Weight
Health bar and Energy bar
The attack from the monsters affects the health bar, the using of pickaxe and player attacking affects the energy bar
Prerequisites for using Monte Carlo
Rerun and Independence: We consider the exhaustion of either health bar or energy bar as the end of one day. So, tomorrow is another day!!!
summary of aggregate statistics:
we compare the total values of gained items in this one-day mining. Since it generates a whole bunch of data, we will draw it using pandas to see the trends (if convergent, we guess it might be a normal distribute). Simply using the mean value and the variance could also be the metrics.
Experiments and predictions
We will use it to verify our hypothesis
## Hypothesis
1. When equipped with the infinity dagger, it is more rewarding to start from 80th floor than from 1st  floor.
2. The ruby ring is more useful than the jade ring when equipped with Burglar's Shank and starts from 1st floor.
3. When reaching level 5 of mining skills, it is more rewarding to choose miner than geologist.
