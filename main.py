from time import sleep
from webbrowser import open as webbrowser_open
from requests import post, get
from random import randrange
import pyautogui # type: ignore

# changeskin function to upload skins from the skinart folder
def changeSkin(style, skin_name, bearer):
    current_png = open(f"skinart/{skin_name}.png", "rb")  # open the skin file in binary mode

    # files header for the request to change skin
    files = {
        "variant": (None, style),
        "file": (f"{skin_name}.png", current_png),
    }

    # auth header for the request to change skin
    headers = {"Authorization": "Bearer " + bearer}

    # make request, and if it's successful move on, or try again (max 3 attempts)
    attempt = 0
    while True:
        req = post(
            url="https://api.minecraftservices.com/minecraft/profile/skins",
            headers=headers,
            files=files,
        ).status_code
        if req == 200:
            break  # skin change succeeded, so break
        else:
            if attempt >= 3:
                print("Error changing skin")
                break
            sleep(3)
        attempt += 1  # upon fail, increase attempt counter

    current_png.close()  # close the png file

# sleep function that can be interrupted
def interruptible_sleep(sleep_time):
    elapsed_time = 0
    while sleep_time > elapsed_time:
        elapsed_time += 0.01
        sleep(0.01)

# function to get Minecraft username using bearer token
def get_minecraft_username(bearer):
    headers = {"Authorization": "Bearer " + bearer}
    response = get("https://api.minecraftservices.com/minecraft/profile", headers=headers)
    if response.status_code == 200:
        return response.json().get("name")
    else:
        print("Error retrieving username. Please check your Bearer token.")
        exit()

# Get Bearer token from user input
bearer = input("Please enter your Bearer token: ")

# Get Minecraft IGN (in-game name) using the Bearer token
ign = get_minecraft_username(bearer)
if ign:
    print(f"Successfully retrieved username: {ign}")

# Ask the user if they want to use slim or classic skins
style = input("Do you want to use 'slim' or 'classic' skins? ").strip().lower()
if style not in ["slim", "classic"]:
    print("Invalid choice, defaulting to 'slim'.")
    style = "slim"

# Display the warning in all caps
warning = input("WARNING: YOU CANNOT USE YOUR PC FOR ABOUT THE NEXT 20 MINUTES DURING THE UPLOAD PROCESS! IF YOU DO, IT MIGHT MESS UP THE SKIN UPLOAD! TYPE 'YES' TO CONFIRM: ").strip().upper()
if warning != "YES":
    print("Upload process aborted. Exiting...")
    exit()

# Automatically apply skins from skinart/Skin-1.png to skinart/Skin-27.png
apply_skins = True

# Confirm the setup
print(f'Setting up auto-apply bot with username "{ign}"...\n')

if apply_skins:
    # Open the NameMC profile in a new window and bring it to the top of the screen
    webbrowser_open(f"http://namemc.com/profile/{ign.lower()}", new=1, autoraise=True)

    # Apply skins from skinart/Skin-1.png to skinart/Skin-27.png
    for skin in range(1, 28):
        changeSkin(style, f"Skin-{skin}", bearer)  # use bearer to change skin

        # Print status message once the skin has been changed
        print(f"Skin {skin} applied successfully")

        interruptible_sleep(30)  # sleep for 30 seconds, allowing the user to interrupt

        # Refresh the browser tab
        pyautogui.hotkey("ctrl", "r")

        # Print status message once tab is refreshed
        print(f"Skin {skin} cached on NameMC successfully")

        interruptible_sleep(15)  # sleep for 15 seconds, allowing the user to interrupt

else:
    print("To manually apply skins, make sure to apply from 1 to 27, and reload the NameMC profile so they cache.\nProgram will close in 5 seconds...")
    sleep(5)
    print("Exiting...")
    exit()
