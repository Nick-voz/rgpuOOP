import json
from tkinter import Tk
from tkinter.ttk import Combobox
from tkinter.ttk import Frame
from tkinter.ttk import LabelFrame

from pydantic import BaseModel
from pydantic import PositiveInt
from pydantic import TypeAdapter

from tkinter_extended.set_up_util import clear_frame

STUDENTS_FILE_PATH = (
    "/Users/nikitavozisow/projects/rgpuOOP/laba_4/students.json"
)


class Student(BaseModel):
    name: str
    faculty: str
    course: PositiveInt
    group: PositiveInt
    marks: list["Mark"]


class Mark(BaseModel):
    subject_name: str
    mark: PositiveInt


def load_students_from_file(file_path: str) -> list["Student"]:
    with open(file_path, "r", encoding="utf8") as f:
        data = json.load(f)
    students = TypeAdapter(list["Student"]).validate_python(data)
    return students


def filter_unique_students(students: list["Student"]) -> list["Student"]:
    names = set()
    res: list["Student"] = []
    for e in students:
        if e.name in names:
            continue
        names.add(e.name)
        res.append(e)
    return res


def write_students_in_file(file_path: str, students: list["Student"]):
    old_students: list["Student"] = load_students_from_file(file_path)
    filtered_students = filter_unique_students(old_students + students)

    students_json = TypeAdapter(list["Student"]).dump_json(
        filtered_students, indent=2
    )

    with open(file_path, "bw") as f:
        f.write(students_json)


def get_student(file_path: str, name) -> Student | None:
    studets = load_students_from_file(file_path)
    return next((s for s in studets if s.name == name), None)


def save_student(file_path: str, student: Student) -> None:
    students = load_students_from_file(file_path)
    students.append(student)
    write_students_in_file(file_path, students)


class UI:
    def __init__(self, frame: Frame, students_file_path: str) -> None:
        self.frame: Frame = frame
        self.frame.pack()
        self.students_file_path = students_file_path
        self.students: list["Student"] = load_students_from_file(
            self.students_file_path
        )
        self.show_main_window()
        self.current_student: Student

    def show_main_window(self) -> None:
        clear_frame(self.frame)
        self.students_selector: Combobox = Combobox(
            self.frame, values=[s.name for s in self.students]
        )
        self.students_selector.pack()

    def on_select(self) -> None:
        self.current_student = self.students[0]

    def show_student(self) -> None:

        card = LabelFrame(
            self.frame, text=f"Student: {self.current_student.name}"
        )
        card.pack()


def main():
 sssroot = Tk()
    frame = Frame(root)
    UI(frame, STUDENTS_FILE_PATH)
    root.mainloop()


if __name__ == "__main__":
    main()
