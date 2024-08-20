from abc import ABC, abstractmethod
from dataclasses import dataclass

from pytemplate.domain.value_objects import AnswerOption


@dataclass
class Question(ABC):
    question_id: int
    question_text: str

    @abstractmethod
    def display(self):
        """
        Abstract method that should be implemented by all subclasses.
        """
        raise NotImplementedError("Subclasses must implement this method")


@dataclass
class MultipleChoiceQuestion(Question):
    options: list[AnswerOption]

    def display(self):
        options_display = "\n".join(
            f"{i + 1}. {opt.text} {'(Correct)' if opt.is_correct else ''}".strip() for i, opt in enumerate(self.options)
        )
        return f"Question ID: {self.question_id}\n{self.question_text}\nOptions:\n{options_display}"


@dataclass
class TrueFalseQuestion(Question):
    correct_answer: bool

    def display(self):
        return f"Question ID: {self.question_id}\n" f"{self.question_text}\n" "Options:\n" "1. True\n" "2. False"


class Quiz:
    def __init__(self, quiz_id: int, title: str):
        self.quiz_id = quiz_id
        self.title = title
        self.questions = []
        self.status = "draft"

    def add_question(self, question: Question):
        self.questions.append(question)

    def publish(self):
        self.status = "published"
        return f"Quiz {self.title!r} published!"

    def display(self):
        questions_display = "\n\n".join(question.display() for question in self.questions)
        return f"Quiz Title: {self.title}\nStatus: {self.status}\n\nQuestions:\n{questions_display}"
