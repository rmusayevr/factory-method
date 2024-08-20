from src.pytemplate.domain.entities import Quiz
from src.pytemplate.infrastructure.repositories import QuizRepository


def test_save_and_find_quiz():
    repo = QuizRepository()

    # Create a Quiz instance
    quiz = Quiz(quiz_id=1, title="General Knowledge Quiz")

    # Save the quiz
    repo.save(quiz)

    # Retrieve the quiz by ID
    retrieved_quiz = repo.find_by_id(1)

    assert retrieved_quiz is not None
    assert retrieved_quiz.quiz_id == 1
    assert retrieved_quiz.title == "General Knowledge Quiz"


def test_find_nonexistent_quiz():
    repo = QuizRepository()

    # Try retrieving a quiz that doesn't exist
    retrieved_quiz = repo.find_by_id(999)

    assert retrieved_quiz is None
