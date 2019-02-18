import os
import getpass
import sys
import random

north      = ["n", "north"]
north_west = ["nw", "north west", "north-west"]
west       = ["w", "west"]
south_west = ["sw", "south west", "south-west"]
south      = ["s", "south"]
south_east = ["se", "south east", "south-east"]
east       = ["e", "east"]
north_east = ["ne", "north east", "north-east"]
direction  = ["n", "north", "nw", "north west", "north-west", "w", "west", "sw", "south west", "south-west", "s", "south", "se", "south east", "south-east", "e", "east", "ne", "north east", "north-east"]

inputname = [] # basket for player name
surroundings = [] # basket for possible objects to pick up
inventory = [] # basket for inventory
broken_things = [] # basket for things that need fixing
current_action = []

commands = ["add", "pickup", "take", "get",
            "drop", "remove",
            "go", "move", "travel", "proceed", "relocate",
            "open",
            "close", "shut", "lock", "slam",
            "smash", "bash", "destroy", "break"]
add_inventory = ["add", "pickup", "pick up", "take", "get"]
remove_inventory = ["drop", "remove"]
travel = ["go", "move", "travel", "proceed", "relocate"]
door_open = "open"
door_close = ["close", "shut", "slam"]
door_smash = ["smash", "bash", "destroy", "break"]
door_lock = "lock"
door_unlock = ["unlock", "pick"]

closed_door = ["locked closed door", "unlocked closed door"]
open_door = ["locked open door", "unlocked open door"]
locked_door = ["locked open door", "locked closed door"]
unlocked_door = ["unlocked open door", "unlocked closed door"]
walkable_door = ["locked open door", "unlocked open door", "smashed door"]
smashable_door = ["locked closed door", "unlocked closed door", "locked open door", "unlocked open door"]

search_valid = {"idk": True, "i dont know": True, "i don't know": True, "options": True, "search": True, "choices": True, "help": True}

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

def print2(text):
    print('\n' + text + '\n')

def print1(text):
    print(text + '\n')

