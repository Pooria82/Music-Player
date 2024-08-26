# main.py
from gui import MusicPlayerGUI
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayerGUI(root)
    root.mainloop()
