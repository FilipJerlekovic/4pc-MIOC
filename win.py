from tkinter import *
from PIL import Image, ImageTk



def win(boja):
    frame = Toplevel()
    boje = ["#ff0008", "#00d100", "#ebe700", "#111d74"]
    magnoos = Image.open(f'.\\Widgets\\{["miocnus crven", "miocnus zelen", "miocnus zut", "miocnus plav"][boja]}.png')
    magnoosy = magnoos.resize((700, 700))
    magnoosius = ImageTk.PhotoImage(magnoosy)
    l1 = Label(frame, text = "Pobjeda!", fg = boje[boja], font = ("Courier New bold", 20))
    l1.grid(column = 0, row = 1)
    l2 = Label(frame, image = magnoosius, width = 700, height = 700)
    l2.grid(column = 0, row = 2)
    frame.mainloop()

if __name__ == "__main__":
    win(3)