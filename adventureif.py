import os
import getpass
import sys
import random

north      = ["n", "north"]
north_west = ["nw", "northwest", "north-west"]
west       = ["w", "west"]
south_west = ["sw", "southwest", "south-west"]
south      = ["s", "south"]
south_east = ["se", "southeast", "south-east"]
east       = ["e", "east"]
north_east = ["ne", "northeast", "north-east"]
direction  = ["n", "north", "nw", "northwest", "north-west", "w", "west", "sw", "southwest", "south-west", "s", "south", "se", "southeast", "south-east", "e", "east", "ne", "northeast", "north-east"]

inputname = [] # basket for player name
surroundings = [] # basket for possible objects to pick up and doors
surroundingsrm1 = [] # basket for room 1 surroundings
inventory = [] # basket for inventory
broken_things = [] # basket for things that need fixing
current_action = [] # basket for current action (eg move, lock, pickup)

commands = ["add", "pickup", "take", "get",
            "drop", "remove",
            "go", "move", "travel", "proceed", "relocate",
            "open",
            "close", "shut", "lock", "slam",
            "smash", "bash", "destroy", "break"]
add_inventory = ["add", "pickup", "pick up", "take", "get", "grab"]
remove_inventory = ["drop", "remove"]
travel = ["go", "move", "travel", "proceed", "relocate", "walk", "run", "step", "jog", "sprint"]
door_open = "open"
door_close = ["close", "shut", "slam"]
door_lock = "lock"
door_unlock = ["unlock", "pick"]
smash_cmd = ["smash", "bash", "destroy", "break"]
hide_cmd = "hide"
sleep_cmd = ["sleep", "nap"]
dodge_cmd = ["dodge", "avoid", "evade", "elude", "escape", "sidestep", "duck"]
fight_cmd = ["fight", "hit", "kick", "punch", "slap", "smack", "swat", "strike", "whallop", "slug"]
unhelpful_cmd = ["nothing", "cry"]
leave_cmd = ["leave", "depart", "escape", "exit", "scram"]
knock_cmd = ["knock", "bang", "pound", "tap"]

walkable_door = ["open door", "smashed door"]
smashable_door = ["closed door", "open door"]
smashable_lock = ["locked lock", "unlocked lock"]

# triggers help
search_valid = ["idk", "i dont know", "i don't know", "dont know", "don't know", "options", "search", "choices", "help", "how", "what should"]

# prints with a line before and after
def print2(text):
    print('\n' + text + '\n')

# prints with a line after
def print1(text):
    print(text + '\n')

