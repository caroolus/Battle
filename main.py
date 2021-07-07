from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item
import random

# Black Magic
fire = Spell("Fire", 25, 600, "black")
thunder = Spell("Thunder", 25, 600, "black")
blizzard = Spell("Blizzard", 25, 600, "black")
meteor = Spell("Meteor", 40, 1200, "black")
quake = Spell("Quake", 14, 140, "black")
#sacrifacial_pact = Spell("Sacrifacial pact", )

# White Magic
cure = Spell("Cure", 25, 620, "white")
cura = Spell("Cura", 50, 1500, "white")

# Items
potion = Item("Potion", "potion", "Heals 500 HP", 500)
hipotion = Item("Hi-potion", "potion", "Heals 1000 HP", 1000)
superpotion = Item("Super Potion", "potion", "Heals 2000 HP", 2000)

elixer = Item("Elixer", "elixer", "Restore HP/MP one party's member to max", 9999)
hielixer = Item("MegaElixer", "elixer", "Restore party's HP/MP to max", 9999)

grenade = Item("Grenade", "attac", "Deals 500 damage", 500)

player_spells = [fire, thunder, blizzard, meteor, cure, cura]
enemy_spells = [fire, meteor, cure]

player_items = [{"item": potion, "quantity": 15},
                {"item": hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 5},
                {"item": elixer, "quantity": 5},
                {"item": hielixer, "quantity": 5},
                {"item": grenade, "quantity": 5}]

# Instantiate People
player1 = Person("Wrosal ", 3260, 132, 300, 34, player_spells, player_items)
player2 = Person("Czapli ", 4160, 188, 311, 34, player_spells, player_items)
player3 = Person("Lemur  ", 3009, 174, 288, 34, player_spells, player_items)

enemy1 = Person(" Imp   ", 1250, 130, 560, 325, enemy_spells, [])
enemy2 = Person(" Rondo ", 11200, 700, 525, 25, enemy_spells, [])
enemy3 = Person(" Imp   ", 1250, 130, 560, 325, enemy_spells, [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

running = True
i = 0
print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)
# 1*"█" = 1.6*" "
while running:
    print("=" * 20)
    print("NAME:             HP:                                    MP:")
    for player in players:
        player.get_stats()

    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:

            player.chose_action()
            choice = input("    Chose action:")
            index = int(choice) - 1

            if index == 0:
                    dmg = player.generate_damage()
                    enemy = player.chose_target(enemies)

                    enemies[enemy].take_damage(dmg)
                    print("You attacted " + enemies[enemy].name.replace(" ", "") + " for", dmg, "points of damage. ")
                    if enemies[enemy].get_hp() == 0:
                        print(enemies[enemy].name.replace(" ", "") + " is died")
                        del enemies[enemy]

            elif index == 1:
                    player.chose_magic()
                    magic_choice = int(input("    Chose spell:")) - 1
                    spell = player.magic[magic_choice]
                    magic_dmg = spell.generate_damage()

                    current_mp = player.get_mp()

                    if magic_choice == -1:
                        continue

                    if spell.cost > current_mp:
                            print(bcolors.FAIL + "\nYou don't have MP.\n" + bcolors.ENDC)
                            continue

                    player.reduce_mp(spell.cost)
                    if spell.type == "white":
                            player.heal(magic_dmg)
                            print(bcolors.OKBLUE + "\n" + spell.name + "heals for" + str(magic_dmg)
                                  + "HP" + bcolors.ENDC)
                    elif spell.type == "black":
                        enemy = player.chose_target(enemies)

                        enemies[enemy].take_damage(magic_dmg)
                        print(bcolors.FAIL + "You attacted " + enemies[enemy].name.replace(" ", "") +
                              " for:", magic_dmg, "points of damage. " + bcolors.ENDC)

                        if enemies[enemy].get_hp() == 0:
                            print(enemies[enemy].name.replace(" ", "") + " is died")
                            del enemies[enemy]

            elif index == 2:
                player.chose_items()
                item_choice = int(input("    Chose item:"))-1

                if item_choice == -1:
                    continue

                item = player.items[item_choice]["item"]

                if player.items[item_choice]["quantity"] == 0:
                    print(bcolors.FAIL + "None left..." + bcolors.ENDC)
                    continue

                player.items[item_choice]["quantity"] -= 1

                if item.type == "potion":
                    player.heal(item.prop)
                    print(bcolors.WARNING + item.name + " heals: " + str(item.prop) + "HP" + bcolors.ENDC)
                elif item.type == "elixer":
                    if item.name == "MegaElixer":
                        for i in players:
                            i.hp = i.maxhp
                            i.mp = i.maxmp
                        else:
                            player.hp = player.maxhp
                            player.mp = player.maxmp
                    print(bcolors.OKGREEN + "\n" + item.name + "fully restores MP/HP" + bcolors.ENDC)
                elif item.type == "attac":
                    enemy = player.chose_target(enemies)
                    enemies[enemy].take_damage(item.prop)
                    print(bcolors.FAIL + "\n" + item.name + " deals " + str(item.prop) + " points of damage to: "
                          + enemies[enemy].name.replace(" ", "") + bcolors.ENDC)
                    if enemies[enemy].get_hp() == 0:
                        print(enemies[enemy].name.replace(" ", "") + " is died")
                        del enemies[enemy]
    print("\n")
    # Enemy attack phase
    for enemy in enemies:
        enemy_choice = random.randrange(0, 2)
        target = random.randrange(0, len(players))
        if enemy_choice == 0:
            enemy_dmg = enemy.generate_damage()

            players[target].take_damage(enemy_dmg)
            print(enemy.name.replace(" ", "") + " deals", enemy_dmg, "points of damage to: "
                  + players[target].name.replace(" ", ""))
            if players[target].get_hp() == 0:
                print(players[target].name.replace(" ", "") + " is died")
                del players[target]

        elif enemy_choice == 1:
            spell, magic_dmg = enemy.enemy_chose_spell()
            enemy.reduce_mp(spell.cost)

            if spell.type == "white":
                enemy.heal(magic_dmg)
                print(bcolors.OKBLUE + spell.name + " heals " +
                      enemy.name.replace(" ", "") + " for " + str(magic_dmg) + " HP" + bcolors.ENDC)
            elif spell.type == "black":
                players[target].take_damage(magic_dmg)
                print(bcolors.OKBLUE + enemy.name.replace(" ", "") + " deals " + str(magic_dmg)
                      + " points of damage to " + players[target].name + bcolors.ENDC)

                if players[target].get_hp() == 0:
                    print(players[target].name.replace(" ", "") + " is died")
                    del players[target]


    # Check if battle is over
    defeated_enemies = 0
    defeated_players = 0

    for enemy in enemies:
        if enemy.get_hp == 0:
            defeated_enemies += 1

    for player in players:
        if player.get_hp == 0:
            defeated_players += 1
    # Check if Player won
    if defeated_enemies == 3:
        print(bcolors.HEADER + "You win!" + bcolors.ENDC)
        runnig = False
    # Check if Enemy won
    elif defeated_players == 3:
        print(bcolors.FAIL + "You lost. Enemies wins :(" + bcolors.ENDC)
        runnig = False

