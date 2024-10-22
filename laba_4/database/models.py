from sqlalchemy import Boolean
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from laba_4.database.base import Base
from laba_4.database.base import engine


class Group(Base):
    """
    The `Group` class maps to the "groups" table in the database.

    Attributes:
        id (int): The unique identifier of the group. Primary key.
        name (str): The name of the group. Limited to 50 characters.
        students (list[Student]): A list of students that belong to this group.
            This relationship is bi-directional, with the `Student`
            class having a corresponding `group` attribute.
    """

    __tablename__ = "groups"

    # fields
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(length=50))

    # relationships
    students: Mapped[list["Student"]] = relationship(back_populates="group")

    def __repr__(self):
        return f"<Group(id={self.id}, name='{self.name}')>"

    def __str__(self):
        return self.name


class Topic(Base):
    """
    Represents a topic in an educational curriculum.

    The `Topic` class maps to the "topics" table in the database and
    is associated with various exam questions
    and exams related to the subject matter.

    Attributes:
        id (int): The unique identifier for each topic. Primary key.
        name (str): The name of the topic.

        exam_questions (list[ExamQuestion]): A list of exam questions
            associated with this topic. This relationship is bi-directional
            with the `ExamQuestion` class having a corresponding
            `topic` attribute.
        exams (list[Exam]): A list of exams that relate to this topic, with the
            `Exam` class having a corresponding `topic` attribute.
    """

    __tablename__ = "topics"

    # fields
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String())

    # relationships
    exam_questions: Mapped[list["ExamQuestion"]] = relationship(
        "ExamQuestion", back_populates="topic"
    )
    exams: Mapped[list["Exam"]] = relationship("Exam", back_populates="topic")

    def __repr__(self):
        return f"<Topic(id={self.id}, name='{self.name}')>"

    def __str__(self):
        return self.name


class Faculty(Base):
    """
    Represents a faculty within an educational institution.

    The `Faculty` class maps to the "faculties" table in the database and
    contains information regarding the faculty
    and its relationship with students.

    Attributes:
        id (int): Unique identifier for the faculty. Primary key.
        name (str): The name of the faculty. Limited to 50 characters.

        students (list[Student]): A list of students enrolled in this faculty.
            This relationship is bi-directional, with the `Student` class
            having a corresponding `faculty` attribute.
    """

    __tablename__ = "faculties"

    # fields
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(length=50))

    # relationships
    students: Mapped[list["Student"]] = relationship(back_populates="faculty")

    def __repr__(self):
        return f"<Faculty(id={self.id}, name='{self.name}')>"

    def __str__(self):
        return self.name


class Subject(Base):
    """
    Represents a subject taught within an educational institution.

    The `Subject` class maps to the "subjects" table in the database
    and manages information regarding the subjects offered
    and their associated exam questions.

    Attributes:
        id (int): Unique identifier for the subject. Primary key.
        name (str): The name of the subject.

        exam_questions (list[ExamQuestion]): A list of exam questions linked to
            this subject. This relationship is bi-directional, with the
            `ExamQuestion` class having a corresponding `subject` attribute.
    """

    __tablename__ = "subjects"

    # fields
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String())

    # relationships
    exam_questions: Mapped[list["ExamQuestion"]] = relationship(
        "ExamQuestion", back_populates="subject"
    )

    def __repr__(self):
        return f"<Subject(id={self.id}, name='{self.name}')>"

    def __str__(self):
        return self.name


