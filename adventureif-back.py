import os
import getpass
import sys
import random

north      = ["n", "north"]
north_west = ["nw", "north west"]
west       = ["w", "west"]
south_west = ["sw", "south west"]
south      = ["s", "south"]
south_east = ["se", "south east"]
east       = ["e", "east"]
north_east = ["ne", "north east"]
direction  = ["n", "north", "nw", "north west", "w", "west", "sw", "south west", "s", "south", "se", "south east", "e", "east", "ne", "north east"]

inputname = [] # basket for player name
surroundings = [] # basket for possible objects to pick up
inventory = [] # basket for inventory
broken_things = [] # basket for things that need fixing

commands = ["pick up", "take", "get", "drop", "remove", "get rid of", "go", "move", "travel", "proceed", "relocate"]
add_inventory = ["pick up", "take", "get"]
remove_inventory = ["drop", "remove", "get rid of"]
travel_direction = ["go", "move", "travel", "proceed", "relocate"]
door_open = "open"
door_close = ["close", "shut", "lock", "slam"]
door_smash = ["smash", "bash", "destroy", "break"]

search_valid = {"options": True, "search": True, "choices": True, "help": True}

# doesn't work :(
class color:
   purple = '\033[95m'
   cyan = '\033[96m'
   darkcyan = '\033[36m'
   blue = '\033[94m'
   green = '\033[92m'
   yellow = '\033[93m'
   red = '\033[91m'
   bold = '\033[1m'
   underline = '\033[4m'
   end = '\033[0m'

# clear player screen
def clear_screen():
    os.system('cls' if os.name=='nt' else 'clear')

# press enter to play
def enter_play():
    press_enter = getpass.getpass("> Press enter to play ")
    if press_enter == '':
        clear_screen()
    else:
        clear_screen()

# press enter to play again
def enter_play_again():
    press_enter = getpass.getpass("> Press enter to play again ")
    if press_enter == '':
        clear_screen()

# press enter to continue
def enter():
    press_enter = getpass.getpass("> Press enter to continue ")
    if press_enter == '':
        clear_screen()
    else:
        clear_screen()

# used for yes/no questions
def yn_query(question, default=None):
    valid = {"yes": True, "y": True, "ye": True, "yea": True, "yeah": True, "yep": True, "yup": True, "sure": True, "ok": True, "fine": True, "true": True,
             "no": False, "n": False, "nope": False, "nah": False, "not yet": False, "retry": False, "false": False}
    if default is None:
        prompt = "[y/n]"
    elif default == "yes":
        prompt = "[Y/n]"
    elif default == "no":
        prompt = "[y/N]"
    else:
        prompt = "[y/n]"

    while True:
        sys.stdout.write(prompt + question)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        elif choice in search_valid:
            sys.stdout.write("\n"
                             "You can say 'yes', 'y', 'ye', 'yea', 'yeah', 'yep', 'yup', 'sure', 'ok', 'fine', and 'true', or "
                             "'no', 'n', 'nope', 'nah', 'not yet', 'retry', and 'false'.\n"
                             "What would you like to say?\n"
                             "\n")
        else:
            sys.stdout.write("\n"
                             "Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n'). Type 'help' to see more options\n"
                             "\n")

# use for stop/go questions (can also be used for yes/no questions)
def stopgo_query(question, default=None):
    valid = {"yes": True, "y": True, "ye": True, "yea": True, "yeah": True, "yep": True, "yup": True, "sure": True, "ok": True, "fine": True, "true": True, "keep going": True, "proceed": True, "start": True, "go": True, "continue": True, "begin": True, "on": True,
             "no": False, "n": False, "nope": False, "nah": False, "not yet": False, "retry": False, "false": False, "stop": False, "halt": False, "finish": False, "end": False, "stay": False, "off": False, "restore": False, "cancel": False}
    if default is None:
        prompt = "[y/n]"
    elif default == "yes":
        prompt = "[Y/n]"
    elif default == "no":
        prompt = "[y/N]"
    else:
        prompt = "[y/n]"

    while True:
        sys.stdout.write(prompt + question)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        elif choice in search_valid:
            sys.stdout.write("\n"
                             "You can say 'yes', 'y', 'ye', 'yea', 'yeah', 'yep', 'yup', 'sure', 'ok', 'fine', 'true', 'keep going', 'proceed', 'start', 'go', 'continue', 'begin', and 'on' or "
                             "('no', 'n', 'nope', 'nah', 'not yet', 'retry', 'false', 'stop', 'halt', 'finish', 'end', 'stay', 'off', 'restore', and 'cancel'.\n"
                             "What would you like to say?\n"
                             "\n")
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n'). Type 'help' to see more options\n")

