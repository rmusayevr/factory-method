import pytest

from pytemplate.domain.entities import MultipleChoiceQuestion, Quiz
from pytemplate.domain.value_objects import AnswerOption
from src.pytemplate.infrastructure.repositories import QuizRepository
from src.pytemplate.service.quiz import QuizService


def test_create_quiz():
    repository = QuizRepository()
    quiz_service = QuizService(repository)
    quiz = quiz_service.create_quiz(quiz_id=1, title="General Knowledge Quiz")

    assert isinstance(quiz, Quiz)
    assert quiz.quiz_id == 1
    assert quiz.title == "General Knowledge Quiz"


def test_add_question_to_quiz():
    repository = QuizRepository()
    quiz_service = QuizService(repository)
    quiz = quiz_service.create_quiz(quiz_id=2, title="Science Quiz")

    options = [AnswerOption(text="Option A", is_correct=True), AnswerOption(text="Option B", is_correct=False)]
    mc_question = MultipleChoiceQuestion(question_id=3, question_text="What is the chemical symbol for water?", options=options)

    quiz_service.add_question_to_quiz(quiz_id=2, question=mc_question)

    retrieved_quiz = quiz_service.repository.find_by_id(2)
    assert len(retrieved_quiz.questions) == 1
    assert retrieved_quiz.questions[0] == mc_question


def test_publish_quiz():
    repository = QuizRepository()
    quiz_service = QuizService(repository)
    quiz = quiz_service.create_quiz(quiz_id=4, title="Geography Quiz")
    quiz_service.publish_quiz(quiz_id=4)

    assert quiz.status == "published"


def test_publish_quiz_not_found():
    repository = QuizRepository()
    quiz_service = QuizService(repository)
    with pytest.raises(ValueError, match="Quiz with ID 999 not found"):
        quiz_service.publish_quiz(quiz_id=999)


def test_add_question_to_quiz_not_found():
    repository = QuizRepository()
    quiz_service = QuizService(repository)
    options = [AnswerOption(text="Option X", is_correct=True), AnswerOption(text="Option Y", is_correct=False)]
    mc_question = MultipleChoiceQuestion(question_id=5, question_text="What is the largest planet?", options=options)

    with pytest.raises(ValueError, match="Quiz with ID 999 not found"):
        quiz_service.add_question_to_quiz(quiz_id=999, question=mc_question)
