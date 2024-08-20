from pytemplate.domain.entities import Question, Quiz
from src.pytemplate.infrastructure.repositories import QuizRepository


class QuizService:
    def __init__(self, repository: QuizRepository):
        self.repository = repository

    def create_quiz(self, quiz_id: int, title: str) -> Quiz:
        quiz = Quiz(quiz_id=quiz_id, title=title)
        self.repository.save(quiz)
        return quiz

    def add_question_to_quiz(self, quiz_id: int, question: Question):
        quiz = self.repository.find_by_id(quiz_id)
        if quiz is None:
            raise ValueError(f"Quiz with ID {quiz_id} not found")
        quiz.add_question(question)

    def publish_quiz(self, quiz_id: int):
        quiz = self.repository.find_by_id(quiz_id)
        if quiz is None:
            raise ValueError(f"Quiz with ID {quiz_id} not found")
        return quiz.publish()
