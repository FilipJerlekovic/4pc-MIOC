from tkinter import *
import time

# frame delay = 0.1 s


def explode(startX, startY):
    frame = Toplevel()
    frame.geometry(f"300x300+{startX}+{startY}")
    frames = []
    for i in range(1, 18):
        frames.append(PhotoImage(file = f".\\Explosion\\frame{i}.gif"))
        frames[-1] = frames[-1].zoom(x=3,y=3)    

    label = Label(frame, image=frames[0], height=300, width=300)
    label.grid()
    label.place(x=150, y=150, anchor="center")
    for i in range(0, 17):
        time.sleep(0.1)
        label.config(image=frames[i])
        frame.update()
    frame.destroy()