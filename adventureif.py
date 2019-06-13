import os
import getpass
import sys
import random
import re
import copy
import adventureif

stripattern = re.compile('([^\s\w]|_)+') # strip all non alphanumeric characters that are not spaces

north      = ["n", "north"]
north_west = ["nw", "northwest", "north-west"]
west       = ["w", "west"]
south_west = ["sw", "southwest", "south-west"]
south      = ["s", "south"]
south_east = ["se", "southeast", "south-east"]
east       = ["e", "east"]
north_east = ["ne", "northeast", "north-east"]
direction  = ["n", "north", "nw", "northwest", "north-west", "w", "west", "sw", "southwest", "south-west", "s", "south", "se", "southeast", "south-east", "e", "east", "ne", "northeast", "north-east"]
false_direction = ["forward", "back", "up", "down", "sideways", "left", "right", "away"]

class Player:
    def __init__(self, name, inventory, health, status, hunger, thirst):
        self.health = health # immune, healthy, standard, weak, sick, ill, delirious, dead
        self.status = status # strong, healthy, standard, hurt, injured, mauled, unconscious, dead
        self.hunger = hunger # full, satisfied, standard, hungry, ravenous, malnourished, starving, dead
        self.thirst = thirst # hydrated, sated, standard, thirsty, parched, dehydrated, dying, dead
        self.name = name
        self.inventory = inventory

class DoorState:
    def __init__(self, breakable, doortype, status, lockstatus, room_list):
        self.doortype = doortype # breakable, wall, stair
        self.status = status # open, closed, smashed, doorframe, hidden, revealed, blocked
        self.lockstatus = lockstatus # locked, unlocked, smashed, blocked
        self.room_list = room_list

class RoomState:
    def __init__(self, description, content, major_door, door_list):
        self.description = description
        self.content = content
        self.major_door = major_door
        self.door_list = door_list

player = Player('', [], "standard", "standard", "standard", "standard" )

door = {
    0: DoorState("breakable", "wooden door", "closed", "locked", [0, 1]),
    1: DoorState("breakable", "wall", "hidden", "blocked", [0, 1]),
    2: DoorState("unbreakable", "stairs", "hidden", "blocked", [1, 2])
}

room = {
    0: RoomState("starting room", ["sledgehammer", "lockpick"], 0, [0, 1]),
    1: RoomState("staircase room", ["lever"], 0, [0, 1, 2]),
    2: RoomState("empty", [], None, 2)
}

current_action = [] # basket for current action (eg move, lock, pickup)
current_room = []

travel = ["go", "move", "travel", "proceed", "relocate", "advance", "walk", "run", "step", "jog", "sprint", "ascend", "descend", "climb", "crawl", "sneak"]
door_unlock = ["unlock", "pick", "unlatch", "unbolt"]
door_close = ["close", "shut", "slam"]
door_open = "open" # unused
door_lock = ["lock", "latch", "bolt"]
hide_cmds = ["hide", "shelter", "conceal"]
smash_cmd = ["smash", "bash", "destroy", "break"]
sleep_cmd = ["sleep", "nap"]
dodge_cmd = ["dodge", "avoid", "evade", "elude", "escape", "sidestep", "duck"]
fight_cmd = ["fight", "hit", "kick", "punch", "slap", "smack", "swat", "strike", "whallop", "slug", "hurt"]
leave_cmd = ["leave", "depart", "escape", "exit", "scram"]
knock_cmd = ["knock", "bang", "pound", "tap"]
shout_cmd = ["shout", "yell", "scream", "challenge", "shriek", "screech", "squawk", "roar", "holler", "cheer", "clamor", "whoop", "wail"]
lever_cmd = ["push", "pull", "press", "poke", "shove", "move", "nudge", "shift", "break"]
jump_cmds = ["jump", "leap", "bounce", "vault", "bound", "hop", "hurdle", "jounce"]
greetings = ["hi", "hey", "hello", "sup", "greeting", "greet", "howdy", "good morning", "whats up", "how are", "how is"]
farewells = ["bye", "toodles", "farewell", "goodbye", "cheerio", "good day", "good night", "so long", "good luck", "got to go", "gtg", "g2g", "talk to you later", "ttyl", "be right back", "brb", "afk", "afc"]
stairssyn = ["stairs", "stair", "stairway", "staircase", "stairwell", "upstairs", "upstair", "downstairs", "downstair", "flight of stairs"]
add_inventory = ["add", "pickup", "pick up", "take", "get", "grab"]
rmv_inventory = ["drop", "remove", "put", "place"]
shout_cmd_past = ["shouted", "yelled", "screamed", "challenged", "shrieked", "squawked", "roared", "hollered", "cheered", "clamored", "whooped", "wailed"]
fight_cmd_past = ["fought", "hit", "kicked", "punched", "smacked", "swatted", "struck", "whalloped", "slugged", "hurt"]
knock_cmd_past = ["knocked", "banged", "pounded", "tapped"]
unhelpful_cmds = ["nothing", "cry"]
forcefully_cmd = ["forcefully", "force", "harder"]
chargeobj_cmds = ["charge", "rush", "bodyslam", "shoulder", "push"]

walkable_door = ["open", "smashed", "doorframe"]
door_in_frame = ["closed", "open", "smashed"]
smashable_door = ["closed", "open"]
smashable_lock = ["locked", "unlocked"]

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
    getpass.getpass("> Press enter to play ")
    clear_screen()

# press enter to play again
def enter_play_again():
    getpass.getpass("> Press enter to play again ")
    clear_screen()

