import os
import random
import getpass

# list of playable words
words = [
    "acromantula",
    "billywig",
    "boggart",
    "bowtruckle",
    "crup",
    "dementor",
    "demiguise",
    "doxy",
    "erumpent",
    "giant squid",
    "hidebehind",
    "hippogriff",
    "horklump",
    "jobberknoll",
    "kappa",
    "knarl",
    "kneazle",
    "murtlap",
    "niffler",
    "nundu",
    "occamy",
    "vipertooth",
    "puffskein",
    "runespoor",
    "snidget",
    "streeler",
    "thestral",
    "thunderbird",
    "wampus"
    ]

allowed_characters = set(map(chr, range(ord('a'), ord('z') + 1)))   # list of lowercase letters from a to z
hangman_parts = [ "head", "left arm", "torso", "right arm", "left leg", "right leg" ]
guess_limit = len(hangman_parts)    # len() gets us the length of the list

user_guess = []    # basket for right and wrong user guesses
check_if_won = []    # basket for right user guesses
played_words = []    # basket for previously played words
inputname = [] # basket for player name

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

# press enter to continue
def enter():
    press_enter = getpass.getpass("> Press enter to continue ")
    if press_enter == '':
        clear_screen()
    else:
        clear_screen()

# press enter to play again without title screen
def enter_play_again():
    print ()
    press_enter = getpass.getpass("> Press enter to play again ")
    if press_enter == '':
        clear_screen()
    else:
        clear_screen()
    all_playthroughs_after_that()

# press enter to play again with title screen and name
def enter_play_again_major():
    print ()
    press_enter = getpass.getpass("> Press enter to play again ")
    if press_enter == '':
        clear_screen()
    else:
        clear_screen()
    first_playthrough()

# print title screen
def title_hangman():
    print ()
    print ("  ██╗  ██╗  █████╗  ███╗   ██╗  ██████╗  ███╗   ███╗  █████╗  ███╗   ██╗")
    print ("  ██║  ██║ ██╔══██╗ ████╗  ██║ ██╔════╝  ████╗ ████║ ██╔══██╗ ████╗  ██║")
    print ("  ███████║ ███████║ ██╔██╗ ██║ ██║  ███╗ ██╔████╔██║ ███████║ ██╔██╗ ██║")
    print ("  ██╔══██║ ██╔══██║ ██║╚██╗██║ ██║   ██║ ██║╚██╔╝██║ ██╔══██║ ██║╚██╗██║")
    print ("  ██║  ██║ ██║  ██║ ██║ ╚████║ ╚██████╔╝ ██║ ╚═╝ ██║ ██║  ██║ ██║ ╚████║")
    print ("  ╚═╝  ╚═╝ ╚═╝  ╚═╝ ╚═╝  ╚═══╝  ╚═════╝  ╚═╝     ╚═╝ ╚═╝  ╚═╝ ╚═╝  ╚═══╝")
    print ()
    enter_play()

# asks player name
def asks_name():
    inputname.clear()
    print ()
    name = input("  What is your name?  > ").strip()
    clear_screen()
    print ()
    if name == '':
        print ("  Let's play hangman!")
    else:
        print ("  Hi " + name + ". Let's play hangman!")
    print ()
    enter()
    inputname.append(name)

# makes playername a global variable (kinda)
def makes_name():
    playername = ''.join(inputname)
    return playername

# draws hangman
def draw(num_wrong):
    if num_wrong > guess_limit:
        # increment the count if wrong guess
        num_wrong = guess_limit
    hangman_characters = {
        "head" : "  O",
        "left arm" : " /",
        "torso" : "|",
        "right arm" : "\\",
        "left leg" : " /",
        "right leg" : " \\"
    }
    hangman_newlines = [ "head", "right arm", "right leg" ]
    output = " _____\n |   |\n | "
    num_newlines = 0
    for i in range(num_wrong):
        output = output + hangman_characters[hangman_parts[i]]
        if hangman_parts[i] in hangman_newlines:
            output = output + "\n | "
            num_newlines = num_newlines + 1
    for i in range(len(hangman_newlines) - num_newlines):
        output = output + "\n |"
    output = output + "____\n\n"
    print (output)

