import json
from collections.abc import Generator
from tkinter import BOTTOM
from tkinter import IntVar
from tkinter import Tk
from tkinter.constants import TOP
from tkinter.ttk import Frame
from tkinter.ttk import Label
from typing import Callable
from typing import List
from typing import TypeVar

import random
from pydantic import BaseModel
from pydantic import ValidationError

from tkinter_extended.focus_sensitive_elems import Button
from tkinter_extended.focus_sensitive_elems import Radiobutton
from tkinter_extended.labeled_entry import LabeledEntryField
from tkinter_extended.set_up_util import clear_frame

T = TypeVar("T")


def shuffle_list(items: List[T]) -> List[T]:
    """Return a new list with elements shuffled in random order."""
    shuffled_items = items[:]
    random.shuffle(shuffled_items)
    return shuffled_items


student_name: str = ""
responses: list["Answer"] = []
GUESTIONS_FILE_PATH = (
    "/Users/nikitavozisow/projects/rgpuOOP/laba_4/questions.json"
)


class Answer(BaseModel):
    text: str
    is_correct: bool


class Question(BaseModel):
    text: str
    answers: List[Answer]


def save_student(name: str) -> None:
    global student_name
    student_name = name


def load_questions() -> Generator["Question"]:
    with open(GUESTIONS_FILE_PATH, "r", encoding="utf8") as file:
        data = json.load(file)
    questions = []
    for q_data in data.get("questions", []):
        try:
            question = Question(**q_data)
            questions.append(question)
        except ValidationError as e:
            print(
                "Validation error for question:",
                f"{q_data['text']}, errors: {e.errors()}",
            )
    questions = shuffle_list(questions)
    return (q for q in questions)


def display_label(frame: Frame, text: str) -> None:
    label = Label(frame, text=text, font=("Helvetica", 14))
    label.pack(pady=5)


def show_res(frame: Frame) -> None:
    frame = clear_frame(frame)

    name_display = f"Student: {student_name}"

    correct_answers = [
        response for response in responses if response.is_correct
    ]

    num_correct = len(correct_answers)
    num_all = len(responses)
    score_display = f"Score: {num_correct} / {num_all}"

    display_label(frame, name_display)
    display_label(frame, score_display)


def show_question(frame: Frame, questions: Generator["Question"]) -> None:
    frame = clear_frame(frame)
    question = next(questions, None)
    if not question:
        show_res(frame)
        return

    question_label = Label(frame, text=question.text, wraplength=300)
    question_label.pack()

    selected_answer_index = IntVar(value=-1)
    for index, ansewr in enumerate(question.answers):
        radion_button = Radiobutton(
            frame,
            text=ansewr.text,
            variable=selected_answer_index,
            value=index,
        )
        radion_button.pack(anchor="w")

    def submit():
        responses.append(question.answers.pop(selected_answer_index.get()))
        show_question(frame, questions)

    submit_button = Button(frame, text="Subit", command=submit)
    submit_button.pack()


def start_exam(frame: Frame, name: str):
    save_student(name)
    questions: Generator["Question"] = load_questions()
    show_question(
        frame,
        questions,
    )


def set_up_menu(root: Frame) -> Frame:
    root.winfo_toplevel().title("Exam")

    frame_menu = Frame(root)
    frame_menu.pack(side=TOP)

    entry_name = LabeledEntryField(frame_menu, label_text="Name: ")
    entry_name.pack()

    frame_button = Frame(root)
    frame_button.pack()

    button_start_test = Button(
        frame_button,
        text="Start exam",
        command=lambda: start_exam(root, entry_name.get()),
    )
    button_start_test.pack()

    return root


def set_up_exam(root: Frame, callback: Callable):
    clear_frame(root)
    frame = Frame(root)
    frame.pack()
    set_up_menu(frame)
    Button(root, text="Back", command=callback).pack(side=BOTTOM)


if __name__ == "__main__":
    app = Tk()
    frame = Frame(app)
    frame.pack()
    set_up_menu(frame)
    app.mainloop()