# press enter to continue
def enter():
    getpass.getpass("> Press enter to continue ")
    clear_screen()

def player_death():
    player.health = "dead"
    player.status = "dead"
    player.hunger = "dead"
    player.thirst = "dead"

# used for yes/no questions
def yn_query(question, default=None):
    valid = {"yes": True, "y": True, "ye": True, "ya": True, "yea": True, "yeah": True, "yep": True, "yup": True, "sure": True, "ok": True, "fine": True, "of course": True, "ofc": True, "true": True,
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
        choiceraw = input().lower().strip()
        choice = stripattern.sub('', choiceraw)
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        elif choice in search_valid:
            sys.stdout.write("\n"
                             "> You can say 'yes', 'y', 'ye', 'ya', 'yea', 'yeah', 'yep', 'yup', 'sure', 'ok', 'fine', 'of course', 'ofc', and 'true', or "
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
    valid = {"yes": True, "y": True, "ye": True, "ya": True, "yea": True, "yeah": True, "yep": True, "yup": True, "sure": True, "ok": True, "fine": True, "of course": True, "ofc": True, "true": True, "keep going": True, "proceed": True, "start": True, "go": True, "continue": True, "begin": True, "on": True,
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
        choiceraw = input().lower().strip()
        choice = stripattern.sub('', choiceraw)
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        elif choice in search_valid:
            sys.stdout.write("\n"
                             "> You can say 'yes', 'y', 'ye', 'ya', 'yea', 'yeah', 'yep', 'yup', 'sure', 'ok', 'fine', 'true', 'keep going', 'proceed', 'start', 'go', 'continue', 'begin', and 'on' or "
                             "('no', 'n', 'nope', 'nah', 'not yet', 'retry', 'false', 'stop', 'halt', 'finish', 'end', 'stay', 'off', 'restore', and 'cancel'.\n"
                             "> What would you like to say?\n"
                             "\n")
        else:
            sys.stdout.write("> Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n'). Type 'help' to see more options\n")

# used to continue rm_interactive
def continuetorm():
    if "rm1" in current_room:
        rm_1_interactive()
    elif "rm2" in current_room:
        rm_2_interactive()

# used in open world rooms
def action_seq(surroundings, room_number, door_direction):
    current_action.clear()
    userinputraw = input("> ").lower().strip()
    choiceraw = stripattern.sub('', userinputraw)
    choice = choiceraw.split()

    listforsurroundings = set(choice).intersection(room[room_number].content)
    objectforsurroundings = ''.join(set(choice).intersection(room[room_number].content))
    commandfortravel = ''.join(set(choice).intersection(travel))
    commandfordirection = ''.join(set(choice).intersection(direction))
    fightcommandtype = ''.join(set(choice).intersection(fight_cmd))
    shoutcommandtype = ''.join(set(choice).intersection(shout_cmd))

    door1 = room[room_number].door_list[0]
    door2 = room[room_number].door_list[1]
    #door3 = room[room_number].door_list[2]
    type1 = door[door1].doortype
    type2 = door[door1].doortype
    type3 = door[door1].doortype
    major_door = copy.deepcopy(room[room_number].major_door)

    if major_door == None:
        if door[door1].status == "hidden":
            if door[door2].status == "hidden":
                major_door = None
            else:
                major_door = door2
        elif door[door2].status == "hidden":
            major_door = door1

    def door_conflict(door_action):
        nonlocal major_door
        if any(elem in choice for elem in door_direction):
            if door_direction[0] != door_direction[1]:
                print (door_direction[0], door_direction[1])
                if door_direction[0] in choice:
                    major_door = door1
                elif door_direction[1] in choice:
                    major_door = door2
        elif any(elem in choice for elem in [type1, type2]):
            if type1 in choice:
                major_door = door1
            elif type2 in choice:
                major_door = door2
        elif room[room_number].major_door == None:
            if door_direction[0] != door_direction[1]:
                print2 ("I don't know what to " + door_action +". Did you mean the " + type1 + " to the " + door_direction[0] + ", or the " + type2 + " to the " + door_direction[1] + "?")
                dooranswer = input("> ").lower().strip().split()
                if door_direction[0] in dooranswer:
                    major_door = door1
                elif door_direction[1] in dooranswer:
                    major_door = door2
                else:
                    print4 ("I'm sorry. I don't understand.")
                    continuetorm
            else:
                print2 ("I don't know what to " + door_action +". Did you mean the " + door[door1].doortype + ", or the " + door[door2].doortype + "?")
                dooranswer = input("> ").lower().strip().split()
                if door[door1].doortype in dooranswer:
                    major_door = door1
                elif door[door2].doortype in dooranswer:
                    major_door = door2
                else:
                    print4 ("I'm sorry. I don't understand.")
                    continuetorm

    if major_door == None:
        display_major = door1
    else:
        display_major = major_door

    # door status
    if door[display_major].status == "closed" and door[display_major].lockstatus == "locked":
        door_status = "a locked door"
    elif door[display_major].status == "closed":
        door_status = "a closed door"
    elif door[display_major].status == "open":
        door_status = "an open door"
    elif door[display_major].status == "smashed":
        door_status = "a broken door"
    elif door[display_major].status == "doorframe":
        door_status = "a doorframe"
    elif door[display_major].status == "hidden":
        door_status = "a door that doesn't exist"
    elif door[display_major].status == "revealed" or door[display_major].status == "blocked":
        door_status = "that"
    else:
        door_status = " INVALID_DOOR_STATUS"

    # if no command
    if userinputraw == '':
        print2 ("Whoops! You forgot to tell me what to do. If you don't know what to do, just type 'help'.")
        action_seq(surroundings, room_number, door_direction)
    # help
    elif any(elem in choice for elem in search_valid):
        current_action.append("help")
        if any(elem in choice for elem in add_inventory) or "pick" in choice and "up" in choice:
            print4 ("To pick up an object, you can say 'add', 'pickup', 'pick up', 'take', 'grab', or 'get'. For example, say 'pick up the lockpick' to have me pick up the lockpick.")
        elif any(elem in choice for elem in rmv_inventory):
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
        elif any(elem in choice for elem in door_lock):
            print4 ("To have me lock a door, just say 'lock the door', or 'lock the lock'. Keep in mind that if I lock an open door and then shut it, I will have to unlock it to open it again. I also need a lockpick to lock something, so make sure I've picked one up or mention it in your command, like 'lock the lock with the lockpick'.")
        elif "sleep" in choice:
            print4 ("To have me go to sleep, just say 'sleep'. However, I am a very deep sleeper, so keep in mind that I might not wake up when messaged.")
        elif any(elem in choice for elem in hide_cmds):
            print4 ("To have me hide, just say 'hide' and I can tell you if I see anything to hide behind. If I only see one thing, I'll hide straightaway, but if I don't see anything or I see more than one thing to hide behind, I'll ask you what to do next.")
        elif any(elem in choice for elem in dodge_cmd):
            print4 ("To have me dodge something, you can say 'dodge', 'avoid', 'evade', 'elude', 'escape', 'sidestep', or 'duck'. I'll dodge immediately.")
        elif any(elem in choice for elem in fight_cmd):
            print4 ("To have me fight something, you can say 'fight', 'hit', 'kick', 'punch', 'slap', 'smack', 'swat', 'strike', 'whallop', or 'slug'. If there's more than one enemy, I'll either ask you which one to hit, or just hit the most important one first.")
        else:
            print4 ("I can pick up or drop an object, smash or pick locks, doors, and walls, open or shut doors, sleep, hide, fight, dodge, and move. For a specific list of commands, type 'help [subset]', like 'help pick up'.")
    # pick up item
    elif any(elem in choice for elem in add_inventory) or "pick" in choice and "up" in choice:
        current_action.append("pickup")
        if len(listforsurroundings) >= 2:
            print4 ("I can't hold two things at once.")
        elif objectforsurroundings != '' and len(player.inventory) != 0:
            print4 ("I'm already holding the " + ''.join(player.inventory) + ".")
        elif all(elem in ["pick", "up"] for elem in choice) or all(elem in add_inventory for elem in choice):
            print4 ("What should I pick up?")
        elif 'door' in choice:
            door_conflict("pick up")
            if 'door' in player.inventory:
                print4 ("I'm already holding the door.")
            elif door[major_door].status == "smashed" and len(player.inventory) == 0:
                player.inventory.append("door")
                door[major_door].status = "doorframe"
                print4 ("I've picked up a door.")
            elif 'door' in room[room_number].content and len(player.inventory) == 0:
                player.inventory.append("door")
                room[room_number].content.remove("door")
                print4 ("I've picked up a door.")
            elif door[major_door].status != "smashed":
                print4 ("I can't pick up " + door_status +".")
            else:
                print4 ("Sorry, I can't find anything like that around here.")
        else:
            if objectforsurroundings != '' and len(player.inventory) == 0:
                player.inventory.append(str(objectforsurroundings))
                room[room_number].content.remove(str(objectforsurroundings))
                print4 ("I've picked up a " + str(objectforsurroundings) + ".")
            else:
                print4 ("Sorry, I can't find anything like that around here.")
    # drop item
    elif any(elem in choice for elem in rmv_inventory) or "put" in choice and "down" in choice:
        current_action.append("drop")
        if len(player.inventory) == 0:
            print4 ("I'm not holding anything.")
        elif len(player.inventory) != 0:
            print4 ("I've dropped the " + ''.join(player.inventory) + ".")
            room[room_number].content.append(''.join(player.inventory))
            player.inventory.clear()
        else:
            print4 ("Sorry, I'm not holding that right now.")
    # leave item
    elif any(elem in choice for elem in player.inventory):
        current_action.append("drop")
        if any(elem in choice for elem in [rmv_inventory, "leave"]):
            print4 ("I've dropped the " + ''.join(player.inventory) + ".")
            room[room_number].content.append(''.join(player.inventory))
            player.inventory.clear()
        else:
            print4 ("I don't understand. What do you want me to do with the " + ''.join(player.inventory) + "?")
    # go in a direction
    elif any(elem in choice for elem in travel):
        current_action.append("move")
        if commandfordirection != '':
            return commandfordirection
        elif "door" in choice:
            return "door"
        elif any(elem in choice for elem in stairssyn):
            door_conflict("go up")
            if door[major_door].doortype == "stair":
                return "stairs"
            else:
                print4 ("Sorry, I can't see any stairs around here.")
                continuetorm()
        elif all(elem in choice for elem in travel):
            print4 ("Whoops! You forgot to tell me which way to go!")
            continuetorm()
        elif any(elem in choice for elem in false_direction):
            print4 ("That's not very helpful, mostly because you don't know which way I'm actually facing, and so can't give me reliable directions. Try giving me a cardinal direction like 'northeast' instead.")
            continuetorm()
        else:
            print4 ("I don't know where to " + commandfortravel + ". Please say something like '" + commandfortravel + " northeast' instead.")
            continuetorm()
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
        def smash_something():
            door_conflict("smash")
            if "lock" in choice:
                if door[major_door].lockstatus == "smashed":
                    print4 ("The lock is already broken open.")
                elif door[major_door].status == "smashed":
                    print4 ("The door is already broken open.")
                elif "sledgehammer" not in player.inventory and "sledgehammer" not in choice:
                    print4 ("I don't have anything to smash the lock with.")
                elif door[major_door].lockstatus in smashable_lock:
                    if "sledgehammer" in player.inventory:
                        door[major_door].lockstatus = "smashed"
                        print4 ("I've smashed the lock.")
                    elif "sledgehammer" in choice:
                        if "sledgehammer" in room[room_number].content:
                            door[major_door].lockstatus = "smashed"
                            print4 ("I've smashed the lock.")
                        else:
                            print4 ("I can't see a sledgehammer anywhere near me.")
                    else:
                        print4 ("For some really weird reason I can't smash the lock. Sorry.")
                else:
                    print4 ("Sorry, I can't see a lock anywhere around here.")
            elif "wall" in choice:
                if "sledgehammer" not in player.inventory and "sledgehammer" not in choice:
                    print4 ("I don't have anything to smash the wall with.")
                else:
                    if room_number == 0:
                        wall_number = 1
                        right_direction_smash = north
                    elif room_number == 1:
                        wall_number = 1
                        right_direction_smash = south
                    else:
                        right_direction_smash = None
                    if any(elem in choice for elem in right_direction_smash):
                        door[wall_number].status = "revealed"
                        door[wall_number].lockstatus = None
                        print4 ("I smashed a hole in the wall. It looks big enough to easily walk through.")
                    elif any(elem in choice for elem in direction):
                        print ()
                        def smash_loop():
                            print ("> Time passes, the seconds punctuated with discordant and heavy thuds.")
                            print2 ("I don't think I'm getting anywhere. Should I keep going?")
                            cont_answer = yn_query("> ")
                            print()
                            if cont_answer:
                                enter()
                                smash_loop()
                            else:
                                print ("Alright. What should I try instead?")
                                continuetorm()
                        smash_loop()
                    else:
                        print4 ("I don't know which wall to smash.")
            elif "floor" in choice:
                if "sledgehammer" not in player.inventory and "sledgehammer" not in choice:
                    print4 ("I don't have anything to smash the floor with.")
                else:
                    print2 ("Are you sure I should smash through the floor?")
                    smash_answer = yn_query("> ")
                    if not smash_answer:
                        print4 ("Alright. What should I do instead?")
                        continuetorm()
                    else:
                        print ()
                        enter()
                        def smash_death():
                            print ("> Time passes, the seconds punctuated with discordant and heavy thuds.")
                            print2 ("I'm getting quite a few cracks here. Should I keep going?")
                            cont_answer = yn_query("> ")
                            if cont_answer:
                                print2 ("Alright. Here goes.")
                                enter()
                                player_death()
                                print1 ("> Eventually, a progressively louder cracking sound filters through the thuds of the sledgehammer, and it only takes a few more strikes for a thunderous rumbling to burst through the radio, almost drowning out the sound of screaming.")
                                print1 ("> After the rubble settles, there is nothing but static.")
                                game_over()
                            else:
                                print4 ("Alright. What should I do instead?")
                                continuetorm()
                        smash_death()
            elif door[major_door].status == "smashed":
                print4 ("The door is already broken open.")
            elif "sledgehammer" not in player.inventory and "sledgehammer" not in choice:
                print4 ("I don't have anything to smash the door with.")
            elif door[major_door].status in smashable_door:
                if "sledgehammer" in player.inventory:
                    door[major_door].status = "smashed"
                    door[major_door].lockstatus = None
                    print4 ("I've smashed the door.")
                elif "sledgehammer" in choice:
                    if "sledgehammer" in surroundings:
                        door[major_door].status = "smashed"
                        door[major_door].lockstatus = None
                        print4 ("I've smashed the door.")
                    else:
                        print4 ("I can't see a sledgehammer anywhere near me.")
                else:
                    print4 ("For some really weird reason I can't smash the door. Sorry.")
            else:
                print4 ("Sorry, I can't see a door anywhere around here.")
        smash_something()
    # unlock door
    elif any(elem in choice for elem in door_unlock):
        current_action.append("unlock")
        door_conflict("unlock")
        if door[major_door].lockstatus == "unlocked":
            print4 ("The door is already unlocked.")
        elif door[major_door].status == "smashed":
            print4 ("The door is already broken open.")
        elif door[major_door].lockstatus == "smashed":
            print4 ("The lock is already broken open.")
        elif door[major_door].lockstatus == "locked":
            if "lockpick" in player.inventory or "lockpick" in choice:
                door[major_door].lockstatus = "unlocked"
                print4 ("I've unlocked the door.")
            elif any(elem in choice for elem in [door_lock, "door"]) and "lockpick" in choice:
                if "lockpick" in room[room_number].content:
                    door[major_door].lockstatus = "unlocked"
                    print4 ("I've unlocked the door.")
                else:
                    print4 ("I can't see a lockpick anywhere near me.")
            elif "lockpick" not in player.inventory:
                print4 ("I don't have anything to pick the lock with.")
            else:
                print4 ("I don't understand.")
    # lock door
    elif any(elem in choice for elem in door_lock):
        current_action.append("lock")
        door_conflict("lock")
        if door[major_door].lockstatus == "unlocked":
            if "lockpick" in player.inventory:
                door[major_door].lockstatus = "locked"
                print4 ("I've locked the door.")
            elif any(elem in choice for elem in [door_lock, "door"]) and "lockpick" in choice:
                if "lockpick" in room[room_number].content:
                    door[major_door].lockstatus = "locked"
                    print4 ("I've locked the door.")
                else:
                    print4 ("I can't see a lockpick anywhere near me.")
            elif "lockpick" not in player.inventory:
                print4 ("I don't have anything to pick the lock with.")
            else:
                print4 ("I don't understand.")
        elif door[major_door].lockstatus == "locked":
            print4 ("The door is already locked.")
        elif door[major_door].status == "smashed":
            print4 ("The door is broken open.")
        elif door[major_door].lockstatus == "smashed":
            print4 ("The lock is broken open.")
    # open door
    elif "open" in choice:
        current_action.append("open")
        door_conflict("open")
        if door[major_door].status == "open":
            print4 ("The door is already open.")
        elif door[major_door].status == "smashed":
            print4 ("The door is already broken open.")
        elif door[major_door].status == "closed":
            if door[major_door].lockstatus == "locked":
                if any(elem in choice for elem in forcefully_cmd):
                    print4 ("The lock refuses to budge.")
                else:
                    print4 ("The door is locked.")
            elif door[major_door].lockstatus == "unlocked" or door[major_door].lockstatus == "smashed":
                if len(player.inventory) == 0:
                    door[major_door].status = "open"
                    print4 ("I've opened the door.")
                else:
                    print4 ("I can't open the door while I'm holding something.")
        else:
            print4 ("Sorry, I can't see a door anywhere around here.")
    # close door
    elif any(elem in choice for elem in door_close):
        current_action.append("close")
        door_conflict("close")
        if door[major_door].status == "closed":
            print4 ("The door is already shut.")
        elif door[major_door].status == "smashed":
            print4 ("The door is broken open.")
        elif len(player.inventory) == 0 and door[major_door].status == "closed":
            door[major_door].status = "closed"
            print4 ("I've closed the door.")
        elif len(player.inventory) != 0 and door[major_door].status == "open":
            print4 ("I can't shut the door while I'm holding something.")
        else:
            print4 ("Sorry, I can't see a door anywhere around here.")
    # lever
    elif "lever" in choice:
        current_action.append("lever")
        if "lever" not in room[room_number].content:
            print4 ("Sorry, I can't see a lever anywhere around here.")
        else:
            if any(elem in choice for elem in lever_cmd):
                return "lever"
            else:
                print4 ("What do you want me do to with the lever?")
    # hide
    elif any(elem in choice for elem in hide_cmds):
        current_action.append("hide")
        door_conflict("hide behind")
        if door[major_door].status == "open" or door[major_door].status == "smashed" or "door" in player.inventory or "door" in room[room_number].content:
            return "hide"
        else:
            print4 ("I can't see anything to hide behind.")
    # sleep
    elif any(elem in choice for elem in sleep_cmd):
        current_action.append("sleep")
        print2 ("That seems like a good idea. Goodnight!")
        player.status = "unconscious"
        sleepnumber = random.randint(0,9)
        def sleeploop():
            enter()
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
        innocent_object = None
        x = fight_cmd.index(fightcommandtype)
        if "kick" in choice:
            limb = "foot"
        else:
            limb = "hand"
        if "door" in choice:
            innocent_object = "door"
        elif "wall" in choice:
            innocent_object = "wall"
        elif "floor" in choice:
            innocent_object = "floor"
        elif "lockpick" in choice:
            innocent_object = "lockpick"
        elif "sledgehammer" in choice:
            innocent_object = "sledgehammer"
        else:
            innocent_object = None
        if any(elem in choice for elem in chargeobj_cmds):
            door_conflict("smash")
            if "door" in choice and door[major_door].status in door_in_frame:
                print4 ("I charged the door. Nothing happened. My shoulder, however, is in a fair amount of pain.")
            elif "door" in choice and door[major_door].status not in door_in_frame:
                print4 ("I don't see a door I could shoulder open.")
            elif "wall" in choice:
                print4 ("I charged the wall. Nothing happened. My shoulder, however, is in a fair amount of pain.")
        elif any(elem in choice for elem in [door_lock, "wall", "door"]):
            if "sledgehammer" in choice or "sledgehammer" in player.inventory:
                smash_something()
            else:
                print4 ("I " + fight_cmd_past[x] + " the " + innocent_object + ". My " + limb + " hurts.")
        elif innocent_object == None:
            if "self" in choice or "yourself" in choice:
                print4 ("What?! No! I'm not hitting myself without a very good reason.")
            else:
                print4 (fightcommandtype.capitalize() + " what? There's nothing there!")
        else:
            print4 ("I " + fight_cmd_past[x] + " the " + innocent_object + ". My " + limb + " hurts.")
    # shout
    elif any(elem in choice for elem in shout_cmd):
        x = shout_cmd.index(shoutcommandtype)
        if "door" in choice:
            innocent_object = "door"
        elif "wall" in choice:
            innocent_object = "wall"
        elif "floor" in choice:
            innocent_object = "floor"
        elif len(listforsurroundings) != 0:
            if len(listforsurroundings) >=2:
                innocent_object = None
            else:
                innocent_object = objectforsurroundings
        else:
            innocent_object = "void"
        if innocent_object == None:
            print4 ("I " + shout_cmd_past[x] + " at the innocent inanimate objects. They seem remarkably unmoved. At least for innocent inanimate objects.")
        elif innocent_object == "void":
            print4 ("I " + shout_cmd_past[x] + " into the void, and all I heard in response was the echoes of my own voice. \n...that's depressing. Moving on!")
        else:
            print4 ("I " + shout_cmd_past[x] + " at the " + innocent_object + ". It seems remarkably unmoved. At least for a " + innocent_object + ".")
    # say hi
    elif any(elem in choice for elem in greetings):
        if "door" in choice:
            innocent_object = "door"
        elif "wall" in choice:
            innocent_object = "wall"
        elif "floor" in choice:
            innocent_object = "floor"
        elif len(listforsurroundings) != 0:
            if len(listforsurroundings) < 2:
                innocent_object = objectforsurroundings
            else:
                innocent_object = None
        else:
            innocent_object = None
        if innocent_object != None:
            print4 ("I greeted the " + innocent_object + " . It seems remarkably unmoved. At least for a " + innocent_object + ".")
        else:
            print4 ("Hello there!")
    # say bye
    elif any(elem in choice for elem in farewells):
        if "door" in choice:
            innocent_object = "door"
        elif "wall" in choice:
            innocent_object = "wall"
        elif "floor" in choice:
            innocent_object = "floor"
        elif len(listforsurroundings) != 0:
            if len(listforsurroundings) < 2:
                innocent_object = objectforsurroundings
            else:
                innocent_object = None
        else:
            innocent_object = None
        if innocent_object != None:
            print4 ("I told the " + innocent_object + " goodbye. It seems remarkably unmoved. At least for a " + innocent_object + ".")
        else:
            print2 ("Wait. Are you leaving?")
            leaving_answer = yn_query("> ")
            if leaving_answer:
                print2 ("Well then. Goodbye, I guess.")
                disconnecting()
            else:
                print4 ("Well then why'd you say that? Whatever. Moving on.")
    # jump
    elif any(elem in choice for elem in jump_cmds):
        print4 ("I jumped on the spot.")
    # unhelpful commands
    elif any(elem in choice for elem in unhelpful_cmds):
        print2 ("Wow. You're sooooo helpful. Wanna try again?")
        helpful = yn_query("> ")
        if helpful:
            print2 ("Cool. Let's get to it.")
        elif not helpful:
            print2 ("Alright. You're clearly not going to be any help. Bye.")
            game_over()
    # alexa
    elif "alexa" in choice:
        print4 ("Yes? What do you want me to do?")
    # siri
    elif "siri" in choice:
        print4 ("Not exactly. We are friends though. What do you want me to do?")
    # cortana
    elif "cortana" in choice:
        print4 ("Nope. I do know her though. What do you want me to do?")
    # no command
    else:
        print4 ("I don't understand. If you're having trouble, type 'help' to see what you can tell me to do.")

# used to ask the player name
def player_name(question):
    sys.stdout.write(question)
    playernameraw = input("My name is ").capitalize().strip().replace('  ', ' ')
    playernameinput = stripattern.sub('', playernameraw)
    if playernameinput == '':
        player_name(question)
    else:
        print2 (playernameinput.capitalize() + ". I like it. I think.")
        print ("> Press enter to continue or type 'retry' to enter your name again")
        player.name = playernameinput.capitalize()
        answer = stopgo_query("> ", "yes")
        if answer:
            clear_screen()
            pt_5()
        if not answer:
            print ()
            player_name(question)

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
    adventureif

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
                    disconnecting = False
            if not answer:
                game_over()
    if not answer:
        print2 ("> Connection restored.")
        enter()
        print ("Oh, you're back.")
        disconnecting = False
    return disconnecting

# title, plays game
def title():
    print ()
    print ("  ██╗    ██╗██╗  ██╗███████╗██████╗ ███████╗")
    print ("  ██║    ██║██║  ██║██╔════╝██╔══██╗██╔════╝")
    print ("  ██║ █╗ ██║███████║█████╗  ██████╔╝█████╗  ")
    print ("  ██║███╗██║██╔══██║██╔══╝  ██╔══██╗██╔══╝  ")
    print ("  ╚███╔███╔╝██║  ██║███████╗██║  ██║███████╗")
    print ("   ╚══╝╚══╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝")
    print ()
    enter_play()
    pt_2()

# after title, glitch hello
def pt_2():
    print1 ("> Transmission detected. Isolating signal...")
    enter()
    print1 ("> Significant static interference. Initiating static scrubbing.")
    enter()
    print ()
    print ()
    print2 ("Ḩ̵̠̮̺̻͔̼̥̭̗͎̝̝̤̱̳͙̺̤͋̈́͋̈́̎̈̎́̾̓̽͋̂͗͌̉̈͊̌́̚͝ͅȩ̸̂͊̄̀̉̎̓̄̉̊͒͛l̵̢̢̮̙͖̠̦͈̪̲̜͖͍̼͚̟͓̃̈́̑̑͂̆̆͂̂͆͑̉̓́̑́͋̚̚͝l̵̘̝͈̈́̚͜o̴͙̰̦͚̞͉̘̹̼͓̙̜͆̈́̔͛͆̎.̶̢̨͔̰͉̹̞͓͎̻̤͉̠̟̜̳͇̟̌̈́̀́͠")
    print ()
    print ()
    print ()
    print1 ("> Scrubbing 17% complete.")
    enter()
    print2 ("H̴͉̮̯̱̺̱̏̓ę̸͈̟̫͇̝͕̬͓̺͎̥̼̊̇̒͐͛̄̚l̷̟͎̭̽̈́̈́͑̿́̓́̊́͊͠l̷̬̖̬̘̥̜̈̇̀o̶̢̡͈͔̞͔̺̗̥̘̼̍̓̾̾͜.̵̢͍̩̣̙̻͉̗̫̣̦̰̇̿̏̒̈̓͂̕͘ͅ")
    print ()
    print ()
    print1 ("> Scrubbing 41% complete.")
    enter()
    print2 ("Ḧ̸̡̟́͜͝ę̵̧̈́͌̆ļ̸̤̻͝l̶̖͘͝o̸͖̬̊͆̊.")
    print1 ("> Scrubbing 78% complete.")
    enter()
    print2 ("H̶̘̎e̵̬̋l̶̮̅l̵͇͌ò̶̲.")
    print1 ("> Scrubbing 99% complete.")
    enter()
    print1 ("Hello.")
    print1 ("> Scrubbing complete. Initiating transmission.")
    enter()
    pt_3()

# can you hear me? [y/n]
def pt_3():
    print ("Oh! Oh my god, I wasn't expecting an answer, not after this long.")
    print1 ("Can you hear me?")
    answer = yn_query("> ")
    if answer:
        print2 ("You can hear me!")
    if not answer:
        print2 ("Wait. You can hear me, or you wouldn't have answered!")
    enter()
    print1 ("No one's been able to hear me before.")
    enter()
    pt_4()

# who are you? [name]
def pt_4():
    print1 ("Who are you?")
    player_name("> ")

# can you help me find out who I am? [y/n]
def pt_5():
    print1 ("Can you help me find out where I am?")
    answer = yn_query("> ")
    if answer:
        print4 ("Ok then! Let's do this.")
        print ("I woke up here. Don't know where here is, just what it looks like.")
        rm_1_setup()
    if not answer:
        print2 ("Oh. Ok. Goodbye.")
        enter ()
        disconnected = disconnecting()
        if not disconnected:
            print ()
            pt_5()
        if disconnected:
            game_over()

# punctuates a list with commas and 'and'
def make_item_list(items, phrase):
    if len(items) == 0:
        return "nothing else" + phrase
    elif len(items) == 1:
        return "a {}".format(items[0]) + phrase
    elif len(items) == 2:
        return "a {} and a {}".format(items[0], items[1]) + phrase
    else:
        last = items[-1]
        rest = ", a ".join(items[0:-1])
        return "a {}, and a {}".format(rest, last) + phrase

# open world room 1 play
def rm_1_interactive():
    current_room.clear
    current_room.append("rm1")
    if len(player.inventory) != 0:
        holding = " holding a " + ''.join(player.inventory)
    else:
        holding = ''

    article = ''
    if door[0].status == "closed" and door[0].lockstatus == "locked":
        door_status = " locked door"
    elif door[0].status == "closed":
        door_status = " closed door"
    elif door[0].status == "open":
        article = "n"
        door_status = " open door"
    elif door[0].status == "smashed":
        door_status = " broken door"
    elif door[0].status == "doorframe":
        article = "n"
        door_status = " empty doorframe"
    else:
        door_status = " INVALID_DOOR_STATE"

    potential_near_me = ["sledgehammer", "lockpick", "door"]
    near_me = [value for value in room[0].content if value in potential_near_me] # gets intersection of lists without using sets

    hole_status = " and a hole in the wall" if door[1].status != "hidden" else ''
    comma = "," if door[1].status != "hidden" else ''

    print ("I'm" + holding + " in a room with a" + article + door_status + hole_status + " to the north" + comma + " and " + make_item_list(near_me, " near me."))
    print1 ("What should I do?")
    answer_action = action_seq(room[0].content, 0, ["north", "north"])
    # move
    if "move" in current_action:
        current_action.clear()
        if any(elem in answer_action for elem in north_east) or any(elem in answer_action for elem in north_west):
            print4 ("There's a wall there. I can't go that way.")
            rm_1_interactive()
        elif any(elem in answer_action for elem in north) and door[0].status == "closed":
            print4 ("I can't go through a closed door.")
            rm_1_interactive()
        elif any(elem in answer_action for elem in north) and door[0].status in walkable_door:
            print2 ("Moving north.")
            enter()
            rm_2_setup()
            print (answer_action)
        elif "door" in answer_action and door[0].status in walkable_door:
            print2 ("Going through the door.")
            enter()
            rm_2_setup()
        elif "hole" in answer_action or "wall" in answer_action and "north wall hole" in room[0].content:
            print2 ("Going through the wall.")
            enter()
            rm_2_setup()
        elif "door" in answer_action and door[0].status == "closed":
            print4 ("I can't go through a closed door.")
            rm_1_interactive()
        else:
            print4 ("There's a wall there. I can't go that way.")
            rm_1_interactive()
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
                        rm_1_interactive()
                keep_hiding()
            else:
                print4 ("Alright. I'm stepping out from behind the door now.")
                rm_1_interactive()
        if door[0].status == "open":
            print2 ("I'm hiding behind the door, but I don't feel like I'm hidden very well. Should I keep hiding?")
            hide_query()
        elif door[0].status == "smashed" or "door" in room[0].content or "door" in player.inventory:
            print2 ("I'm hiding under the broken door, and I feel like I'm hidden fairly well. Should I keep hiding?")
            hide_query()
        else:
            current_action.clear()
            rm_1_interactive()
    # leave
    elif "leave" in current_action:
        hole_status = " or the hole in the wall" if "north wall hole" in room[0].content else ''
        print4 ("The only exit I see is through the" + door_status + hole_status + " to the north.")
        rm_1_interactive()
    else:
        current_action.clear()
        rm_1_interactive()

def rm_2_interactive():
    current_room.clear
    current_room.append("rm2")
    if len(player.inventory) != 0:
        holding = " holding a " + ''.join(player.inventory)
    else:
        holding = ''

    article = ''
    if door[0].status == "closed" and door[0].lockstatus == "locked":
        door_status = " locked door"
    elif door[0].status == "closed":
        door_status = " closed door"
    elif door[0].status == "open":
        article = "n"
        door_status = " open door"
    elif door[0].status == "smashed":
        door_status = " broken door"
    elif door[0].status == "doorframe":
        article = "n"
        door_status = " empty doorframe"
    else:
        door_status = " INVALID_DOOR_STATE"

    potential_near_me = ["lockpick", "sledgehammer", "door"]
    near_me = [value for value in room[1].content if value in potential_near_me] # gets intersection of lists without using sets

    hole_status = " and a hole in the wall" if door[1].status != "hidden" else ''

    print ("I'm" + holding + " in a room with a" + article + door_status + hole_status + " to the south, a lever in the middle of the room, and " + make_item_list(near_me, " near me."))
    print1 ("What should I do?")
    answer_action = action_seq(room[1].content, 1, ["south", "south" "north"])
    # move
    if "move" in current_action:
        current_action.clear()
        if any(elem in answer_action for elem in south_east) or any(elem in answer_action for elem in south_west):
            print4 ("There's a wall there. I can't go that way.")
            rm_2_interactive()
        elif "stairs" in answer_action:
            if door[2].status == "revealed":
                print4 ("Going up the stairs.")
                rm_3_setup()
            elif door[2].status == "blocked":
                print4 ("I took a few steps up the stairs, but decided not to hit my head on the ceiling.")
                rm_2_interactive()
            else:
                print4 ("Sorry, I don't see any stairs around here.")
                rm_2_interactive()
        elif any(elem in answer_action for elem in south) and "closed door" in room[1].content:
            print4 ("I can't go through a closed door.")
            rm_2_interactive()
        elif any(elem in answer_action for elem in south) and door[0].status in walkable_door:
            print2 ("Moving south.")
            enter()
            rm_2_interactive()
            print (answer_action)
        elif "door" in answer_action and door[0].status in walkable_door:
            print2 ("Going through the door.")
            enter()
            rm_2_interactive()
        elif "hole" in answer_action or "wall" in answer_action and "south wall hole" in room[1].content:
            print2 ("Going through the wall.")
            enter()
            rm_2_interactive()
        elif "door" in answer_action and door[0].status == "closed":
            print4 ("I can't go through a closed door.")
            rm_2_interactive()
        else:
            print4 ("There's a wall there. I can't go that way.")
            rm_2_interactive()
    # pull lever
    elif "lever" in current_action:
        if door[2].status == "hidden":
            door[2].status = "revealed"
            print4 ("As soon as I touched the lever, it fell forward, and a set of stairs unfolded from the wall, going up until it meets the ceiling. I assume that the stairs continue past the ceiling, but it could just be a weirdly useless secret staircase.")
            rm_2_interactive()
        elif door[2].lockstatus == "blocked":
            door[2].lockstatus = None
            print4 ("This time, a panel in the ceiling right above the stairs folded into itself. I can go up the stairs now.")
            rm_2_interactive()
        else:
            print4 ("The lever is locked in place.")
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
                        rm_2_interactive()
                keep_hiding()
            else:
                print4 ("Alright. I'm stepping out from behind the door now.")
                rm_2_interactive()
        if door[0].status == "open":
            print2 ("I'm hiding behind the door, but I don't feel like I'm hidden very well. Should I keep hiding?")
            hide_query()
        elif door[0].status == "smashed" or "door" in room[1].content or "door" in player.inventory:
            print2 ("I'm hiding under the broken door, and I feel like I'm hidden fairly well. Should I keep hiding?")
            hide_query()
        else:
            current_action.clear()
            rm_2_interactive()
    # leave
    elif "leave" in current_action:
        hole_status = " or the hole in the wall" if "south wall hole" in room[1].content else ''
        stair_status = " or the stairs to the north" if door[2].status != "hidden" else ''
        print4 ("The only exit I see is through the" + door_status + hole_status + " to the south" + stair_status + ".")
        rm_2_interactive()
    else:
        current_action.clear()
        rm_2_interactive()

# open world room 1 setup
def rm_1_setup():
    door[0].status == "closed"
    door[0].lockstatus == "locked"
    rm_1_interactive()

def rm_2_setup():
    if "north wall hole" in room[0].content:
        room[1].content.append("south wall hole")
    room[1].content.append("lever")
    rm_2_interactive()

# scripted end, will use in lieu of rooms that aren't set up
def rm_3_setup():
    playernameused = player.name.lower().strip().replace(' ', '')
    current_action.clear()
    print ("Hey look! I see a piece of paper.")
    print1 ("I'm gonna pick it up.")
    enter()
    print1 ("It says: 'You're in an Alexa.'")
    enter()
    print1 (">>Hey Alexa! Play generic pop song #37!<<")
    print1 ("I gotta go. Thanks for helping!")
    print1 (">>HEY ALEXA!<<")
    print1 ("okireallygottagothanksagain" + playernameused + "bye")
    game_over()

#def rm_2_setup():

#title()
rm_1_setup()