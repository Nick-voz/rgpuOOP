from random import randint
from tkinter import Canvas
from tkinter import Tk
from tkinter.constants import LEFT
from tkinter.ttk import Frame

from tkinter_extended.focus_sensitive_elems import Button


def create(canvas: Canvas):
    global text_id
    text_id = canvas.create_text(
        125, 100, text="Initial Text", font=("Arial", 14)
    )


def delete(shape, canvas: Canvas):
    canvas.delete(shape)


def update_text(shape: int, canvas: Canvas):
    (x, y, *_) = canvas.coords(shape)
    canvas.itemconfig(shape, text=f"I'm in ({x}, {y})")


def move(shape: int, canvas: Canvas):
    (x0, y0, *_) = canvas.coords(shape)

    x_move = randint(-50, 50)
    y_move = randint(-50, 50)

    canvas_x0 = canvas.winfo_rootx()
    canvas_x1 = canvas_x0 + canvas.winfo_width()
    canvas_y0 = canvas.winfo_rooty()
    canvas_y1 = canvas_y0 + canvas.winfo_height()

    if x0 + x_move <= canvas_x0 or x0 + x_move >= canvas_x1:
        x_move *= -2

    if y0 + y_move <= canvas_y0 or y0 + y_move >= canvas_y1:
        y_move *= -2

    update_text(shape=shape, canvas=canvas)
    canvas.move(shape, x_move, y_move)


root = Tk()
root.title("Live Button")
menu_frame = Frame(root)

button_create = Button(
    menu_frame, text="create", command=lambda: create(canvas=canvas)
)
button_move = Button(
    menu_frame,
    text="move",
    command=lambda: move(shape=text_id, canvas=canvas),
)
button_delete = Button(
    menu_frame,
    text="delete",
    command=lambda: delete(shape=text_id, canvas=canvas),
)

canvas = Canvas(root, width=400, height=400, bg="black")

button_create.pack(side=LEFT)
button_move.pack(side=LEFT)
button_delete.pack(side=LEFT)

menu_frame.pack()

canvas.pack()


if __name__ == "__main__":
    root.mainloop()
