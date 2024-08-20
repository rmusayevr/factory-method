from src.pytemplate.domain.value_objects import AnswerOption


def test_answer_option_creation():
    option = AnswerOption(text="Example Answer", is_correct=True)
    assert option.text == "Example Answer"
    assert option.is_correct is True


def test_answer_option_is_correct_false():
    option = AnswerOption(text="Another Answer", is_correct=False)
    assert option.text == "Another Answer"
    assert option.is_correct is False
