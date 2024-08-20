from pytemplate.domain.entities import Quiz


class QuizRepository:
    def __init__(self):
        self.quizzes = {}

    def save(self, quiz: Quiz):
        self.quizzes[quiz.quiz_id] = quiz

    def find_by_id(self, quiz_id: int):
        return self.quizzes.get(quiz_id)
