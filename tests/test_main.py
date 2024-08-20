from unittest.mock import patch

from pytemplate.domain.entities import MultipleChoiceQuestion, TrueFalseQuestion
from src.pytemplate.domain.value_objects import AnswerOption
from src.pytemplate.entrypoints.cli.main import (
    add_questions_to_quiz,
    create_question_based_on_type,
    get_multiple_choice_question,
    get_true_false_question,
)
from src.pytemplate.infrastructure.repositories import QuizRepository
from src.pytemplate.service.quiz import QuizService


def test_get_multiple_choice_question():
    question_id = 1
    question_text = "What is the capital of France?"

    user_inputs = [
        "2",  # Number of options
        "Paris",  # Option 1 text
        "yes",  # Option 1 is correct
        "Berlin",  # Option 2 text
        "no",  # Option 2 is not correct
    ]

    with patch("builtins.input", side_effect=user_inputs):
        question = get_multiple_choice_question(question_id, question_text)

    assert isinstance(question, MultipleChoiceQuestion)
    assert question.question_id == question_id
    assert question.question_text == question_text
    assert len(question.options) == 2
    assert question.options[0] == AnswerOption(text="Paris", is_correct=True)
    assert question.options[1] == AnswerOption(text="Berlin", is_correct=False)


def test_get_true_false_question():
    question_id = 2
    question_text = "The sky is blue."

    user_inputs = ["yes"]  # Indicate that the statement is true

    with patch("builtins.input", side_effect=user_inputs):
        question = get_true_false_question(question_id, question_text)

    assert isinstance(question, TrueFalseQuestion)
    assert question.question_id == question_id
    assert question.question_text == question_text
    assert question.correct_answer is True


def test_get_true_false_question_false():
    question_id = 3
    question_text = "The earth is flat."

    user_inputs = ["no"]  # Indicate that the statement is false

    with patch("builtins.input", side_effect=user_inputs):
        question = get_true_false_question(question_id, question_text)

    assert isinstance(question, TrueFalseQuestion)
    assert question.question_id == question_id
    assert question.question_text == question_text
    assert question.correct_answer is False


def test_create_question_based_on_type_multiple_choice():
    user_inputs = [
        "1",  # question_id
        "What is the capital of France?",  # question_text
        "2",  # Number of options
        "Paris",  # Option 1 text
        "yes",  # Option 1 is correct
        "Berlin",  # Option 2 text
        "no",  # Option 2 is not correct
    ]

    with patch("builtins.input", side_effect=user_inputs):
        question = create_question_based_on_type("multiple_choice")

    assert isinstance(question, MultipleChoiceQuestion)
    assert question.question_id == 1
    assert question.question_text == "What is the capital of France?"
    assert len(question.options) == 2
    assert question.options[0] == AnswerOption(text="Paris", is_correct=True)
    assert question.options[1] == AnswerOption(text="Berlin", is_correct=False)


def test_create_question_based_on_type_true_false():
    user_inputs = ["2", "The sky is blue.", "yes"]  # question_id  # question_text  # Statement is true

    with patch("builtins.input", side_effect=user_inputs):
        question = create_question_based_on_type("true_false")

    assert isinstance(question, TrueFalseQuestion)
    assert question.question_id == 2
    assert question.question_text == "The sky is blue."
    assert question.correct_answer is True


def test_create_question_based_on_type_invalid():
    user_inputs = [
        "3",  # question_id
        "Is the earth flat?",  # question_text
    ]

    with patch("builtins.input", side_effect=user_inputs):
        question = create_question_based_on_type("invalid_type")

    assert question is None


def test_add_questions_to_quiz_multiple_choice():
    # Mock user inputs for a multiple choice question
    inputs = [
        "multiple_choice",
        "1",
        "What is the capital of France?",
        "3",
        "Paris",
        "yes",
        "London",
        "no",
        "Berlin",
        "no",
        "no",  # Stop adding questions
    ]

    with patch("builtins.input", side_effect=inputs):
        quiz_repo = QuizRepository()
        quiz_service = QuizService(quiz_repo)
        quiz = quiz_service.create_quiz(quiz_id=1, title="Geography Quiz")

        add_questions_to_quiz(quiz_service, quiz_id=1)

        assert len(quiz.questions) == 1
        assert isinstance(quiz.questions[0], MultipleChoiceQuestion)
        assert quiz.questions[0].question_text == "What is the capital of France?"


def test_add_questions_to_quiz_true_false():
    # Mock user inputs for a true/false question
    inputs = ["true_false", "2", "The Earth is flat.", "no", "no"]  # Stop adding questions

    with patch("builtins.input", side_effect=inputs):
        quiz_repo = QuizRepository()
        quiz_service = QuizService(quiz_repo)
        quiz = quiz_service.create_quiz(quiz_id=2, title="Science Quiz")

        add_questions_to_quiz(quiz_service, quiz_id=2)

        assert len(quiz.questions) == 1
        assert isinstance(quiz.questions[0], TrueFalseQuestion)
        assert quiz.questions[0].question_text == "The Earth is flat."


def test_add_questions_to_quiz_invalid_type():
    # Mock user inputs for an invalid question type
    inputs = ["invalid_type", "3", "Is this a valid question?", "no"]  # Stop adding questions
    with patch("builtins.input", side_effect=inputs):
        quiz_repo = QuizRepository()
        quiz_service = QuizService(quiz_repo)
        quiz = quiz_service.create_quiz(quiz_id=3, title="Random Quiz")

        add_questions_to_quiz(quiz_service, quiz_id=3)

        assert len(quiz.questions) == 0
