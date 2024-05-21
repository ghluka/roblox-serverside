import getpass
import os
import pickle

from utils.inputs import PATH, bool_input


def get_cookie() -> str:
    while True:
        try:
            try:
                with open(f"{PATH}/cookie.pkl", "rb") as file:
                    print("Loading saved cookie...")
                    cookie = pickle.load(file)
            except FileNotFoundError:
                cookie = getpass.getpass("Enter your Roblox cookie: ")
            
            if not os.path.exists(f"{PATH}/cookie.pkl") and bool_input("Remember cookie?", False):
                with open(f"{PATH}/cookie.pkl", "wb") as file:
                    pickle.dump(cookie, file)
            
            break
        except KeyboardInterrupt:
            exit()
    
    return cookie