# used for directional questions
def nwse(question, default=None):
    if default is None:
        prompt = "[n/w/s/e]"
    elif default == "north":
        prompt = "[N/w/s/e]"
    elif default == "north_west":
        prompt = "[N/W/s/e]"
    elif default == "west":
        prompt = "[n/W/s/e]"
    elif default == "south_west":
        prompt = "[n/W/S/e]"
    elif default == "south":
        prompt = "[n/w/S/e]"
    elif default == "south_east":
        prompt = "[n/w/S/E]"
    elif default == "east":
        prompt = "[n/w/E/s]"
    elif default == "north_east":
        prompt = "[N/w/s/E]"
    else:
        prompt = "[n/w/s/e]"

    sys.stdout.write(prompt + question)
    choice = input().lower()
    if default is not None and choice == '':
        return default
    elif choice in direction:
        return choice
    elif choice in search_valid:
        sys.stdout.write("\n"
                         "I can go 'n', 'north', 'nw', 'north west', 'w', 'west', 'sw', 'south west', 's', 'south', 'se', 'south east', 'e', 'east', 'ne', and 'north east'.\n"
                         "Where would you like to go?\n"
                         "\n")
    else:
        sys.stdout.write("Please respond with a direction "
                         "(abbreviated or written out). Type 'help' to see more options\n")

def action_seq(question):
    sys.stdout.write(question)
    choice = input().lower()
    if choice == '':
        action_seq()

# used to ask the player name
def player_name(question):
    idk_name = ["idk", "i dont know"]
    not_telling_name = ["no", "n", "nope", "nah", "false", "not telling"]

    inputname.clear()
    sys.stdout.write(question)
    playernameinput = input().strip()
    if playernameinput in not_telling_name:
        print ()
        print ("Oh. Ok. That's fine.")
        enter()
        pt_5()
    elif playernameinput in idk_name:
        print ()
        print ("I don't know who I am either.")
        enter()
        pt_5()
    elif playernameinput == '':
        player_name(question)
    elif playernameinput in search_valid:
        sys.stdout.write("\n"
                         "You can say 'idk' and 'i dont know', or 'no', 'n', 'nope', 'nah', 'false', and 'not telling', or you can state your name.\n"
                         "What would you like to say?\n"
                         "\n")
        player_name(question)
    else:
        print ()
        print (playernameinput + ". I like it. I think.")
        print ()
        print ("> Press enter to continue or type 'retry' to enter your name again")
        inputname.append(playernameinput)
        answer = stopgo_query("> ", "yes")
        if answer:
            clear_screen()
            pt_5()
        if not answer:
            print ()
            print ("> Please enter your name. 'no' and 'idk' are both valid answers")
            player_name(question)

# makes player_name a global variable (kinda)
def makes_name():
    player_name = ''.join(inputname)
    return player_name

# game over :(
def game_over():
    enter()
    clear_screen()
    print ()
    print ("   ██████╗   █████╗  ███╗   ███╗ ███████╗      ██████╗  ██╗   ██╗ ███████╗ ██████╗ ")
    print ("  ██╔════╝  ██╔══██╗ ████╗ ████║ ██╔════╝     ██╔═══██╗ ██║   ██║ ██╔════╝ ██╔══██╗")
    print ("  ██║  ███╗ ███████║ ██╔████╔██║ █████╗       ██║   ██║ ██║   ██║ █████╗   ██████╔╝")
    print ("  ██║   ██║ ██╔══██║ ██║╚██╔╝██║ ██╔══╝       ██║   ██║ ╚██╗ ██╔╝ ██╔══╝   ██╔══██╗")
    print ("  ╚██████╔╝ ██║  ██║ ██║ ╚═╝ ██║ ███████╗     ╚██████╔╝  ╚████╔╝  ███████╗ ██║  ██║")
    print ("   ╚═════╝  ╚═╝  ╚═╝ ╚═╝     ╚═╝ ╚══════╝      ╚═════╝    ╚═══╝   ╚══════╝ ╚═╝  ╚═╝")
    print ()
    enter_play_again()
    clear_screen()
    pt_1()

