import json
from collections.abc import Callable
from tkinter import Label
from tkinter import Tk
from tkinter.constants import BOTTOM
from tkinter.constants import TOP
from tkinter.ttk import Button
from tkinter.ttk import Combobox
from tkinter.ttk import Frame
from tkinter.ttk import Labelframe

from pydantic import BaseModel
from pydantic import PositiveInt
from pydantic import TypeAdapter

from tkinter_extended.labeled_entry import LabeledEntryField
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
    filtered_students = filter_unique_students(students + old_students)

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


def update_student(file_path: str, student: Student) -> None:
    students = load_students_from_file(file_path)
    students = [s for s in students if s.name != student.name]
    students.append(student)
    students_json = TypeAdapter(list["Student"]).dump_json(students, indent=2)

    with open(file_path, "bw") as f:
        f.write(students_json)


class StudentSelector:
    def __init__(
        self,
        frame: Frame,
        students: list["Student"],
        callback: Callable[["Student"], None],
    ) -> None:

        self.frame = frame
        self.callback = callback
        self.students = students
        self.selector: Combobox = Combobox(
            self.frame, values=[s.name for s in self.students]
        )
        self.selector.bind("<<ComboboxSelected>>", lambda _: self.on_select())

    def on_select(self) -> None:
        name = self.selector.get()
        student = next(e for e in self.students if e.name == name)
        self.callback(student)

    def pack(self, **kwargs) -> None:
        self.selector.pack()
        self.frame.pack(**kwargs)


def show_student_card(frame, student: Student) -> None:

    card = Labelframe(frame, text="Student card")
    card.pack()
    bio = Labelframe(card, text="BIO")
    bio.pack()

    labels = (
        ("Name", student.name),
        ("Faculty", student.faculty),
        ("Course", student.course),
        ("Group", student.group),
    )
    for name, value in labels:
        label = Label(bio, text=f"{name}: {value}")
        label.pack(side=TOP, anchor="w")

    marks = Labelframe(card, text="marks")
    marks.pack()

    for e in student.marks:
        label = Label(marks, text=f"{e.subject_name}: {e.mark}")
        label.pack(side=TOP, anchor="w")


class StudentNew:
    def __init__(
        self, frame: Frame, callback: Callable, students_file_path
    ) -> None:
        name = LabeledEntryField(frame, label_text="Name", placeholder="")
        faculty = LabeledEntryField(
            frame, label_text="Faculty", placeholder=""
        )

        group = LabeledEntryField(frame, label_text="Grouop", placeholder="")
        course = LabeledEntryField(frame, label_text="Course", placeholder="")

        name.pack()
        faculty.pack()
        group.pack()
        course.pack()

        def submit() -> None:
            student = Student(
                name=name.get(),
                faculty=faculty.get(),
                group=int(group.get()),
                course=int(course.get()),
                marks=[],
            )
            save_student(students_file_path, student)
            clear_frame(frame)
            callback()

        button_submit = Button(frame, text="Sumbit", command=submit)
        button_submit.pack(side=BOTTOM)


def show_add_mark(
    frame: Frame, callback: Callable, student: Student, students_file_path
) -> None:
    frame.pack()
    subbject_name = LabeledEntryField(
        frame, label_text="Subject", placeholder="Computer science"
    )
    subbject_name.pack()
    mark = LabeledEntryField(frame, label_text="mark", placeholder="1")
    mark.pack()

    def submit() -> None:
        student.marks.append(
            Mark(subject_name=subbject_name.get(), mark=int(mark.get()))
        )
        update_student(students_file_path, student)
        clear_frame(frame)
        callback()

    button_submit = Button(frame, text="Sumbit", command=submit)
    button_submit.pack(side=BOTTOM)


class RootUI:
    def __init__(self, frame: Frame, students_file_path: str) -> None:
        self.frame: Frame = frame
        self.students_file_path = students_file_path
        self.students: list["Student"] = load_students_from_file(
            self.students_file_path
        )
        self.selector_frame = Frame(self.frame)
        self.info_frame = Frame(self.frame)
        self.init_selector()
        self.button_new_student = Button(
            frame, text="add student", command=self.add_student
        )
        self.button_new_student.pack()
        self.button_add_mark = Button(
            frame, text="add mark", command=self.add_mark
        )
        self.button_add_mark.pack()

    def add_student(self) -> None:
        self.frame = clear_frame(self.frame)
        StudentNew(
            self.frame,
            callback=lambda: self.__init__(
                self.frame, self.students_file_path
            ),
            students_file_path=self.students_file_path,
        )

    def on_select(self, student: Student) -> None:
        self.info_frame = clear_frame(self.info_frame)
        self.current_student = student
        self.show_student()

    def show_student(self) -> None:
        show_student_card(frame=self.info_frame, student=self.current_student)
        self.info_frame.pack()

    def add_mark(self) -> None:
        self.frame = clear_frame(self.frame)
        show_add_mark(
            frame=self.frame,
            student=self.current_student,
            students_file_path=self.students_file_path,
            callback=lambda: self.__init__(
                self.frame, self.students_file_path
            ),
        )

    def init_selector(self) -> None:
        self.selector = StudentSelector(
            self.selector_frame, self.students, self.on_select
        )
        self.selector.pack()


def set_up_student_card(root: Frame, callback: Callable):
    clear_frame(root)
    frame = Frame(root)
    frame.pack()
    RootUI(frame, STUDENTS_FILE_PATH)
    Button(root, text="Back", command=callback).pack(side=BOTTOM)


def main():
    root = Tk()
    frame = Frame(root)
    frame.pack()
    RootUI(frame, STUDENTS_FILE_PATH)
    root.mainloop()


if __name__ == "__main__":
    main()
