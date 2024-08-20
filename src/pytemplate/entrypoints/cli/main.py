from src.pytemplate.domain.factories import QuestionFactory
from src.pytemplate.domain.value_objects import AnswerOption
from src.pytemplate.infrastructure.repositories import QuizRepository
from src.pytemplate.service.quiz import QuizService


def get_multiple_choice_question(question_id, question_text):
    """Prompt the user to input multiple choice question details."""
    options = []
    num_options = int(input("Enter the number of options: "))
    for i in range(num_options):
        text = input(f"Enter text for option {i+1}: ")
        is_correct = input(f"Is option {i+1} correct? (yes/no): ").strip().lower() == "yes"
        options.append(AnswerOption(text, is_correct))
    return QuestionFactory.create_question(
        question_type="multiple_choice", question_id=question_id, question_text=question_text, options=options
    )


def get_true_false_question(question_id, question_text):
    """Prompt the user to input true/false question details."""
    correct_answer = input("Is the statement true? (yes/no): ").strip().lower() == "yes"
    return QuestionFactory.create_question(
        question_type="true_false", question_id=question_id, question_text=question_text, correct_answer=correct_answer
    )


def add_questions_to_quiz(quiz_service, quiz_id):
    """Add questions to the quiz based on user input."""
    while True:
        question_type = input("Enter the question type (multiple_choice/true_false): ").strip().lower()
        question = create_question_based_on_type(question_type)

        if question:
            quiz_service.add_question_to_quiz(quiz_id=quiz_id, question=question)

        more_questions = input("Do you want to add another question? (yes/no): ").strip().lower()
        if more_questions == "no":
            break


def create_question_based_on_type(question_type):
    """Create a question based on the provided question type."""
    question_id = int(input("Enter the question ID: "))
    question_text = input("Enter the question text: ")

    if question_type == "multiple_choice":
        return get_multiple_choice_question(question_id, question_text)
    elif question_type == "true_false":
        return get_true_false_question(question_id, question_text)
    else:
        return None


def main():
    """Main function to run the quiz management system."""
    # Initialize repository and service
    quiz_repo = QuizRepository()
    quiz_service = QuizService(quiz_repo)

    # Create a new quiz
    quiz_id = int(input("Enter the quiz ID: "))
    title = input("Enter the quiz title: ")
    quiz = quiz_service.create_quiz(quiz_id=quiz_id, title=title)

    # Add questions to the quiz
    add_questions_to_quiz(quiz_service, quiz_id)

    # Publish and display the quiz
    quiz_service.publish_quiz(quiz_id=quiz_id)
    quiz.display()