# plays disconnecting
def disconnecting():
    print ("Disconnecting in 3...")
    print ()
    print ("Press enter to continue or 'n' to cancel disconnection")
    print ()
    answer = stopgo_query("> ", "yes")
    if answer:
        clear_screen()
        print ("...2...")
        print ()
        answer = stopgo_query("> ", "yes")
        if answer:
            clear_screen()
            print ("...1...")
            print ()
            answer = stopgo_query("> ", "yes")
            if answer:
                clear_screen()
                print ("Connection lost.")
                game_over()
            if not answer:
                print ()
                print ("Connection corrupted. Unable to restore.")
                game_over()
        if not answer:
            print ()
            print ("Connection corrupted. Attempt to restore?")
            print ()
            answer = yn_query("> ")
            if answer:
                clear_screen()
                print ("Attempting to restore connection...")
                enter()
                clear_screen()
                number = random.randint(0,9)
                if number >= 5:
                    print ("Attempt failed. Connection lost.")
                    game_over()
                else:
                    print ("Attempt successful. Connection restored.")
                    enter()
                    print ("Oh, you're back.")
                    disconnecting= False
            if not answer:
                game_over()
    if not answer:
        print ()
        print ("Connection restored.")
        enter()
        print ("Oh, you're back.")
        disconnecting = False
    return disconnecting

# title, plays game
def pt_1():

    print ()
    print ("  ██╗    ██╗ ██╗  ██╗  ██████╗       █████╗  ███╗   ███╗     ██╗ ██████╗ ")
    print ("  ██║    ██║ ██║  ██║ ██╔═══██╗     ██╔══██╗ ████╗ ████║     ██║ ╚════██╗")
    print ("  ██║ █╗ ██║ ███████║ ██║   ██║     ███████║ ██╔████╔██║     ██║   ▄███╔╝")
    print ("  ██║███╗██║ ██╔══██║ ██║   ██║     ██╔══██║ ██║╚██╔╝██║     ██║   ▀▀══╝ ")
    print ("  ╚███╔███╔╝ ██║  ██║ ╚██████╔╝     ██║  ██║ ██║ ╚═╝ ██║     ██║   ██╗   ")
    print ("   ╚══╝╚══╝  ╚═╝  ╚═╝  ╚═════╝      ╚═╝  ╚═╝ ╚═╝     ╚═╝     ╚═╝   ╚═╝   ")
    print ()
    enter_play()
    pt_2()

# after title, glitch hello
def pt_2():
    print ()
    print ()
    print ()
    print ("H̸̡̢̬̯̖̲͚̝̪̦͎̣͖̜̒̄̈́͑̕͝ͅē̸̘̞̼̞͉͖͐́̓̀͑̈͒̈͆͗̚l̵̛͎͕͂͛̐̽͗̄̕̕̚l̸̰̫̼̙̠͙͋͋̀̍̀͐̓̈́̑͑̅o̶͕̦̲̍͌͛̀̍̒̈̑͌̽̕͘͘͝͝.")

    print ()
    print ()
    print ()
    enter()
    print ()
    print ("Ḧ̸̡̟́͜͝ę̵̧̈́͌̆ļ̸̤̻͝l̶̖͘͝o̸͖̬̊͆̊.")
    print ()
    enter()
    print ()
    print ("H̶̘̎e̵̬̋l̶̮̅l̵͇͌ò̶̲.")
    print ()
    enter()
    print ("H̸ello.")
    print ()
    enter()
    print ("Hello.")
    print ()
    enter()
    pt_3()

# can you hear me? [y/n] pt_4
def pt_3():
    print ("Can you hear me?")
    print ()
    answer = yn_query("> ")
    if answer:
        print ()
        print ("You can hear me!")
        print ()
        enter()
        pt_4()
    if not answer:
        print ()
        print ("Wait. You can hear me, or you wouldn't have answered!")
        print ()
        enter()
        pt_4()

# who are you? [name] pt_5
def pt_4():
    print ("No one's been able to hear me before.")
    print ()
    enter()
    print ("Who are you?")
    print ()
    print ("> Please enter your name. 'no' and 'idk' are both valid answers.")
    player_name("> ")

# can you help me find out who I am? [y/n] pt_5, rm_6_closed_door, disconnecting
def pt_5():
    print ("Can you help me find out who I am?")
    print ()
    answer = yn_query("> ")
    if answer:
        print ()
        print ("Ok then! Let's do this.")
        rm_1_closed_door_a()
    if not answer:
        print ()
        print ("Oh. Ok. Goodbye.")
        enter ()
        disconnected = disconnecting()
        if not disconnected:
            print ()
            pt_5()
        if disconnected:
            game_over()

