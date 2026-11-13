"""Building report cards and class reports, and saving them to files."""

import csv
import os
from datetime import datetime

import results
from storage import BASE_DIR

REPORT_DIR = os.path.join(BASE_DIR, "reports")
LINE = "=" * 60


def report_card(student, position=None, total_in_class=None):
    avg = results.average_score(student)
    lines = [
        LINE,
        "NEW HORIZON - STUDENT REPORT CARD".center(60),
        LINE,
        f"Name        : {student.name}",
        f"Student ID  : {student.student_id}",
        f"Class       : {student.class_name}",
        f"Gender      : {student.gender}",
        f"Date of birth: {student.dob}",
        f"Result date : {student.result_date or 'not entered'}",
        "-" * 60,
        f"{'Subject':<30}{'Score':>8}{'Grade':>8}",
        "-" * 60,
    ]
    for subject, mark in student.scores.items():
        lines.append(f"{subject:<30}{mark:>8.1f}{results.get_grade(mark):>8}")
    lines.append("-" * 60)
    lines.append(f"Total   : {results.total_score(student):.1f}")
    lines.append(f"Average : {avg:.2f}")
    lines.append(f"Grade   : {results.get_grade(avg)} ({results.get_remark(avg)})")
    if position:
        lines.append(f"Position: {position} out of {total_in_class}")
    lines.append(LINE)
    return "\n".join(lines)


def student_table(students):
    """Table of students with total, average and grade."""
    header = f"{'ID':<9}{'Name':<26}{'Class':<8}{'Total':>8}{'Avg':>8}{'Grade':>7}"
    lines = [header, "-" * len(header)]
    for s in students:
        if results.has_results(s):
            lines.append(
                f"{s.student_id:<9}{s.name[:24]:<26}{s.class_name:<8}"
                f"{results.total_score(s):>8.1f}{results.average_score(s):>8.2f}"
                f"{results.get_grade(results.average_score(s)):>7}"
            )
        else:
            lines.append(f"{s.student_id:<9}{s.name[:24]:<26}{s.class_name:<8}"
                         f"{'-':>8}{'-':>8}{'-':>7}")
    return "\n".join(lines)


def statistics_text(students):
    stats = results.class_statistics(students)
    if stats is None:
        return "No results have been recorded yet."
    hi_score, hi_name, hi_sub = stats["highest"]
    lo_score, lo_name, lo_sub = stats["lowest"]
    top = stats["top_student"]
    bottom = stats["bottom_student"]
    lines = [
        f"Students with results : {stats['count']}",
        f"Highest score         : {hi_score:.1f} ({hi_name}, {hi_sub})",
        f"Lowest score          : {lo_score:.1f} ({lo_name}, {lo_sub})",
        f"Class average         : {stats['class_average']:.2f}",
        f"Best student          : {top.name} ({results.average_score(top):.2f})",
        f"Weakest student       : {bottom.name} ({results.average_score(bottom):.2f})",
        "",
        "Average per subject:",
    ]
    for subject, avg in results.subject_averages(students).items():
        lines.append(f"  {subject:<26}{avg:>6.2f}")
    return "\n".join(lines)


def full_class_report(students, class_name=None):
    ranked = results.sort_students([s for s in students if results.has_results(s)])
    unranked = [s for s in students if not results.has_results(s)]
    title = f"CLASS RESULT SHEET - {class_name}" if class_name else "CLASS RESULT SHEET - ALL CLASSES"
    lines = [
        LINE,
        title.center(60),
        f"Generated on {datetime.now().strftime('%d-%m-%Y %H:%M')}".center(60),
        LINE,
        "",
        student_table(ranked + unranked),
        "",
        "CLASS STATISTICS",
        "-" * 60,
        statistics_text(students),
        LINE,
    ]
    return "\n".join(lines)


def save_text_report(text, name="class_report"):
    """Save a report into the reports folder and return the file path."""
    os.makedirs(REPORT_DIR, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(REPORT_DIR, f"{name}_{stamp}.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(text + "\n")
    return path


def export_csv(students):
    os.makedirs(REPORT_DIR, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(REPORT_DIR, f"results_{stamp}.csv")
    subjects = results.DEFAULT_SUBJECTS
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Name", "Class", "Gender", "DOB"] + subjects
                        + ["Total", "Average", "Grade"])
        for s in students:
            if not results.has_results(s):
                continue
            avg = results.average_score(s)
            row = [s.student_id, s.name, s.class_name, s.gender, s.dob]
            row += [s.scores.get(sub, "") for sub in subjects]
            row += [results.total_score(s), round(avg, 2), results.get_grade(avg)]
            writer.writerow(row)
    return path
