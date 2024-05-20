import getpass
import os
import pickle

from utils.inputs import bool_input


def get_cookie() -> str:
    while True:
        try:
            try:
                with open("cookie.pkl", "rb") as file:
                    print("Loading saved cookie...")
                    cookie = pickle.load(file)
            except FileNotFoundError:
                cookie = getpass.getpass("Enter your Roblox cookie: ")
            
            if not os.path.exists("cookie.pkl") and bool_input("Remember cookie?", False):
                with open("cookie.pkl", "wb") as file:
                    pickle.dump(cookie, file)
            
            break
        except KeyboardInterrupt:
            exit()
    
    return cookie