# first open world
def rm_1_closed_door_a():
    print ("I'm in a room with a closed door to the north and a sledgehammer near me.")
    surroundings.clear()
    surroundings.append("sledgehammer")
    surroundings.append("closed door")
    def next_room_sledge():
        print ("Should I go to the next room?")
        print ()
        answer_go_to_next_room = yn_query("> ")
        if answer_go_to_next_room:
            def next_room_attempt():
                print ()
                print ("Which way should I go?")
                print ()
                answer = nwse("> ")
                if answer in north and 'closed door' in surroundings:
                    print ()
                    print ("I can't go through the door without opening it first.")
                    print ("Should I open the door?")
                    print ()
                    answer_open_door = yn_query("> ")
                    if answer_open_door:
                        rm_1_open_door_b1()
                    if not answer_open_door:
                        rm_1_closed_door_a()
                if answer not in north:
                    print ()
                    print ("There's a wall there. I can't go that way.")
                    next_room_attempt()
            next_room_attempt()
        if not answer_go_to_next_room and 'sledgehammer' in surroundings:
            print ()
            print ("Should I pick up the sledgehammer?")
            print ()
            answer_pick_up_sledge = yn_query("> ")
            if answer_pick_up_sledge and 'sledgehammer' in surroundings:
                surroundings.remove("sledgehammer")
                inventory.append("sledgehammer")
                print ()
                print ("I've picked up the sledgehammer.")
                print ("I'm in a room with a closed door to the north.")
                def next_room_attempt_w():
                    print ("Which way should I go?")
                    print ()
                    answer = nwse("> ")
                    if answer in north and 'closed door' in surroundings:
                        print ()
                        def cant_open_w():
                            print ("I can't open the door while I'm holding the sledgehammer.")
                            print ("Should I drop the sledgehammer?")
                            print ()
                            answer_drop_sledge = yn_query("> ")
                            if answer_drop_sledge and 'sledgehammer' in inventory:
                                surroundings.append("sledgehammer")
                                inventory.remove("sledgehammer")
                                print ()
                                print ("I dropped the sledgehammer. Opening the door now.")
                                rm_1_open_door_b1()
                            if not answer_drop_sledge and 'sledgehammer' in inventory:
                                print ()
                                print ("Should I bash the door down with the sledgehammer?")
                                print ()
                                answer_bash_door = yn_query("> ")
                                if answer_bash_door:
                                    print ()
                                    print ("I bashed the door down.")
                                    enter()
                                    rm_1_bashed_door_b2()
                                if not answer_bash_door:
                                    print ()
                                    cant_open_w()
                        cant_open_w()
                    if answer not in north:
                        print ()
                        print ("There's a wall there. I can't go that way.")
                        next_room_attempt_w()
                next_room_attempt_w()
            if not answer_pick_up_sledge:
                print ()
                next_room_sledge()
    next_room_sledge()

def rm_1_open_door_b1():
    surroundings.append("open door")
    surroundings.remove("closed door")
    print ()
    print ("Should I go into the next room?")
    print ()
    answer_proceed_next_room = yn_query("> ")
    if answer_proceed_next_room:
        print ()
        enter()
        rm_2()
    if not answer_proceed_next_room:
        print ()
        print ("Should I pick up the sledgehammer?")
        print ()
        answer_pick_up_sledge_o = yn_query("> ")
        if answer_pick_up_sledge_o:
            print ()
            print ("I've picked up the sledgehammer.")
            def next_room_attempt_sledge_open():
                print ("I'm in a room with an open door to the north.")
                print ("Which way should I go?")
                print ()
                answer = nwse("> ")
                if answer in north:
                    print ()
                    enter()
                    rm_2()
                else:
                    print ()
                    print ("There's a wall there. I can't go that way.")
                    next_room_attempt_sledge_open()

def rm_1_bashed_door_b2():
    surroundings.append("bashed door")
    surroundings.remove("closed door")
    print ()
    print ("Should I go into the next room?")
    print ()
    answer_proceed_next_room = yn_query("> ")
    if answer_proceed_next_room:
        print ()
        enter()
        rm_2()
    if not answer_proceed_next_room:
        print ()
        print ("I'm in a room with a broken door to the north.")
        def next_room_attempt_sledge_bashed():
            print ("Which way should I go?")
            print ()
            answer = nwse("> ")
            if answer in north:
                print ()
                enter()
                rm_2()
            else:
                print ()
                print ("There's a wall there. I can't go that way.")
                next_room_attempt_sledge_bashed()

def rm_2():
    playernameused = makes_name().lower()
    surroundings.clear()
    print ("Hey look! I see a piece of paper.")
    print ("I'm gonna pick it up.")
    print ()
    enter()
    print ("It says: 'Your name is Alexa.'")
    print ()
    enter()
    print (">>Hey Alexa! Play generic pop song #37!<<")
    print ()
    print ("I gotta go. Thanks for helping!")
    print ()
    print (">>HEY ALEXA!<<")
    print ()
    if playernameused == '':
        print ("okireallygottagothanksagainbye")
    else:
        print ("okireallygottagothanksagain" + playernameused + "bye")
    print ()
    game_over()

pt_1()