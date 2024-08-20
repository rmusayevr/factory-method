from pytemplate.domain.entities import MultipleChoiceQuestion, Question, TrueFalseQuestion


class QuestionFactory:
    @staticmethod
    def create_question(question_type: str, question_id: int, question_text: str, **kwargs) -> Question:
        if question_type == "multiple_choice":
            return MultipleChoiceQuestion(question_id, question_text, kwargs["options"])
        elif question_type == "true_false":
            return TrueFalseQuestion(question_id, question_text, kwargs["correct_answer"])
        else:
            raise ValueError(f"Invalid question type: {question_type}")