# plays right, wrong, invalid, duplicate, empty guesses
def right_wrong_invalid(guess_limit, word):
    wrong_user_guess = 0
    while wrong_user_guess < guess_limit and set(word) != set(check_if_won):
        user_guess_display = sorted(set(user_guess), key=user_guess.index)
        print ()
        print ("  [FOR TESTING ONLY] Your word is " + word + ".")    # for testing only, remove after development
        print ("  Your word has " + str(len(word)) + " letters.")
        if len(user_guess) == 0:
            print ()
        else:
            print ()
            print ("  You have guessed " + ', '.join(user_guess_display))
            print ()
        user = input("> What is your guess?  > ").strip().lower()
        if len(user) > 1:    # if more than one character
            print ()
            print ("  Whoops! Looks like you entered more than one character. Please enter one letter at a time.")
            print ()
        else:    # if one character
            if user.isalpha():    # if the character is a letter
                if user in user_guess:    # if the letter has already been guessed
                    print ()
                    print ("  You've already guessed this. Please guess again.")
                    print ()
                else:    # if the letter hasn't been guessed
                    if user in word:    # if the letter is in the word
                          print ()
                          print ("  Right :)")
                          draw(wrong_user_guess)
                          user_guess.append(user)    # puts right input in user_guess basket
                          check_if_won.append(user)    # puts right input in check_if_won basket
                    else:    # if the letter is not in the word
                        print ()
                        print ("  Wrong :(")
                        wrong_user_guess += 1
                        draw(wrong_user_guess)
                        user_guess.append(user)    # puts wrong input in user_guess basket
            elif user == '':    # if the guess is empty
                print ()
                print ("  Please enter your guess.")
                print ()
            else:    # if the character is not a letter
                print ()
                print ("  Invalid guess. Please guess again.")
                print ()

        enter()
    return wrong_user_guess    # states output to call in win_lose

