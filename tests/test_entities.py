import pytest

from src.pytemplate.domain.entities import AnswerOption, MultipleChoiceQuestion, Question, Quiz, TrueFalseQuestion


def test_question_initialization():
    class ConcreteQuestion(Question):
        def display(self):
            return f"Question ID: {self.question_id}, Text: {self.question_text}"

    question = ConcreteQuestion(question_id=1, question_text="What is the capital of France?")
    assert question.question_id == 1
    assert question.question_text == "What is the capital of France?"
    assert question.display() == "Question ID: 1, Text: What is the capital of France?"


def test_abstract_method():
    with pytest.raises(TypeError):
        Question(question_id=1, question_text="What is the capital of France?")


def test_multiple_choice_question_initialization():
    options = [
        AnswerOption(text="Option 1", is_correct=True),
        AnswerOption(text="Option 2", is_correct=False),
        AnswerOption(text="Option 3", is_correct=False),
    ]
    question = MultipleChoiceQuestion(question_id=1, question_text="What is the capital of France?", options=options)

    assert question.question_id == 1
    assert question.question_text == "What is the capital of France?"
    assert len(question.options) == 3
    assert question.options[0].text == "Option 1"
    assert question.options[0].is_correct is True


def test_multiple_choice_question_display():
    options = [
        AnswerOption(text="Option 1", is_correct=True),
        AnswerOption(text="Option 2", is_correct=False),
    ]
    question = MultipleChoiceQuestion(question_id=1, question_text="What is the capital of France?", options=options)
    expected_display = "Question ID: 1\nWhat is the capital of France?\nOptions:\n1. Option 1 (Correct)\n2. Option 2"
    assert question.display() == expected_display


def test_true_false_question_initialization():
    question = TrueFalseQuestion(question_id=2, question_text="Is the sky blue?", correct_answer=True)

    assert question.question_id == 2
    assert question.question_text == "Is the sky blue?"
    assert question.correct_answer is True


def test_true_false_question_display():
    question = TrueFalseQuestion(question_id=2, question_text="Is the sky blue?", correct_answer=True)
    expected_display = "Question ID: 2\n" "Is the sky blue?\n" "Options:\n" "1. True\n" "2. False"
    assert question.display() == expected_display


def test_quiz_initialization():
    quiz = Quiz(quiz_id=1, title="General Knowledge Quiz")

    assert quiz.quiz_id == 1
    assert quiz.title == "General Knowledge Quiz"
    assert quiz.questions == []
    assert quiz.status == "draft"


def test_add_question():
    quiz = Quiz(quiz_id=1, title="General Knowledge Quiz")

    options = [AnswerOption(text="Option 1", is_correct=True), AnswerOption(text="Option 2", is_correct=False)]
    mc_question = MultipleChoiceQuestion(question_id=1, question_text="What is the capital of France?", options=options)
    tf_question = TrueFalseQuestion(question_id=2, question_text="Is the sky blue?", correct_answer=True)

    quiz.add_question(mc_question)
    quiz.add_question(tf_question)

    assert len(quiz.questions) == 2
    assert quiz.questions[0] == mc_question
    assert quiz.questions[1] == tf_question


def test_publish():
    quiz = Quiz(quiz_id=1, title="General Knowledge Quiz")
    result = quiz.publish()

    assert quiz.status == "published"
    assert result == "Quiz 'General Knowledge Quiz' published!"


def test_display():
    options = [AnswerOption(text="Option 1", is_correct=True), AnswerOption(text="Option 2", is_correct=False)]
    mc_question = MultipleChoiceQuestion(question_id=1, question_text="What is the capital of France?", options=options)
    tf_question = TrueFalseQuestion(question_id=2, question_text="Is the sky blue?", correct_answer=True)

    quiz = Quiz(quiz_id=1, title="General Knowledge Quiz")
    quiz.add_question(mc_question)
    quiz.add_question(tf_question)

    expected_display = (
        "Quiz Title: General Knowledge Quiz\n"
        "Status: draft\n\n"
        "Questions:\n"
        "Question ID: 1\n"
        "What is the capital of France?\n"
        "Options:\n"
        "1. Option 1 (Correct)\n"
        "2. Option 2\n\n"
        "Question ID: 2\n"
        "Is the sky blue?\n"
        "Options:\n"
        "1. True\n"
        "2. False"
    )

    assert quiz.display() == expected_display