class Student(Base):
    """
    Represents a student enrolled in an educational institution.

    The `Student` class maps to the "students" table in the database
    and contains personal details of each student along with their
    relationships to groups, faculties, exams,
    and their responses to exam questions.

    Attributes:
        id (int): Unique identifier for the student. Primary key.
        name (str): The first name of the student. Must be unique.
        second_name (str): The second name of the student (optional).
        surname (str): The surname of the student (optional).
        group_id (int): Foreign key referencing the group
            to which the student belongs.
        faculty_id (int): Foreign key referencing the faculty
            to which the student belongs.

        group (Group): A reference to the Group instance
            that contains this student.
        faculty (Faculty): A reference to the Faculty instance
            associated with this student.
        exams (list[Exam]): A list of exams taken by the student.
        responses (list[StudentResponses]): A list of responses given by
            the student.
    """

    __tablename__ = "students"

    # fields
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

    # relationships
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
    """
    Represents an exam taken by a student for assessment purposes.

    The `Exam` class maps to the "exams" table in the database
    and contains details about the assessment,
    including the student taking the exam and the relevant topic and subject.

    Attributes:
        id (int): Unique identifier for the exam. Primary key.
        student_id (int): Foreign key referencing the student taking the exam.
        topic_id (int): Foreign key referencing the topic of the exam.
        subject_id (int): Foreign key referencing the subject of the exam.

        student (Student): A reference to
            the Student instance taking this exam.
        topic (Topic): A reference to the Topic instance related to the exam.
        subject (Subject): A reference to
            the Subject instance related to the exam.
    """

    __tablename__ = "exams"

    # fields
    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))
    topic_id: Mapped[int] = mapped_column(ForeignKey("topics.id"))
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"))

    # relationships
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
    """
    Represents the responses given by students to exam questions.

    The `StudentResponses` class maps to the "student_responses" table in the
    database and manages the relationship between students and their answers
    to exam questions.

    Attributes:
        id (int): Unique identifier for the student response. Primary key.
        answer_id (int): Foreign key
            referencing the answer given to an exam question.
        student_id (int): Foreign key
            referencing the student giving the response.

        answer (ExamQuestionAnswers): A reference to the
            ExamQuestionAnswers instance
            related to this response.
        student (Student): A reference to the
            Student instance that made the response.
    """

    __tablename__ = "student_responses"

    # fields
    id: Mapped[int] = mapped_column(primary_key=True)
    answer_id: Mapped[int] = mapped_column(
        ForeignKey("exam_question_answers.id")
    )
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))

    # relationships
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
    """
    Represents questions included in exams.

    The `ExamQuestion` class maps to the "exam_questions" table in the database
    and contains details regarding the exam questions,
    including their relationship with topics, subjects, and possible answers.

    Attributes:
        id (int): Unique identifier for the exam question. Primary key.
        text (str): The text of the exam question. Limited to 150 characters.
        topic_id (int): Foreign key
            referencing the topic to which the question belongs.
        subject_id (int): Foreign key
            referencing the subject associated with the question.

        topic (Topic): A reference to the Topic instance
            related to this exam question.
        subject (Subject): A reference to the Subject instance
            related to this exam question.
        answers (list[ExamQuestionAnswers]): A list of possible answers for
            this question.
    """

    __tablename__ = "exam_questions"

    # fields
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(length=150))
    topic_id: Mapped[int] = mapped_column(ForeignKey("topics.id"))
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"))

    # relationships
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
    """
    Represents possible answers to exam questions.

    The `ExamQuestionAnswers` class maps to the "exam_question_answers" table
    in the database and contains the text of the answers
    and whether they are correct.

    Attributes:
        id (int): Unique identifier for the answer. Primary key.
        question_id (int): Foreign key referencing the question to which the
            answer belongs.
        text (str): The text of the answer. Limited to 100 characters.
        is_correct (bool): A boolean flag indicating if the answer is correct.

        question (ExamQuestion): A reference to the ExamQuestion instance
            related to this answer.
    """

    __tablename__ = "exam_question_answers"

    # fields
    id: Mapped[int] = mapped_column(primary_key=True)
    question_id: Mapped[int] = mapped_column(
        ForeignKey("exam_questions.id"), nullable=False
    )
    text: Mapped[str] = mapped_column(String(length=100))
    is_correct: Mapped[bool] = mapped_column(Boolean())

    # relationships
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
