from dataclasses import dataclass


@dataclass
class AnswerOption:
    text: str
    is_correct: bool
