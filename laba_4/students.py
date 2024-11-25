import json

from pydantic import BaseModel
from pydantic import PositiveInt
from pydantic import TypeAdapter

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
    combined_students = old_students + students
    filtered_students = filter_unique_students(combined_students)

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


def main():
    tmp = load_students_from_file(STUDENTS_FILE_PATH)
    write_students_in_file(STUDENTS_FILE_PATH, tmp)
    print("load example: ", tmp)
    student = get_student(STUDENTS_FILE_PATH, "exmaple name")
    print("get example: ", student)
    # s = Student(
    #     name="example 3 name",
    #     faculty="examle faculty",
    #     course=1,
    #     group=1,
    #     marks=[
    #         Mark(subject_name="math", mark=5),
    #         Mark(subject_name="computer science", mark=5),
    #     ],
    # )
    # save_student(STUDENTS_FILE_PATH, s)


if __name__ == "__main__":
    main()
