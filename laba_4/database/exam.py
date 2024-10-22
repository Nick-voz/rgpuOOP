from random import sample

from sqlalchemy import Select
from sqlalchemy.orm import Session

from laba_4.database.base import engine
from laba_4.database.models import Exam
from laba_4.database.models import ExamQuestion
from laba_4.database.models import ExamQuestionAnswers
from laba_4.database.models import Student
from laba_4.database.models import StudentResponses
from laba_4.database.models import Subject
from laba_4.database.models import Topic


class ExamFlow:
    def __init__(
        self, topic: str, subject: str, length: int, student_name: str
    ):
        self._topic: Topic = self._find_topic(topic)
        self._subject: Subject = self._find_subjcet(subject)
        self._student: Student = self._find_student(student_name)
        self._length: int = length
        self._questions: list["ExamQuestion"] = self._load_questions()
        self._filter_questions()
        self._load_answers()
        self._exam: Exam = self._init_exam()
        self.__question_index = -1

    def get_next_qustion(self) -> ExamQuestion:
        self.__question_index += 1

        if self.__question_index >= len(self._questions):
            raise StopIteration

        return self._questions[self.__question_index]

    def save_answer(self, answer: ExamQuestionAnswers) -> None:
        response = StudentResponses()
        response.answer = answer
        response.student = self._student
        with Session(engine) as session:
            session.add(response)
            session.commit()

    def _init_exam(self):
        exam = Exam()
        exam.student = self._student
        exam.subject = self._subject
        exam.topic = self._topic

        with Session(engine) as session:
            session.add(exam)
            session.commit()
            exam = session.get(Exam, exam.id)

        return exam

    def _load_answers(self):
        with Session(engine) as session:
            for question in self._questions:
                question = session.get(ExamQuestion, question.id)
                question.answers

    def _filter_questions(self):
        questions_length = len(self._questions)
        if questions_length <= self._length:
            return

        self._questions = sample(self._questions, self._length)

    def _load_questions(self) -> list["ExamQuestion"]:
        selector = (
            Select(ExamQuestion)
            .where(ExamQuestion.topic == self._topic)
            .where(ExamQuestion.subject == self._subject)
        )
        with Session(engine) as session:
            return session.scalars(selector).all()

    def _find_topic(self, topic: str) -> Topic:
        selector = Select(Topic).where(Topic.name == topic)
        with Session(engine) as session:
            res = session.scalars(selector).one()
        if res is None:
            raise KeyError(f"can not found topic: {topic}")
        return res

    def _find_subjcet(self, subject: str) -> Subject:
        selector = Select(Subject).where(Subject.name == subject)
        with Session(engine) as session:
            res = session.scalars(selector).one()
        if res is None:
            raise KeyError(f"can not found subject: {subject}")
        return res

    def _find_student(self, student_name: str) -> Student:
        selector = Select(Student).where((Student.name == student_name))
        with Session(engine) as session:
            res = session.scalars(selector).one()
        if res is None:
            raise KeyError(f"can not found student: {student_name}")
        return res