# prints with a line before
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
    valid = {"yes": True, "y": True, "ye": True, "yea": True, "yeah": True, "yep": True, "yup": True, "sure": True, "ok": True, "fine": True, "of course": True, "ofc": True, "true": True,
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
                             "> You can say 'yes', 'y', 'ye', 'yea', 'yeah', 'yep', 'yup', 'sure', 'ok', 'fine', 'of course', 'ofc', and 'true', or "
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
    valid = {"yes": True, "y": True, "ye": True, "yea": True, "yeah": True, "yep": True, "yup": True, "sure": True, "ok": True, "fine": True, "of course": True, "ofc": True, "true": True, "keep going": True, "proceed": True, "start": True, "go": True, "continue": True, "begin": True, "on": True,
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
    surroundings.remove("locked lock")
    surroundings.append("unlocked lock")
    print4 ("I've unlocked the door.")

def lock_door_cmd():
    surroundings.remove("unlocked lock")
    surroundings.append("locked lock")
    print4 ("I've locked the door.")

def smash_door_cmd():
    if "closed door" in surroundings:
        surroundings.remove("closed door")
    elif "locked door" in surroundings:
        surroundings.remove("locked door")
    elif "open door" in surroundings:
        surroundings.remove("open door")
    if "locked lock" in surroundings:
        surroundings.remove("locked lock")
    elif "unlocked lock" in surroundings:
        surroundings.remove("unlocked lock")
    if "smashed lock" in surroundings:
        surroundings.remove("smashed lock")
    surroundings.append("smashed door")
    print4 ("I've smashed the door.")

def smash_lock_cmd():
    if "locked lock" in surroundings:
        surroundings.remove("locked lock")
    elif "unlocked lock" in surroundings:
        surroundings.remove("unlocked lock")
    surroundings.append("smashed lock")
    print4 ("I've smashed the lock.")

# used in open world rooms
def action_seq():
    current_action.clear()
    userinput = input("> ").strip().strip("'").strip("?").strip("!").strip(".").strip(",")
    choice = userinput.split()

    listforsurroundings = set(choice).intersection(surroundings)
    objectforsurroundings = ''.join(set(choice).intersection(surroundings))
    commandfordirection = ''.join(set(choice).intersection(direction))
    fightcommandtype = ''.join(set(choice).intersection(fight_cmd)).capitalize()

    # door status
    if "closed door" in surroundings and "locked lock" in surroundings:
        door_status = " locked door"
    elif "closed door" in surroundings:
        door_status = " closed door"
    elif "open door" in surroundings:
        door_status = "n open door"
    elif "smashed door" in surroundings:
        door_status = " broken door"
    else:
        door_status = " doorframe"

    # if no command
    if userinput == '':
        print2 ("Whoops! You forgot to tell me what to do. If you don't know what to do, just type 'help'.")
        action_seq()
    # help
    elif any(elem in choice for elem in search_valid):
        current_action.append("help")
        if any(elem in choice for elem in add_inventory) or "pick" and "up" in choice:
            print4 ("To pick up an object, you can say 'add', 'pickup', 'pick up', 'take', 'grab', or 'get'. For example, say 'pick up the lockpick' to have me pick up the lockpick.")
        elif any(elem in choice for elem in remove_inventory):
            print4 ("To drop an object, you can say 'drop' or 'remove'. You don't need to specify the object, as I can only carry one thing at a time.")
        elif any(elem in choice for elem in travel):
            print4 ("To have me travel in a specific direction, you can say 'go', 'move', 'travel', 'proceed', 'relocate', 'walk', 'run', 'step', 'jog', or 'sprint', followed by a direction. I can also travel to a specific thing, so you can say 'go sw', 'go southwest', or 'go through the door'. To see a list of valid directions, type 'help directions'.")
        elif "directions" in choice:
            print4 ("I can go in any of the eight major compass points: north (or n), east (e), west (w), south (s), northeast (ne, north-east), northwest (nw, north-west), southeast (se, south-east), or southwest (sw, south-west).")
        elif "open" in choice:
            print4 ("To have me open a door, just say 'open the door'. If I can't open the door, it might be because it is locked.")
        elif any(elem in choice for elem in door_close):
            print4 ("To have me close a door, you can say 'close', 'shut', or 'slam'. For example, say 'shut the door' to have me shut the door.")
        elif any(elem in choice for elem in smash_cmd):
            print4 ("To have me smash something, you can say 'smash', 'bash', 'destroy', or 'break'. For example, say 'smash the door open' to have me smash the door open. However, keep in mind that I need a sledgehammer to smash something, so make sure I've picked one up or mention it in your command, like 'smash the door open with the sledgehammer'.")
        elif any(elem in choice for elem in door_unlock):
            print4 ("To have me unlock a door, you can say 'unlock' or 'pick'. For example, say 'pick the lock' to have me unlock a door. Keep in mind that I need a lockpick to unlock something, so make sure I've picked one up or mention it in your command, like 'unlock the door with the lockpick'.")
        elif "lock" in choice:
            print4 ("To have me lock a door, just say 'lock the door', or 'lock the lock'. Keep in mind that if I lock an open door and then shut it, I will have to unlock it to open it again. I also need a lockpick to lock something, so make sure I've picked one up or mention it in your command, like 'lock the lock with the lockpick'.")
        elif "sleep" in choice:
            print4 ("To have me go to sleep, just say 'sleep'. However, I am a very deep sleeper, so keep in mind that I might not wake up when messaged.")
        elif "hide" in choice:
            print4 ("To have me hide, just say 'hide' and I can tell you if I see anything to hide behind. If I only see one thing, I'll hide straightaway, but if I don't see anything or I see more than one thing to hide behind, I'll ask you what to do next.")
        elif any(elem in choice for elem in dodge_cmd):
            print4 ("To have me dodge something, you can say 'dodge', 'avoid', 'evade', 'elude', 'escape', 'sidestep', or 'duck'. I'll dodge immediately.")
        elif any(elem in choice for elem in fight_cmd):
            print4 ("To have me fight something, you can say 'fight', 'hit', 'kick', 'punch', 'slap', 'smack', 'swat', 'strike', 'whallop', or 'slug'. If there's more than one enemy, I'll either ask you which one to hit, or just hit the most important one first.")
        else:
            print4 ("I can pick up or drop an object, smash or pick locks, doors, and walls, open or shut doors, sleep, hide, fight, dodge, and move. For a specific list of commands, type 'help [subset]', like 'help pick up'.")
    # pick up item
    elif any(elem in choice for elem in add_inventory) or "pick" and "up" in choice:
        current_action.append("pickup")
        if len(listforsurroundings) >= 2:
            print4 ("I can't hold two things at once.")
        elif all(elem in ["pick", "up"] for elem in choice):
            print4 ("What should I pick up?")
        elif all(elem in add_inventory for elem in choice):
            print4 ("What should I pick up?")
        elif 'door' in choice:
            if 'smashed door' in surroundings and len(inventory) == 0:
                inventory.append(str("door"))
                surroundings.remove(str("smashed door"))
                print4 ("I've picked up a door.")
            elif 'door' in inventory and len(inventory) != 0:
                print4 ("I'm already holding the door.")
            elif 'dropped door' in surroundings:
                inventory.append(str("door"))
                surroundings.remove(str("dropped door"))
                print4 ("I've picked up a door.")
            elif 'smashed door' not in surroundings and 'door' not in inventory:
                print4 ("I can't pick up a" + door_status +".")
            else:
                print4 ("Sorry, I can't find anything like that around here.")
        else:
            if objectforsurroundings != '' and len(inventory) == 0:
                inventory.append(str(objectforsurroundings))
                surroundings.remove(str(objectforsurroundings))
                print4 ("I've picked up a " + str(objectforsurroundings) + ".")
            elif objectforsurroundings != '' and len(inventory) != 0:
                print4 ("I'm already holding the " + ''.join(inventory) + ".")
            else:
                print4 ("Sorry, I can't find anything like that around here.")
    # drop item
    elif any(elem in choice for elem in remove_inventory) or "put" and "down" in choice:
        current_action.append("drop")
        if len(inventory) == 0:
            print4 ("I'm not holding anything.")
        elif "door" in inventory:
            print4 ("I've dropped the " + ''.join(inventory) + ".")
            surroundings.append("dropped door")
            inventory.clear()
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
    # leave
    elif any(elem in choice for elem in leave_cmd):
        current_action.append("leave")
    # knock
    elif any(elem in choice for elem in knock_cmd):
        current_action.append("knock")
        if "wall" in choice:
            print4 ("The wall seems...well, like a wall. It sounds like a wall. Fairly solid. Why did you want me to knock on the wall again?")
        elif "floor" in choice:
            print4 ("Nothing happened. It's a floor. Don't know what you expected.")
        else:
            print4 ("I knocked on the door. Nothing happened.")
    # smash
    elif any(elem in choice for elem in smash_cmd):
        current_action.append("smash")
        if "lock" in choice:
            if "smashed lock" in surroundings:
                print4 ("The lock is already broken open.")
            if "smashed door" in surroundings:
                print4 ("The door is already broken open.")
            elif "sledgehammer" not in inventory and "sledgehammer" not in choice:
                print4 ("I don't have anything to smash the lock with.")
            elif any(elem in surroundings for elem in smashable_lock):
                if "sledgehammer" in inventory:
                    smash_lock_cmd()
                elif "sledgehammer" in choice:
                    if "sledgehammer" in surroundings:
                        smash_lock_cmd()
                    else:
                        print4 ("I can't see a sledgehammer anywhere near me.")
                else:
                    print4 ("For some really weird reason I can't smash the lock. Sorry.")
            else:
                print4 ("Sorry, I can't see a lock anywhere around here.")
        elif "wall" in choice:
            if "sledgehammer" not in inventory and "sledgehammer" not in choice:
                print4 ("I don't have anything to smash the wall with.")
            else:
                if any(elem in choice for elem in north):
                    surroundings.append("north wall hole")
                    print4 ("I smashed a hole in the wall. It looks big enough to easily walk through.")
                elif any(elem in choice for elem in east) or any(elem in choice for elem in west) or any(elem in choice for elem in south):
                    print ()
                    def smash_loop():
                        print ("> Time passes, the seconds punctuated with discordant and heavy thuds.")
                        print2 ("I don't think I'm getting anywhere. Should I keep going?")
                        cont_answer = yn_query("> ")
                        print()
                        enter()
                        if cont_answer:
                            smash_loop()
                        else:
                            print4 ("Alright. What should I try instead?")
                            next_room_sledge()
                    smash_loop()
                else:
                    print4 ("I don't know which wall to smash.")
        elif "smashed door" in surroundings:
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
    # unlock door
    elif any(elem in choice for elem in door_unlock):
        current_action.append("unlock")
        if "unlocked lock" in surroundings:
            print4 ("The door is already unlocked.")
        elif "smashed door" in surroundings:
            print4 ("The door is already broken open.")
        elif "smashed lock" in surroundings:
            print4 ("The lock is already broken open.")
        elif "locked lock" in surroundings:
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
        if "unlocked lock" in surroundings:
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
        elif "locked lock":
            print4 ("The door is already locked.")
        elif "smashed door" in surroundings:
            print4 ("The door is broken open.")
        elif "smashed lock" in surroundings:
            print4 ("The lock is broken open.")
    # open door
    elif "open" in choice:
        current_action.append("open")
        if "open door" in surroundings:
            print4 ("The door is already open.")
        elif "smashed door" in surroundings:
            print4 ("The door is already broken open.")
        elif "closed door" in surroundings:
            if "locked lock" in surroundings:
                print4 ("The door is locked.")
            elif "unlocked lock" in surroundings or "smashed lock" in surroundings:
                if len(inventory) == 0:
                    surroundings.append("open door")
                    surroundings.remove("closed door")
                    print4 ("I've opened the door.")
                else:
                    print4 ("I can't open the door while I'm holding something.")
        else:
            print4 ("Sorry, I can't see a door anywhere around here.")
    # close door
    elif any(elem in choice for elem in door_close):
        current_action.append("close")
        if "closed door" in surroundings:
            print4 ("The door is already shut.")
        elif "smashed door" in surroundings:
            print4 ("The door is broken open.")
        elif len(inventory) == 0 and "open door" in surroundings:
            surroundings.append("closed door")
            surroundings.remove("open door")
            print4 ("I've closed the door.")
        elif len(inventory) != 0 and "open door" in surroundings:
            print4 ("I can't shut the door while I'm holding something.")
        else:
            print4 ("Sorry, I can't see a door anywhere around here.")
    # hide
    elif "hide" in choice:
        current_action.append("hide")
        if "open door" in surroundings or "smashed door" in surroundings:
            return "hide"
        else:
            print4 ("I can't see anything to hide behind.")
    # sleep
    elif any(elem in choice for elem in sleep_cmd):
        current_action.append("sleep")
        print2 ("That seems like a good idea. Goodnight!")
        def sleeploop():
            enter()
            sleepnumber = random.randint(0,9)
            print1 ("Time passes.")
            print1 ("What would you like to say?")
            input("> ")
            print2 ("There is no response, but you can hear faint snoring in the background.")
            if sleepnumber >= 5:
                sleeploop()
            else:
                print1 ("Error. Connection timed out.")
                game_over()
        sleeploop()
    # dodge
    elif any(elem in choice for elem in dodge_cmd):
        print4 ("> You hear a sudden rustling amid a burst of static")
        print4 ("There's nothing there! You scared me, making me dodge nothing for no reason!")
    # fight
    elif any(elem in choice for elem in fight_cmd):
        print4 (fightcommandtype + " what? There's nothing there!")
    elif any(elem in choice for elem in unhelpful_cmd):
        print2 ("Wow. You're sooooo helpful. Wanna try again?")
        helpful = yn_query("> ")
        if helpful:
            print2 ("Cool. Let's get to it.")
        elif not helpful:
            print2 ("Alright. You're clearly not going to be any help. Bye.")
            game_over()
    # [[[REMOVE]]] bypass to room 2
    elif "bypasscmdrm2" in choice:
        rm_2()
    elif "alexa" in choice:
        print4 ("Yes? What do you want me to do?")
    elif "siri" in choice:
        print4 ("I'm not Siri. We are friends though. What do you want me to do?")
    # no command
    else:
        print4 ("I don't understand. If you're having trouble, type 'help' to see what you can tell me to do.")

# used to ask the player name
def player_name(question):
    idk_name = ["idk", "i dont know"]
    not_telling_name = ["no", "n", "nope", "nah", "false", "not telling"]

    inputname.clear()
    sys.stdout.write(question)
    playernameinput = input().strip().capitalize()
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
    player_name("> My name is ")

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

# open world room 1 play
def next_room_sledge():
    if len(inventory) != 0:
        holding = " holding a " + ''.join(inventory)
    else:
        holding = ''

    if "closed door" in surroundings and "locked lock" in surroundings:
        door_status = " locked door"
    elif "closed door" in surroundings:
        door_status = " closed door"
    elif "open door" in surroundings:
        door_status = "n open door"
    elif "smashed door" in surroundings:
        door_status = " broken door"
    else:
        door_status = "n empty doorframe"

    potential_near_me = ["sledgehammer", "lockpick", "dropped door"]
    near_me = set(surroundings).intersection(potential_near_me)

    if len(near_me) == 3:
        p2 = ","
        p3 = ", and"
    elif 'sledgehammer' not in surroundings and len(near_me) == 2:
        p2 = ''
        p3 = " and"
    elif len(near_me) == 2:
        p2 = " and"
        p3 = ''
    elif len(near_me) <= 1:
        p2 = ''
        p3 = ''

    if len(potential_near_me) != 0:
        p1 = " and"
        p4 = " near me"
    else:
        p1 = ''
        p2 = ''

    if "sledgehammer" in surroundings:
        sledge_nearby = " a sledgehammer"
    else:
        sledge_nearby = ''
    if "lockpick" in surroundings:
        lock_nearby = " a lockpick"
    else:
        lock_nearby = ''
    if "dropped door" in surroundings:
        door_nearby = " a door"
    else:
        door_nearby = ''

    if "north wall hole" in surroundings:
        hole_status = " and a hole in the wall"
    else:
        hole_status = ''

    print (surroundings)
    print (inventory)
    print ("I'm" + holding + " in a room with a" + door_status + hole_status + " to the north" + p1 + sledge_nearby + p2 + lock_nearby + p3 + door_nearby + p4 +".")
    print1 ("What should I do?")
    answer_action = action_seq()
    # move
    if "move" in current_action:
        current_action.clear()
        if any(elem in answer_action for elem in north_east) or any(elem in answer_action for elem in north_west):
            print4 ("There's a wall there. I can't go that way.")
            next_room_sledge()
        elif any(elem in answer_action for elem in north) and "closed door" in surroundings:
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
        elif "door" in answer_action and "closed door" in surroundings:
            print4 ("I can't go through a closed door.")
            next_room_sledge()
        else:
            print4 ("There's a wall there. I can't go that way.")
            next_room_sledge()
    # hide
    elif "hide" in current_action:
        def hide_query():
            answer = yn_query("> ")
            if answer:
                print2("Ok. I don't really see the point, but ok.")
                enter()
                def keep_hiding():
                    hidenumber = random.randint(0,9)
                    print ("> Time passes.")
                    print2 ("Should I keep hiding?")
                    cont_answer = yn_query("> ")
                    print()
                    enter()
                    if cont_answer:
                        if hidenumber >= 3:
                            keep_hiding()
                        else:
                            print1 ("> Error. Connection timed out.")
                            game_over()
                    else:
                        print4 ("Alright. I'm stepping out from behind the door now.")
                        next_room_sledge()
                keep_hiding()
            else:
                print4 ("Alright. I'm stepping out from behind the door now.")
                next_room_sledge()
        if "open door" in surroundings:
            print2 ("I'm hiding behind the door, but I don't feel like I'm hidden very well. Should I keep hiding?")
            hide_query()
        elif "smashed door" in surroundings:
            print2 ("I'm hiding under the broken door, and I feel like I'm hidden fairly well. Should I keep hiding?")
            hide_query()
        else:
            current_action.clear()
            next_room_sledge()
    elif "leave" in current_action:
        if "north wall hole" in surroundings:
            print4 ("The only exit I see is through the" + door_status + " or the hole in the wall to the north.")
        else:
            print4 ("The only exit I see is through the" + door_status + " to the north.")
        next_room_sledge()
    else:
        current_action.clear()
        next_room_sledge()

# open world room 1 setup
def rm_1_closed_door_a():
    inventory.clear()
    surroundings.clear()
    surroundings.append("sledgehammer")
    surroundings.append("lockpick")
    surroundings.append("closed door")
    surroundings.append("locked lock")
    next_room_sledge()

# scripted room 2
def rm_2():
    surroundingsrm1.extend(surroundings)
    #print (surroundingsrm1)
    playernameused = makes_name().lower().strip().replace(' ', '')
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

#pt_1()
rm_1_closed_door_a()