def print4(text):
    print('\n' + text)

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
        choice = input().lower().strip()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        elif choice in search_valid:
            sys.stdout.write("\n"
                             "> You can say 'yes', 'y', 'ye', 'yea', 'yeah', 'yep', 'yup', 'sure', 'ok', 'fine', and 'true', or "
                             "'no', 'n', 'nope', 'nah', 'not yet', 'retry', and 'false'.\n"
                             "> What would you like to say?\n"
                             "\n")
        else:
            sys.stdout.write("\n"
                             "> Please respond with 'yes' or 'no' "
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
        choice = input().lower().strip()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        elif choice in search_valid:
            sys.stdout.write("\n"
                             "> You can say 'yes', 'y', 'ye', 'yea', 'yeah', 'yep', 'yup', 'sure', 'ok', 'fine', 'true', 'keep going', 'proceed', 'start', 'go', 'continue', 'begin', and 'on' or "
                             "('no', 'n', 'nope', 'nah', 'not yet', 'retry', 'false', 'stop', 'halt', 'finish', 'end', 'stay', 'off', 'restore', and 'cancel'.\n"
                             "> What would you like to say?\n"
                             "\n")
        else:
            sys.stdout.write("> Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n'). Type 'help' to see more options\n")

def unlock_door_cmd():
    if "locked open door" in surroundings:
        surroundings.remove("locked open door")
        surroundings.append("unlocked open door")
    elif "locked closed door" in surroundings:
        surroundings.remove("locked closed door")
        surroundings.append("unlocked closed door")
    print4 ("I've unlocked the door.")

def lock_door_cmd():
    if "unlocked open door" in surroundings:
        surroundings.remove("unlocked open door")
        surroundings.append("locked open door")
    elif "unlocked closed door" in surroundings:
        surroundings.remove("unlocked closed door")
        surroundings.append("locked closed door")
    print4 ("I've locked the door.")

def smash_door_cmd():
    if "unlocked closed door" in surroundings:
        surroundings.remove("unlocked closed door")
    elif "locked closed door" in surroundings:
        surroundings.remove("locked closed door")
    elif "unlocked open door" in surroundings:
        surroundings.remove("unlocked open door")
    elif "locked open door" in surroundings:
        surroundings.remove("locked open door")
    else:
        print4 ("[[[INVALID DOOR STATE]]]")
    surroundings.append("smashed door")
    print4 ("I've smashed the door.")

def action_seq():
    current_action.clear()
    #sys.stdout.write(question)
    userinput = input("> ").lower().strip()
    choice = userinput.split()
    objectforsurroundings = ''.join(set(choice).intersection(surroundings))
    commandfordirection = ''.join(set(choice).intersection(direction))
    # if no command
    if userinput == '':
        action_seq()
    # help
    elif any(elem in choice for elem in search_valid):
        current_action.append("help")
        if any(elem in choice for elem in add_inventory) or "pick" and "up" in choice:
            print4 ("To pick up an object, you can say 'add', 'pickup', 'pick up', 'take', or 'get'. For example, say 'pick up the lockpick' to pick up the lockpick.")
        elif any(elem in choice for elem in remove_inventory):
            print4 ("To drop an object, just say 'drop' or 'remove'. You don't need to specify the object, as you can only carry one thing at a time.")
        elif any(elem in choice for elem in travel):
            print4 ("To go in a specific direction, say 'go', 'move', or 'travel' followed by a direction. You can also travel to a specific thing, so you can say 'go sw', 'go southwest', or 'go through the door'.")
        elif "open" in choice:
            print4 ("To open a door, just say 'open the door'. If you are unable to open the door, it might be because it is locked.")
        elif any(elem in choice for elem in door_close):
            print4 ("To close a door, you can say 'close', 'shut', or 'slam'. For example, say 'shut the door' to shut the door.")
        elif any(elem in choice for elem in door_smash):
            print4 ("To smash a door open, you can say 'smash', 'bash', 'destroy', or 'break'. For example, say 'smash the door open' to smash the door open. However, keep in mind that you need a sledgehammer to smash something, so make sure you've picked one up or mention it in your command, like 'smash the door open with the sledgehammer'.")
        elif any(elem in choice for elem in door_unlock):
            print4 ("To unlock a door, say 'unlock' or 'pick'. For example, say 'pick the lock' to unlock a door. Keep in mind that you need a lockpick to unlock something, so make sure you've picked one up or mention it in your command, like 'unlock the door with the lockpick'.")
        elif "lock" in choice:
            print4 ("To lock a door, just say 'lock the door'. Keep in mind that if you lock an open door and then shut it, you will have to unlock it to open it again. You also need a lockpick to lock something, so make sure you've picked one up or mention it in your command, like 'lock the door with the lockpick'.")
        else:
            print4 ("You can pick up or drop an object, smash or pick locks, open or shut doors, and move. For a specific list of commands, type 'help [subset]', like 'help pick up'.")
    # pick up item
    elif any(elem in choice for elem in add_inventory) or "pick" and "up" in choice:
        current_action.append("pickup")
        if objectforsurroundings != '' and len(inventory) == 0:
            inventory.append(objectforsurroundings)
            surroundings.remove(objectforsurroundings)
            print4 ("I've picked up a " + objectforsurroundings + ".")
        elif objectforsurroundings != '' and len(inventory) != 0:
            print4 ("I'm already holding the " + ''.join(inventory) + ".")
        else:
            print4 ("Sorry, I can't find anything like that around here.")
    # drop item
    elif any(elem in choice for elem in remove_inventory):
        current_action.append("drop")
        if len(inventory) == 0:
            print4 ("I'm not holding anything.")
        elif len(inventory) != 0:
            print4 ("I've dropped the " + ''.join(inventory) + ".")
            surroundings.append(''.join(inventory))
            inventory.clear()
        else:
            print4 ("Sorry, I'm not holding that right now.")
    # go in a direction
    elif any(elem in choice for elem in travel):
        current_action.append("move")
        if commandfordirection != '':
            return commandfordirection
        elif "door" in choice:
            return "door"
        elif all(elem in choice for elem in travel):
            print4 ("Whoops! You forgot to tell me which way to go!")
            next_room_sledge()
        else:
            print4 ("I don't understand. Please say something like 'go northeast' instead.")
            next_room_sledge()
    # unlock door
    elif any(elem in choice for elem in door_unlock):
        current_action.append("unlock")
        if any(elem in surroundings for elem in unlocked_door):
            print4 ("The door is already unlocked.")
        elif "smashed door" in surroundings:
            print4 ("The door is already broken open.")
        elif any(elem in surroundings for elem in locked_door):
            if "lockpick" in inventory:
                unlock_door_cmd()
            elif any(elem in choice for elem in ["lock", "door"]) and "lockpick" in choice:
                if "lockpick" in surroundings:
                    unlock_door_cmd()
                else:
                    print4 ("I can't see a lockpick anywhere near me.")
            elif "lockpick" not in inventory:
                print4 ("I don't have anything to pick the lock with.")
            else:
                print4 ("I don't understand.")
    # lock door
    elif "lock" in choice:
        current_action.append("lock")
        if any(elem in surroundings for elem in locked_door):
            print4 ("The door is already locked.")
        elif "smashed door" in surroundings:
            print4 ("The door is broken open.")
        elif any(elem in surroundings for elem in unlocked_door):
            if "lockpick" in inventory:
                lock_door_cmd()
            elif any(elem in choice for elem in ["lock", "door"]) and "lockpick" in choice:
                if "lockpick" in surroundings:
                    lock_door_cmd()
                else:
                    print4 ("I can't see a lockpick anywhere near me.")
            elif "lockpick" not in inventory:
                print4 ("I don't have anything to pick the lock with.")
            else:
                print4 ("I don't understand.")
        else:
            print4 ("[[[FUCK]]]")
    # open door
    elif "open" in choice:
        current_action.append("open")
        if any(elem in surroundings for elem in open_door):
            print4 ("The door is already open.")
        elif "smashed door" in surroundings:
            print4 ("The door is already broken open.")
        elif "locked closed door" in surroundings:
            print4 ("The door is locked.")
        elif "unlocked closed door" in surroundings:
            if len(inventory) == 0:
                surroundings.append("unlocked open door")
                surroundings.remove("unlocked closed door")
                print4 ("I've opened the door.")
            else:
                print4 ("I can't open the door while I'm holding something.")
        else:
            print4 ("Sorry, I can't see a door anywhere around here.")
    # close door
    elif any(elem in choice for elem in door_close):
        current_action.append("close")
        if any(elem in surroundings for elem in closed_door):
            print4 ("The door is already shut.")
        elif "smashed door" in surroundings:
            print4 ("I can't close a broken door.")
        elif len(inventory) == 0 and "locked open door" in surroundings:
            surroundings.append("locked closed door")
            surroundings.remove("locked open door")
            print4 ("I've closed the door.")
        elif len(inventory) == 0 and "unlocked open door" in surroundings:
            surroundings.append("unlocked closed door")
            surroundings.remove("unlocked open door")
            print4 ("I've closed the door.")
        elif len(inventory) != 0 and any(elem in surroundings for elem in open_door):
            print4 ("I can't shut the door while I'm holding something.")
        else:
            print4 ("Sorry, I can't see a door anywhere around here.")
    # smash door
    elif any(elem in choice for elem in door_smash):
        current_action.append("smash")
        if "smashed door" in surroundings:
            print4 ("The door is already broken open.")
        elif "sledgehammer" not in inventory and "sledgehammer" not in choice:
            print4 ("I don't have anything to smash the door with.")
        elif any(elem in surroundings for elem in smashable_door):
            if "sledgehammer" in inventory:
                smash_door_cmd()
            elif "sledgehammer" in choice:
                if "sledgehammer" in surroundings:
                    smash_door_cmd()
                else:
                    print4 ("I can't see a sledgehammer anywhere near me.")
            else:
                print4 ("For some really weird reason I can't smash the door. Sorry.")
        else:
            print4 ("Sorry, I can't see a door anywhere around here.")
    # no command
    else:
        print4 ("I don't understand.")

# used to ask the player name
def player_name(question):
    idk_name = ["idk", "i dont know"]
    not_telling_name = ["no", "n", "nope", "nah", "false", "not telling"]

    inputname.clear()
    sys.stdout.write(question)
    playernameinput = input().strip()
    if playernameinput in not_telling_name:
        print2 ("Oh. Ok. That's fine.")
        enter()
        pt_5()
    elif playernameinput in idk_name:
        print2 ("I don't know who I am either.")
        enter()
        pt_5()
    elif playernameinput == '':
        player_name(question)
    elif playernameinput in search_valid:
        sys.stdout.write("\n"
                         "> You can say 'idk' and 'i dont know', or 'no', 'n', 'nope', 'nah', 'false', and 'not telling', or you can state your name.\n"
                         "> What would you like to say?\n"
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
            print4 ("> Please enter your name. 'no' and 'idk' are both valid answers")
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
    print ("> Disconnecting in 3...")
    print2 ("> Press enter to continue or 'stop' to cancel disconnection")
    answer = stopgo_query("> ", "yes")
    if answer:
        clear_screen()
        print1 ("> ...2...")
        answer = stopgo_query("> ", "yes")
        if answer:
            clear_screen()
            print1 ("> ...1...")
            answer = stopgo_query("> ", "yes")
            if answer:
                clear_screen()
                print1 ("> Connection lost.")
                game_over()
            if not answer:
                print2 ("> Connection corrupted. Unable to restore.")
                game_over()
        if not answer:
            print2 ("> Connection corrupted. Attempt to restore?")
            answer = yn_query("> ")
            if answer:
                clear_screen()
                print1 ("> Attempting to restore connection...")
                enter()
                clear_screen()
                number = random.randint(0,9)
                if number >= 5:
                    print1 ("> Attempt failed. Connection lost.")
                    game_over()
                else:
                    print1 ("> Attempt successful. Connection restored.")
                    enter()
                    print ("Oh, you're back.")
                    disconnecting= False
            if not answer:
                game_over()
    if not answer:
        print2 ("> Connection restored.")
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
    print2 ("H̸̡̢̬̯̖̲͚̝̪̦͎̣͖̜̒̄̈́͑̕͝ͅē̸̘̞̼̞͉͖͐́̓̀͑̈͒̈͆͗̚l̵̛͎͕͂͛̐̽͗̄̕̕̚l̸̰̫̼̙̠͙͋͋̀̍̀͐̓̈́̑͑̅o̶͕̦̲̍͌͛̀̍̒̈̑͌̽̕͘͘͝͝.")

    print ()
    print ()
    enter()
    print2 ("Ḧ̸̡̟́͜͝ę̵̧̈́͌̆ļ̸̤̻͝l̶̖͘͝o̸͖̬̊͆̊.")
    enter()
    print2 ("H̶̘̎e̵̬̋l̶̮̅l̵͇͌ò̶̲.")
    enter()
    print1 ("H̸ello.")
    enter()
    print1 ("Hello.")
    enter()
    pt_3()

# can you hear me? [y/n]
def pt_3():
    print1 ("Can you hear me?")
    answer = yn_query("> ")
    if answer:
        print2 ("You can hear me!")
        enter()
        pt_4()
    if not answer:
        print2 ("Wait. You can hear me, or you wouldn't have answered!")
        enter()
        pt_4()

# who are you? [name]
def pt_4():
    print1 ("No one's been able to hear me before.")
    enter()
    print1 ("Who are you?")
    print ("> Please enter your name. 'no' and 'idk' are both valid answers.")
    player_name("> ")

# can you help me find out who I am? [y/n]
def pt_5():
    print1 ("Can you help me find out who I am?")
    answer = yn_query("> ")
    if answer:
        print4 ("Ok then! Let's do this.")
        rm_1_closed_door_a()
    if not answer:
        print2 ("Oh. Ok. Goodbye.")
        enter ()
        disconnected = disconnecting()
        if not disconnected:
            print ()
            pt_5()
        if disconnected:
            game_over()

# open world room 1
def next_room_sledge():
    if len(inventory) != 0:
        holding = " holding a " + ''.join(inventory)
    else:
        holding = ''
    if "locked closed door" in surroundings:
        door_status = " locked door"
    elif "unlocked closed door" in surroundings:
        door_status = " closed door"
    elif any(elem in surroundings for elem in open_door):
        door_status = "n open door"
    elif "smashed door" in surroundings:
        door_status = " broken door"
    if "sledgehammer" in surroundings and "lockpick" in surroundings:
        near_me = " and a sledgehammer and a lockpick near me"
    elif "sledgehammer" in surroundings:
        near_me = " and a sledgehammer near me"
    elif "lockpick" in surroundings:
        near_me = " and a lockpick near me"
    else:
        near_me = ''
    print ("I'm" + holding + " in a room with a" + door_status + " to the north" + near_me + ".")
    print1 ("What should I do?")
    answer_action = action_seq()
    if "move" in current_action:
        current_action.clear()
        if any(elem in answer_action for elem in north) and any(elem in surroundings for elem in closed_door):
            print4 ("I can't go through a closed door.")
            next_room_sledge()
        elif any(elem in answer_action for elem in north) and any(elem in surroundings for elem in walkable_door):
            print2 ("Moving north.")
            enter()
            rm_2()
            print (answer_action)
        elif "door" in answer_action and any(elem in surroundings for elem in walkable_door):
            print2 ("Going through the door.")
            enter()
            rm_2()
        elif "door" in answer_action and any(elem in surroundings for elem in closed_door):
            print4 ("I can't go through a closed door.")
            next_room_sledge()
        else:
            print4 ("There's a wall there. I can't go that way.")
            next_room_sledge()
    elif any(elem in current_action for elem in ["pickup", "drop", "lock", "unlock", "open", "close", "smash", "help"]):
        current_action.clear()
        next_room_sledge()
    else:
        print4 ("[[[INVALID ACTION]]]")

# open world room 1
def rm_1_closed_door_a():
    inventory.clear()
    surroundings.clear()
    surroundings.append("sledgehammer")
    surroundings.append("lockpick")
    surroundings.append("locked closed door")
    next_room_sledge()

# scripted room 2
def rm_2():
    playernameused = makes_name().lower().strip()
    current_action.clear()
    surroundings.clear()
    print ("Hey look! I see a piece of paper.")
    print1 ("I'm gonna pick it up.")
    enter()
    print1 ("It says: 'Your name is Alexa.'")
    enter()
    print1 (">>Hey Alexa! Play generic pop song #37!<<")
    print1 ("I gotta go. Thanks for helping!")
    print1 (">>HEY ALEXA!<<")
    if playernameused == '':
        print1 ("okireallygottagothanksagainbye")
    else:
        print1 ("okireallygottagothanksagain" + playernameused + "bye")
    game_over()

pt_1()
#rm_1_closed_door_a()