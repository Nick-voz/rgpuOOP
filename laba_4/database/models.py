from sqlalchemy import Boolean
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from laba_4.database.base import Base
from laba_4.database.base import engine


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(length=50))

    students: Mapped[list["Student"]] = relationship(back_populates="group")

    def __repr__(self):
        return f"<Group(id={self.id}, name='{self.name}')>"

    def __str__(self):
        return self.name


class Topic(Base):
    __tablename__ = "topics"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String())

    exam_questions: Mapped[list["ExamQuestion"]] = relationship(
        "ExamQuestion", back_populates="topic"
    )
    exams: Mapped[list["Exam"]] = relationship("Exam", back_populates="topic")

    def __repr__(self):
        return f"<Topic(id={self.id}, name='{self.name}')>"

    def __str__(self):
        return self.name


class Faculty(Base):
    __tablename__ = "faculties"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(length=50))

    students: Mapped[list["Student"]] = relationship(back_populates="faculty")

    def __repr__(self):
        return f"<Faculty(id={self.id}, name='{self.name}')>"

    def __str__(self):
        return self.name


class Subject(Base):
    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String())

    exam_questions: Mapped[list["ExamQuestion"]] = relationship(
        "ExamQuestion", back_populates="subject"
    )

    def __repr__(self):
        return f"<Subject(id={self.id}, name='{self.name}')>"

    def __str__(self):
        return self.name


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(length=50), unique=True)
    second_name: Mapped[str] = mapped_column(String(length=50), nullable=True)
    surname: Mapped[str] = mapped_column(String(length=50), nullable=True)
    group_id: Mapped[int] = mapped_column(
        ForeignKey("groups.id"), nullable=True
    )
    faculty_id: Mapped[int] = mapped_column(
        ForeignKey("faculties.id"), nullable=True
    )

    group: Mapped["Group"] = relationship(back_populates="students")
    faculty: Mapped["Faculty"] = relationship(back_populates="students")
    exams: Mapped[list["Exam"]] = relationship(
        "Exam", back_populates="student"
    )
    responses: Mapped[list["StudentResponses"]] = relationship(
        "StudentResponses", back_populates="student"
    )

    def __repr__(self):
        res = (
            f"<Student(id={self.id}, name='{self.name}', "
            + f"surname='{self.surname}')>"
        )
        return res

    def __str__(self):
        return f"{self.name} {self.surname} {self.second_name or ''}".strip()


class Exam(Base):
    __tablename__ = "exams"

    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))
    topic_id: Mapped[int] = mapped_column(ForeignKey("topics.id"))
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"))

    student: Mapped["Student"] = relationship(
        "Student", back_populates="exams"
    )
    topic: Mapped["Topic"] = relationship("Topic", back_populates="exams")
    subject: Mapped["Subject"] = relationship("Subject")

    def __repr__(self):
        return (
            f"<Exam(id={self.id}, student_id={self.student_id}, "
            + f"topic_id={self.topic_id})>"
        )

    def __str__(self):
        return f"Exam {self.id} for Student {self.student_id}"


class StudentResponses(Base):
    __tablename__ = "student_responses"

    id: Mapped[int] = mapped_column(primary_key=True)
    answer_id: Mapped[int] = mapped_column(
        ForeignKey("exam_question_answers.id")
    )
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))

    answer: Mapped["ExamQuestionAnswers"] = relationship("ExamQuestionAnswers")
    student: Mapped["Student"] = relationship(
        "Student", back_populates="responses"
    )

    def __repr__(self):
        return (
            f"<StudentResponse(id={self.id}, student_id={self.student_id}, "
            + f"answer_id={self.answer_id})>"
        )

    def __str__(self):
        return (
            f"Response by Student {self.student_id}, Answer {self.answer_id}"
        )


class ExamQuestion(Base):
    __tablename__ = "exam_questions"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(length=150))
    topic_id: Mapped[int] = mapped_column(ForeignKey("topics.id"))
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"))

    topic: Mapped["Topic"] = relationship(
        "Topic", back_populates="exam_questions"
    )
    subject: Mapped["Subject"] = relationship(
        "Subject", back_populates="exam_questions"
    )
    answers: Mapped[list["ExamQuestionAnswers"]] = relationship(
        "ExamQuestionAnswers", back_populates="question"
    )

    def __repr__(self):
        return f"<ExamQuestion(id={self.id}, text='{self.text[:20]}...')>"

    def __str__(self):
        return self.text


class ExamQuestionAnswers(Base):
    __tablename__ = "exam_question_answers"

    id: Mapped[int] = mapped_column(primary_key=True)
    question_id: Mapped[int] = mapped_column(
        ForeignKey("exam_questions.id"), nullable=False
    )
    text: Mapped[str] = mapped_column(String(length=100))
    is_correct: Mapped[bool] = mapped_column(Boolean())

    question: Mapped["ExamQuestion"] = relationship(
        "ExamQuestion", back_populates="answers"
    )

    def __repr__(self):
        return (
            f"<ExamQuestionAnswer(id={self.id}, text='{self.text[:20]}...', "
            + f"is_correct={self.is_correct})>"
        )

    def __str__(self):
        return self.text


Base.metadata.create_all(engine)
