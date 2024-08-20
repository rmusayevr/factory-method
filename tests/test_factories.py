import pytest

from pytemplate.domain.entities import MultipleChoiceQuestion, TrueFalseQuestion
from src.pytemplate.domain.factories import QuestionFactory
from src.pytemplate.domain.value_objects import AnswerOption


def test_create_multiple_choice_question():
    options = [AnswerOption(text="Option 1", is_correct=True), AnswerOption(text="Option 2", is_correct=False)]
    question = QuestionFactory.create_question(
        question_type="multiple_choice", question_id=1, question_text="What is the capital of France?", options=options
    )

    assert isinstance(question, MultipleChoiceQuestion)
    assert question.question_id == 1
    assert question.question_text == "What is the capital of France?"
    assert len(question.options) == 2


def test_create_true_false_question():
    question = QuestionFactory.create_question(
        question_type="true_false", question_id=2, question_text="Is the sky blue?", correct_answer=True
    )

    assert isinstance(question, TrueFalseQuestion)
    assert question.question_id == 2
    assert question.question_text == "Is the sky blue?"
    assert question.correct_answer is True


def test_create_question_invalid_type():
    with pytest.raises(ValueError, match="Invalid question type: invalid_type"):
        QuestionFactory.create_question(question_type="invalid_type", question_id=3, question_text="This should fail")
