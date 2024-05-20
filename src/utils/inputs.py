import pathlib
import tkinter as tk
from tkinter import filedialog

PATH = pathlib.Path(__file__).parent.parent.resolve()

def select_rbxmx() -> str:
    root = tk.Tk()
    root.wm_attributes('-topmost', 1)
    root.withdraw()

    file = filedialog.askopenfilename(
        initialdir=f"{PATH}/presets",
        filetypes=[("Roblox XML Model Files", "*.rbxmx")]
    )
    if not file:
        exit()
    
    return file

def bool_input(input_prompt:str, default:bool=True) -> bool:
    input_str:str = input(input_prompt + f" ({'Y/n' if default else 'y/N'}): ")

    if input_str.lower().startswith("y"):
        return True
        
    elif input_str.lower().startswith("n"):
        return False
    
    return default