# gives definition of word
def definition():
    print ()
    if word == "acromantula":
        print ("  An Acromantula is a species of giant spider, native to the rainforests of Southeast Asia, \n"
               "  particularly Borneo, where it inhabits dense jungles. It is believed to be a wizard-bred species, \n"
               "  designed to guard dwellings or treasure hoards, and was first created before the Ban on Experimental \n"
               "  Breeding in 1965. This giant spider with a taste for human flesh was first spotted in 1794.")
    if word == "billywig":
        print ("  A Billywig is an insect native to Australia, and is around half an inch long with a vivid sapphire blue \n"
               "  colouring. The speed of the Billywig means that it is rarely noticed by Muggles, and wizards and \n"
               "  witches can typically only spot it after they have been stung.")
    if word == "boggart":
        print ("  A boggart is an amortal shape-shifting non-being that takes on the form of the viewer's worst fear. \n"
               "  Because of its shape-shifting ability, no one knows what a boggart looks like when it is alone, as it\n"
               "  instantly changes into one's worst fears when one first sees it.")
    if word == "bowtruckle":
        print ("  A Bowtruckle is a hand-sized, insect-eating tree dweller with long, sharp fingers (two on each \n"
               "  hand), brown eyes, and a general appearance of a flat-faced stick figure made of bark and twigs, \n"
               "  which serves well as camouflage in its natural habitat. It is immensely difficult to spot.")
    if word == "crup":
        print ("  A crup strongly resembles a Jack Russell Terrier with a forked tail. It is a wizard-bred dog that \n"
               "  is extremely loyal to wizards, and exceptionally ferocious towards Muggles. It is a great scavenger, \n"
               "  and eats everything from gnomes to old tires.")
    if word == "dementor":
        print ("  A Dementor is a gliding, wraith-like Dark creature, widely considered to be one of the foulest \n"
               "  things to inhabit the world. It feeds on human happiness, and thus generates feelings of depression \n"
               "  and despair in any person in its immediate vicinity.")
    if word == "demiguise":
        print ("  A Demiguise is a peaceful, herbivorous creature that can make itself invisible and see the future, \n"
               "  making it very hard to catch. It is found in the Far East, but only wizards and witches trained in \n"
               "  its capture can even see it. It resembles an ape with large, black eyes and long, silky hair.")
    if word == "doxy":
        print ("  A Doxy is covered in coarse black hair, and has additional set of arms and legs. It has shiny \n"
               "  beetle-like wings, and a double row of sharp venomous teeth. If bitten, an antidote should be taken \n"
               "  immediately.")
    if word == "erumpent":
        print ("  An Erumpent resembles a rhinoceros with a roundish body. It is a powerful creature, with a thick \n"
               "  hide capable of repelling most curses and charms, a single long horn, and a thick tail. Treat with \n"
               "  extreme caution.")
    if word == "giant squid":
        print ("  The largest invertebrate known to Muggle science, the giant squid can grow to 70 feet in length. It \n"
               "  possesses an unnerving level of intelligence, and is strongly suspected to have magical \n"
               "  capabilities.")
    if word == "hidebehind":
        print ("  A Hidebehind is a nocturnal, forest-dwelling spectre-like beast that preys on humanoids. It can \n"
               "  shift its shape, allowing it to hide behind almost any object.")
    if word == "hippogriff":
        print ("  A Hippogriff is a magical creature that has the front legs, wings, and head of a giant eagle and \n"
               "  the body, hind legs and tail of a horse. It is very similar to another mythical creature, the \n"
               "  Griffin, with the horse rear replacing the lion rear.")
    if word == "horklump":
        print ("  A Horklump is a magical creature that resembles a fleshy pink mushroom covered in sparse black \n"
               "  bristles. It has no descernible use or purpose, and is nearly invulnerable.")
    if word == "jobberknoll":
        print ("  A Jobberknoll is a small, blue speckled bird that never makes any noise until just before it dies. \n"
               "  It then lets out a long scream, which consists of every sound it has ever heard backwards. \n"
               "  Jobberknoll feathers are used in Truth Serums and Memory Potions.")
    if word == "kappa":
        print ("  A Kappa is a Japanese water demon that feeds on human blood. It is known for strangling humans that \n"
               "  invade their shallow ponds.")
    if word == "knarl":
        print ("  The Knarl greatly resembles a hedgehog, so much so that there is only one known (behavioural) \n"
               "  difference between them: when food is left out for a hedgehog it will appreciate and enjoy the \n"
               "  gift; but a knarl will see it as an attempt to lure it into a trap and hence savage the giver's \n"
               "  garden.")
    if word == "kneazle":
        print ("  A Kneazle is a magical feline creature related to, and similar in appearance to, a cat. It has \n"
               "  spotted, speckled or flecked fur, large ears and a lightly plumed tail, like a lion. It has \n"
               "  separate breeds, like cats, and therefore varies in appearance. It makes for an excellent pet.")
    if word == "murtlap":
        print ("  A Murtlap is a marine beast that resembles a rat with a growth on its back resembling a sea anemone, \n"
               "  and is found on the coastal areas of Britain. Its bite can incapacitate Muggles.")
    if word == "niffler":
        print ("  A Niffler is a were rodent-like creature with a long snout (similar to that of a platypus) and a \n"
               "  coat of black, fluffy fur. It is attracted to shiny things, and keeps its findings in a magically \n"
               "  expanded pouch on its belly.")
    if word == "nundu":
        print ("  A Nundu is a large East African beast that resembles a leopard. It moves silently, despite its \n"
               "  gigantic size, and is considered by some to be the most dangerous creature in existence. The breath \n"
               "  of the Nundu is extremely toxic and filled with a disease so potent that it can wipe out entire \n"
               "  villages. It is notoriously hard to subdue, requiring at least one hundred wizards working together \n"
               "  to be defeated.")
    if word == "occamy":
        print ("  An Occamy is a winged serpentine beast native to Asia. It is a plumed, two-legged, \n"
               "  serpentine-bodied creature with wings that reached up to fifteen feet in height. It is extremely \n"
               "  aggressive to anyone who approaches it, and lives off of insects, rats, birds, and occasionally \n"
               "  monkeys. It is extremely protective of its eggs, which are made of an extremely pure and soft \n"
               "  silver. It is also choranaptyxic, and grows or shrinks to fit available space.")
    if word == "vipertooth":
        print ("  The Peruvian Vipertooth is native to the eastern and northeastern parts of Peru. It is the smallest, \n"
               "  fastest, and most venomous dragon. Its scales are smooth and copper-coloured, and has black \n"
               "  ridge-markings and short horns on its head. The Vipertooth mainly feeds on goats and cows, but is \n"
               "  infamous for its particular craving for humans.")
    if word == "puffskein":
        print ("  A Puffskein is a small beast covered in soft fur and spherical in shape. It is a popular pet \n"
               "  worldwide, and does not object to being cuddled or thrown about. It is extremely easy to care for, \n"
               "  and emits a low humming sound when content.")
    if word == "runespoor":
        print ("  A Runespoor is a three-headed snake native to the African country of Burkina Faso and is commonly \n"
               "  associated with Dark Wizards. It is typically six to seven feet long, with orange and black stripes. \n"
               "  The Burkina Faso Ministry of Magic has had to make several forests Unplottable for its use.")
    if word == "snidget":
        print ("  A Snidget is a small round-bodied bird that was chased as part of the game of Quidditch for about a \n"
               "  century in the 1200s and 1300s, until it almost went extinct. Also known as the Golden Snidget, \n"
               "  this small, spherical bird can fly with amazing agility, changing speed and direction almost \n"
               "  instantaneously.")
    if word == "streeler":
        print ("  The Streeler is a giant snail that has sharp, venomous spikes on its shell. It changes colour \n"
               "  hourly, and leaves behind a trail of venom so toxic that it burns everything that it touches. It is \n"
               "  kept as a pet by those who enjoy its kaleidoscopic colour changes. Streeler venom is one of the few \n"
               "  known substances that can kill Horklumps.")
    if word == "thestral":
        print ("  A Thestral is a winged horse with a skeletal body, reptilian face, and wide, leathery wings that \n"
               "  resemble a bat's. It is very rare, and is visible only to those who have witnessed death at least \n"
               "  once.")
    if word == "thunderbird":
        print ("  A Thunderbird is a large, avian creature native to North America, and is most commonly found in \n"
               "  Arizona. A close relative of the Phoenix, it can create storms as it flies, and is highly sensitive \n"
               "  to impending danger.")
    if word == "wampus":
        print ("  A Wampus can walk on its hind legs and outrun arrows, and its yellow eyes are rumored to have the \n"
               "  power of both hypnosis and Legilimency. It is extremely fast, extremely strong, and almost \n"
               "  impossible to kill.")

