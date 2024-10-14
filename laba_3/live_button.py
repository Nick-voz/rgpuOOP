from random import randint
from tkinter import BOTTOM
from tkinter import Canvas
from tkinter import Tk
from tkinter.constants import LEFT
from tkinter.ttk import Frame
from typing import Callable

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


def set_up_app(frame: Frame):
    root = frame
    root.winfo_toplevel().title("Live Button")
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


def set_up_live_button(root: Frame, callback: Callable):
    for widget in root.winfo_children():
        widget.pack_forget()
    set_up_app(root)
    Button(root, text="Back", command=callback).pack(side=BOTTOM)


if __name__ == "__main__":
    root = Tk()
    frame = Frame(root)
    frame.pack()
    set_up_app(frame)
    root.mainloop()
