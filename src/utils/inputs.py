import pathlib
import tkinter as tk
from tkinter import filedialog

PATH = pathlib.Path(__file__).parent.parent.resolve()

TOS_VERSION = 1


def select_rbxmx() -> str:
    """Opens a file dialog to select a Roblox XML model file."""
    root = tk.Tk()
    root.wm_attributes("-topmost", 1)
    root.withdraw()

    file = filedialog.askopenfilename(
        initialdir=PATH / "presets", filetypes=[("Roblox XML Model Files", "*.rbxmx")]
    )

    if not file:
        exit()

    return file


def bool_input(input_prompt: str, default: bool = True) -> bool:
    """Prompts the user for a boolean input with a default option."""
    input_str = (
        input(f"{input_prompt} ({'Y/n' if default else 'y/N'}): ").strip().lower()
    )

    if input_str.startswith("y"):
        return True
    if input_str.startswith("n"):
        return False

    return default