# if lost game
def lost_game():
    playernameused = makes_name()
    print ()
    if playernameused:
        print ("  Oh no! You lost. Your word was " + word + ".")
    else:
        print ("  Sorry " + playernameused + ". You lost. Your word was " + word + ".")
    enter_play_again()

# if won game
def won_game():
    played_words.append(word)
    playernameused = makes_name()
    print ()
    if playernameused == '':
        print ("  Congratulations! You won! Your word was " + word + ".")
    else:
        print ("  Congratulations " + playernameused + "! You won! Your word was " + word + ".")
    print ("  (＾ヮ＾)╯\(＾ヮ＾)")
    definition()
    enter_play_again()

# plays win or lose
def win_lose():
    wrong_user_guess = right_wrong_invalid(guess_limit, word)    # calls right_wrong_invalid
    if wrong_user_guess == guess_limit:    # if game is lost
        lost_game()
    win_requirement_met = all(elem in set(check_if_won) for elem in set(word))     # if check_if_won has everything in word
    if win_requirement_met:
        won_game()

# chooses a random word to play with no repeats
def psuedo_random():
    word = random.choice(words)
    if word in played_words:
        psuedo_random()
    return word

# first playthrough
def first_playthrough():
    user_guess.clear()
    check_if_won.clear()
    played_words.clear()
    inputname.clear()
    title_hangman()
    asks_name()

# minor replay
def all_playthroughs_after_that():
    user_guess.clear()
    check_if_won.clear()

# plays game
for word in words:
    playernameused = makes_name()
    if playernameused == '':
        first_playthrough()
    elif len(played_words) != 0:
        all_playthroughs_after_that()
    word = psuedo_random()
    win_lose()