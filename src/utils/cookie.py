# import getpass
import os
import pickle

from utils.inputs import PATH


def get_cookie() -> str:
    """Retrieves the Roblox cookie, prompting the user if not found."""
    cookie_path = f"{PATH}/cookie.pkl"

    try:
        if os.path.exists(cookie_path):
            with open(cookie_path, "rb") as file:
                print("Loading saved cookie...")
                return pickle.load(file)

        cookie = ""  # getpass.getpass("Enter your Roblox cookie: ")
        # if bool_input("Remember cookie?", False):
        # with open(cookie_path, "wb") as file:
        #    pickle.dump(cookie, file)

        return cookie
    except KeyboardInterrupt:
        exit()
