"""Student class and helper functions for validating and finding students."""

import re
from datetime import datetime

# Student IDs look like NH001, NH0042, NH12345 (New Horizon prefix + digits)
ID_PATTERN = re.compile(r"^NH\d{3,5}$")
DATE_FORMAT = "%d-%m-%Y"
GENDERS = ("Male", "Female")


class Student:
    def __init__(self, student_id, name, class_name, gender, dob,
                 scores=None, result_date=None):
        self.student_id = student_id
        self.name = name
        self.class_name = class_name
        self.gender = gender
        self.dob = dob
        self.scores = scores if scores is not None else {}
        self.result_date = result_date  # when the scores were last entered

    def set_score(self, subject, score):
        self.scores[subject] = score
        self.result_date = datetime.now().strftime("%d-%m-%Y %H:%M")

    def to_dict(self):
        return {
            "student_id": self.student_id,
            "name": self.name,
            "class_name": self.class_name,
            "gender": self.gender,
            "dob": self.dob,
            "scores": self.scores,
            "result_date": self.result_date,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["student_id"],
            data["name"],
            data["class_name"],
            data["gender"],
            data["dob"],
            data.get("scores", {}),
            data.get("result_date"),
        )

    def __str__(self):
        return f"{self.student_id} - {self.name} ({self.class_name})"


def is_valid_id(student_id):
    return bool(ID_PATTERN.match(student_id))


def is_valid_dob(text):
    """True if text is a real DD-MM-YYYY date that is not in the future."""
    try:
        born = datetime.strptime(text, DATE_FORMAT)
    except ValueError:
        return False
    return born <= datetime.now()


def find_by_id(students, student_id):
    for s in students:
        if s.student_id == student_id.upper():
            return s
    return None


def search_students(students, term):
    """Match on exact ID or on any part of the name."""
    term = term.strip().lower()
    return [s for s in students
            if s.student_id.lower() == term or term in s.name.lower()]
