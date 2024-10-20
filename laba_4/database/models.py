from base import Base
from base import engine
from sqlalchemy import Boolean
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(length=50))

    students: Mapped[list["Student"]] = relationship(back_populates="group")


class Topic(Base):
    __tablename__ = "topics"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String())

    test_questions: Mapped[list["TestQuestion"]] = relationship(
        "TestQuestion", back_populates="topic"
    )
    tests: Mapped[list["Test"]] = relationship("Test", back_populates="topic")


class Faculty(Base):
    __tablename__ = "faculties"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(length=50))

    students: Mapped[list["Student"]] = relationship(back_populates="faculty")


class Subject(Base):
    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String())

    test_questions: Mapped[list["TestQuestion"]] = relationship(
        "TestQuestion", back_populates="subject"
    )


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(length=50))
    second_name: Mapped[str] = mapped_column(String(length=50))
    surname: Mapped[str] = mapped_column(String(length=50))
    group_id: Mapped[int] = mapped_column(
        ForeignKey("groups.id"), nullable=True
    )
    faculty_id: Mapped[int] = mapped_column(
        ForeignKey("faculties.id"), nullable=True
    )

    group: Mapped["Group"] = relationship(back_populates="students")
    faculty: Mapped["Faculty"] = relationship(back_populates="students")
    tests: Mapped[list["Test"]] = relationship(
        "Test", back_populates="student"
    )
    responses: Mapped[list["StudentResponses"]] = relationship(
        "StudentResponses", back_populates="student"
    )


class Test(Base):
    __tablename__ = "tests"

    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))
    topic_id: Mapped[int] = mapped_column(ForeignKey("topics.id"))
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"))

    student: Mapped["Student"] = relationship(
        "Student", back_populates="tests"
    )
    topic: Mapped["Topic"] = relationship("Topic", back_populates="tests")
    subject: Mapped["Subject"] = relationship("Subject")


class StudentResponses(Base):
    __tablename__ = "student_responses"

    id: Mapped[int] = mapped_column(primary_key=True)
    answer_id: Mapped[int] = mapped_column(
        ForeignKey("test_question_answers.id")
    )
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))

    answer: Mapped["TestQuestionAnswers"] = relationship("TestQuestionAnswers")
    student: Mapped["Student"] = relationship(
        "Student", back_populates="responses"
    )


class TestQuestion(Base):
    __tablename__ = "test_questions"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(length=150))
    topic_id: Mapped[int] = mapped_column(ForeignKey("topics.id"))
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"))

    topic: Mapped["Topic"] = relationship(
        "Topic", back_populates="test_questions"
    )
    subject: Mapped["Subject"] = relationship(
        "Subject", back_populates="test_questions"
    )
    answers: Mapped[list["TestQuestionAnswers"]] = relationship(
        "TestQuestionAnswers", back_populates="question"
    )


class TestQuestionAnswers(Base):
    __tablename__ = "test_question_answers"

    id: Mapped[int] = mapped_column(primary_key=True)
    question_id: Mapped[int] = mapped_column(
        ForeignKey("test_questions.id"), nullable=False
    )
    text: Mapped[str] = mapped_column(String(length=100))
    is_correct: Mapped[bool] = mapped_column(Boolean())

    question: Mapped["TestQuestion"] = relationship(
        "TestQuestion", back_populates="answers"
    )


Base.metadata.create_all(engine)
