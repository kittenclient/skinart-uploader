from colorama import Fore, init
from requests import post
from MsAuth import login
from keyboard import is_pressed
from time import sleep
from PIL import Image
from random import randrange

# activate colorama
init()


def auth(email, password):
    """
    Function to auth a minecraft account

    Args:
        email: email of account
        password: password of account
    """

    try:
        # make a change skin request, and store the data
        authRequest = post(
            "https://authserver.mojang.com/authenticate",
            json={
                "agent": {"name": "Minecraft", "version": 1},
                "username": email,
                "password": password,
            },
        ).json()
        ign = authRequest["selectedProfile"]["name"]
        print(
            f'{Fore.YELLOW}Username was detected to be {Fore.CYAN}"{ign}"{Fore.GREEN}'
        )
        bearer = authRequest["accessToken"]
        return bearer, ign  # return the bearer obtained via the request
    except KeyError:
        authRequest = login(email, password)
        ign = authRequest["username"]
        print(
            f'{Fore.YELLOW}Username was detected to be {Fore.CYAN}"{ign}"{Fore.GREEN}'
        )
        bearer = authRequest["access_token"]

        return bearer, ign


def apply_skins_warn():
    """
    Function to warn user about simulated keystrokes before applying skins
    """

    print(
        f"\n{Fore.YELLOW}Once started, your browswer will open, to cache skins on NameMC"
    )
    print(
        f"{Fore.RED}DO NOT{Fore.YELLOW} USE YOUR PC while the skins are being applied."
    )
    print(f"{Fore.YELLOW}This process will take 15-20 minutes or so.")
    print(f"To stop the program at any point, press control+space\n{Fore.GREEN}")
    input(f"Press [Enter] to start!")

def interruptible_sleep(sleep_time, break_keybind="control+space"):
    """
    check if exit keybind is being held whilst sleeping a given duration
    """
    elapsed_time = 0
    while sleep_time > elapsed_time:
        elapsed_time += 0.01
        sleep(0.01)
        if is_pressed(break_keybind):
            print(f"{Fore.RED}Exiting!{Fore.GREEN}")
            exit()


def changeSkin(style, skin_name, bearer):
    current_png = open(f"{skin_name}.png", "rb")  # open the skin file in binary mode

    # files header for the request to change skin
    files = {
        "variant": (None, style),
        "file": (f"{skin_name}.png", current_png),
    }

    # auth header for the request to change skin
    headers = {"Authorization": "Bearer " + bearer}

    # make request, and if it's successful move on
    # and if it isn't, try again (max 3 attempts)
    attempt = 0
    while True:  # try to change skin 3 times, or break on success
        # req is a variable that stores the status code for a skin change request
        req = post(
            url="https://api.minecraftservices.com/minecraft/profile/skins",
            headers=headers,
            files=files,
        ).status_code
        if req == 200:
            break  # skin change succeded, so break
        else:
            if attempt >= 3:
                print("Error changing skin")
            sleep(3)
        attempt += 1  # upon fail, increase attempt counter

    current_png.close()  # close the png file
