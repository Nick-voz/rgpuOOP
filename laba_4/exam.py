import json
from collections.abc import Generator
from tkinter import IntVar
from tkinter import Tk
from tkinter.constants import TOP
from tkinter.ttk import Frame
from tkinter.ttk import Label
from typing import List

from pydantic import BaseModel
from pydantic import ValidationError

from tkinter_extended.focus_sensitive_elems import Button
from tkinter_extended.focus_sensitive_elems import Radiobutton
from tkinter_extended.labeled_entry import LabeledEntryField
from tkinter_extended.set_up_util import clear_frame

student_name: str = ""
responses: list["Answer"] = []
GUESTIONS_FILE_PATH = "questions.json"


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
        return (q for q in questions)

    return (q for q in sample_questions)


def show_res(frame: Frame) -> None:
    frame.winfo_toplevel().geometry("250x250")
    frame = clear_frame(frame)
    correct_answers = [e for e in responses if e.is_correct is True]
    num_correct = len(correct_answers)
    num_all = len(responses)
    score = f"{num_correct} / {num_all}"
    label_name = Label(frame, text=student_name)
    label_name.pack()
    label = Label(frame, text=score)
    label.pack()


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

    frame_button = Frame(root)
    frame_button.pack()

    button_start_test = Button(
        frame_button,
        text="Start exam",
        command=lambda: start_exam(root, entry_name.get()),
    )
    button_start_test.pack()

    return root


if __name__ == "__main__":
    app = Tk()
    frame = Frame(app)
    frame.pack()
    set_up_menu(frame)
    app.mainloop()
