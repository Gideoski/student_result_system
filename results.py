"""Score calculations, grading and class statistics."""

DEFAULT_SUBJECTS = [
    "English Language",
    "Mathematics",
    "Physics",
    "Chemistry",
    "Biology",
]

# (minimum average, grade, remark) - checked from the top down
GRADE_TABLE = [
    (70, "A", "Excellent"),
    (60, "B", "Very Good"),
    (50, "C", "Good"),
    (40, "D", "Pass"),
    (0, "F", "Fail"),
]


def total_score(student):
    return sum(student.scores.values())


def average_score(student):
    if not student.scores:
        return 0.0
    return total_score(student) / len(student.scores)


def get_grade(average):
    for minimum, grade, _ in GRADE_TABLE:
        if average >= minimum:
            return grade
    return "F"


def get_remark(average):
    for minimum, _, remark in GRADE_TABLE:
        if average >= minimum:
            return remark
    return "Fail"


def has_results(student):
    return len(student.scores) >= len(DEFAULT_SUBJECTS)


def sort_students(students, by="average"):
    """Return a new sorted list. by='average' is highest first, by='name' is A-Z."""
    if by == "name":
        return sorted(students, key=lambda s: s.name.lower())
    return sorted(students, key=average_score, reverse=True)


def class_statistics(students):
    """Stats for students who have results. Returns None if there are none."""
    scored = [s for s in students if has_results(s)]
    if not scored:
        return None

    all_scores = []  # (score, student name, subject)
    for s in scored:
        for subject, mark in s.scores.items():
            all_scores.append((mark, s.name, subject))

    averages = [average_score(s) for s in scored]
    return {
        "count": len(scored),
        "highest": max(all_scores),
        "lowest": min(all_scores),
        "class_average": sum(averages) / len(averages),
        "top_student": max(scored, key=average_score),
        "bottom_student": min(scored, key=average_score),
    }


def subject_averages(students):
    """Average mark per subject across the given students."""
    totals = {}
    for s in students:
        for subject, mark in s.scores.items():
            totals.setdefault(subject, []).append(mark)
    return {sub: sum(marks) / len(marks) for sub, marks in totals.items()}
