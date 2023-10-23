from time import sleep  # import sleep from time, to add cooldowns
from keyboard import press_and_release, is_pressed  # simulate control+r presses
from webbrowser import open  # for opening the namemc profile in a browser
from colorama import Fore, init
from utils import *

init()  # activate colorama
ign = None  # ign will later be stored in this variable

# have user choose between random generation mode, or namemc art mode
print(
    f"{Fore.YELLOW}Would you like to apply NameMC Skin Art?{Fore.CYAN}[y/n]{Fore.YELLOW}"
)
while True:
    mode = input("> ").lower()
    if mode in ["y"]:
        print()
        break
    else:
        print(
            f"{Fore.YELLOW}Would you like to apply NameMC Skin Art?{Fore.CYAN}[y/n]{Fore.YELLOW}"
        )

# prompt user for account's email
print(f"{Fore.YELLOW}Input your account's email{Fore.GREEN}")
while True:
    email = input("> ")
    if "@" in email:  # make sure it's a real email
        print()
        break
    else:  # if it isn't, have them try again
        print(f"{Fore.RED}Make sure to enter a valid email!{Fore.GREEN}")

# prompt user for account's password
print(f"{Fore.YELLOW}Input your account's password{Fore.GREEN}")
password = input("> ")
print()

# prompt user for the style of the skins
# ("slim" or "classic")
print(
    f'{Fore.YELLOW}Input the style of the skins ({Fore.CYAN}"slim"{Fore.YELLOW} or {Fore.CYAN}"classic"{Fore.YELLOW}){Fore.GREEN}'
)
while True:
    style = input("> ")
    if style in ["slim", "classic"]:
        print()
        break
    else:
        # if it isn't, have them try again
        print(
            f'{Fore.RED}Please try again, the options are {Fore.CYAN}"slim"{Fore.RED} or {Fore.CYAN}"classic"{Fore.RED}.{Fore.GREEN}'
        )

# confirm the user's choices
print(
    f'{Fore.YELLOW}Setting up auto-apply bot with email {Fore.CYAN}"{email}"{Fore.YELLOW}...\n'
)

# user is applying NameMc art
if mode == "y":
    print(f"{Fore.YELLOW}Would you like the bot to apply your skins? (y/n){Fore.GREEN}")
    apply_skins = input("> ").lower()
    while True:
        if apply_skins == "n":
            apply_skins = False
            break
        elif apply_skins == "y":
            apply_skins_warn()
            apply_skins = True
            break
        else:
            print(
                f'{Fore.RED}Make sure to only enter {Fore.CYAN}"y"{Fore.RED} or {Fore.CYAN}"n"{Fore.GREEN}'
            )

    if apply_skins:
        bearer, ign = auth(email, password)  # obtain a bearer
        print()

        # open the namemc profile in a new window, and bring it to the top of the screen
        open("http://namemc.com/profile/" + ign.lower(), new=1, autoraise=True)

        if mode == "y":
            for skin in range(27, 0, -1):

                changeSkin(
                    style, "output/" + str(skin), bearer
                )  # use bearer to change skin

                # print status message once skin has been changed
                print(
                    f"{Fore.GREEN}Skin {Fore.CYAN}{str(skin)}{Fore.GREEN} applied successfully"
                )

                interruptible_sleep(
                    25
                )  # sleep for 3 seconds, but make it so the user can break the sleep cleanly

                # reload tab
                press_and_release("control+r")

                # print statusu message once tab is reloaded
                print(
                    f"{Fore.GREEN}Skin {Fore.CYAN}{str(skin)}{Fore.GREEN} cached on NameMC successfully"
                )

                interruptible_sleep(
                    10
                )  # sleep for 3 seconds, but make it so the user can break the sleep cleanly

    else:
        print(
            f"{Fore.YELLOW}To manually apply skins, make sure to apply from 27 down, and make sure to reload the NameMC profile so they cache.{Fore.GREEN}"
        )
        print(f"{Fore.YELLOW}Program will close in 5 seconds...")
        sleep(5)
        print(f"{Fore.RED}Exiting...")
        exit()

