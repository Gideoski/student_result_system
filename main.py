"""New Horizon Student Result Management System - entry point and menu."""

from datetime import datetime

import reports
import results
import storage
from student import (GENDERS, Student, find_by_id, is_valid_dob, is_valid_id,
                     search_students)

MENU = """
========== STUDENT RESULT SYSTEM ==========
 1. Add student              8. Report card
 2. View all students        9. Class list (sorted)
 3. Search student          10. Class statistics
 4. Update student          11. Save text report
 5. Delete student          12. Export results to CSV
 6. Record scores            0. Exit
 7. Update a score
==========================================="""


# ---------- input helpers ----------

def ask(prompt, check=None, error="Invalid input, try again."):
    """Keep asking until the answer is non-empty and passes check (if given)."""
    while True:
        answer = input(prompt).strip()
        if answer and (check is None or check(answer)):
            return answer
        print(error)


def ask_score(subject):
    while True:
        raw = input(f"  {subject} (0-100): ").strip()
        try:
            mark = float(raw)
        except ValueError:
            print("  Please enter a number.")
            continue
        if 0 <= mark <= 100:
            return mark
        print("  Score must be between 0 and 100.")


def ask_gender(prompt="Gender (M/F): "):
    letter = ask(prompt, lambda x: x[0].upper() in "MF" and len(x) == 1,
                 "Enter M or F.")
    return GENDERS[0] if letter.upper() == "M" else GENDERS[1]


def pick_student(students):
    """Ask for an ID and return the matching student, or None."""
    if not students:
        print("No students registered yet.")
        return None
    sid = ask("Student ID: ")
    student = find_by_id(students, sid)
    if student is None:
        print(f"No student with ID {sid.upper()}.")
    return student


def pick_class(students):
    """Optionally narrow down to one class. Blank means all classes."""
    name = input("Class (press Enter for all classes): ").strip()
    if not name:
        return None, students
    chosen = [s for s in students if s.class_name.lower() == name.lower()]
    if not chosen:
        print(f"No students found in {name}.")
    return name, chosen


# ---------- student management ----------

def add_student(students):
    print("\n--- Add new student ---")
    sid = ask("Student ID (e.g. NH001): ", is_valid_id,
              "ID must be NH followed by 3 to 5 digits.").upper()
    if find_by_id(students, sid):
        print("A student with that ID already exists.")
        return
    name = ask("Full name: ").title()
    class_name = ask("Class/Form (e.g. SS2A): ").upper()
    gender = ask_gender()
    dob = ask("Date of birth (DD-MM-YYYY): ", is_valid_dob,
              "Use a real past date in DD-MM-YYYY format.")
    students.append(Student(sid, name, class_name, gender, dob))
    storage.save_students(students)
    print(f"{name} has been registered.")


def view_students(students):
    if not students:
        print("No students registered yet.")
        return
    print(f"\n{'ID':<9}{'Name':<26}{'Class':<8}{'Gender':<8}{'DOB'}")
    print("-" * 62)
    for s in students:
        print(f"{s.student_id:<9}{s.name[:24]:<26}{s.class_name:<8}{s.gender:<8}{s.dob}")
    print(f"\nTotal: {len(students)}")


def search_student(students):
    term = ask("Enter student ID or name: ")
    found = search_students(students, term)
    if not found:
        print("No match found.")
        return
    view_students(found)


def update_student(students):
    student = pick_student(students)
    if student is None:
        return
    print(f"Updating {student.name}. Press Enter to keep the current value.")

    new_name = input(f"Name [{student.name}]: ").strip()
    if new_name:
        student.name = new_name.title()

    new_class = input(f"Class [{student.class_name}]: ").strip()
    if new_class:
        student.class_name = new_class.upper()

    new_gender = input(f"Gender (M/F) [{student.gender}]: ").strip()
    if new_gender:
        if new_gender.upper() in ("M", "F"):
            student.gender = GENDERS[0] if new_gender.upper() == "M" else GENDERS[1]
        else:
            print("Gender not changed (use M or F).")

    new_dob = input(f"Date of birth [{student.dob}]: ").strip()
    if new_dob:
        if is_valid_dob(new_dob):
            student.dob = new_dob
        else:
            print("Date of birth not changed (use a real DD-MM-YYYY date).")

    storage.save_students(students)
    print("Student record updated.")


def delete_student(students):
    student = pick_student(students)
    if student is None:
        return
    sure = input(f"Delete {student.name} permanently? (y/n): ").strip().lower()
    if sure == "y":
        students.remove(student)
        storage.save_students(students)
        print("Record deleted.")
    else:
        print("Nothing was deleted.")


# ---------- scores ----------

def record_scores(students):
    student = pick_student(students)
    if student is None:
        return
    if student.scores:
        print("This student already has scores. Use 'Update a score' to change them.")
        return

    print(f"Enter scores for {student.name}:")
    for subject in results.DEFAULT_SUBJECTS:
        student.set_score(subject, ask_score(subject))

    # extra subjects are optional
    while True:
        extra = input("Add another subject? (name, or Enter to finish): ").strip().title()
        if not extra:
            break
        if extra in student.scores:
            print("That subject is already recorded.")
            continue
        student.set_score(extra, ask_score(extra))

    storage.save_students(students)
    avg = results.average_score(student)
    print(f"Saved. Average: {avg:.2f}, Grade: {results.get_grade(avg)}")


def update_score(students):
    student = pick_student(students)
    if student is None:
        return
    if not student.scores:
        print("No scores recorded for this student yet.")
        return

    subjects = list(student.scores)
    for i, sub in enumerate(subjects, start=1):
        print(f"  {i}. {sub}: {student.scores[sub]}")
    choice = ask("Pick a subject number: ",
                 lambda x: x.isdigit() and 1 <= int(x) <= len(subjects),
                 "Enter one of the numbers shown.")
    subject = subjects[int(choice) - 1]
    student.set_score(subject, ask_score(subject))
    storage.save_students(students)
    print("Score updated.")


# ---------- reports ----------

def show_report_card(students):
    student = pick_student(students)
    if student is None:
        return
    if not student.scores:
        print("No scores recorded for this student yet.")
        return
    # position is worked out within the student's class
    classmates = [s for s in students
                  if s.class_name == student.class_name and results.has_results(s)]
    ranked = results.sort_students(classmates)
    position = ranked.index(student) + 1 if student in ranked else None
    print()
    print(reports.report_card(student, position, len(ranked)))


def show_class_list(students):
    if not students:
        print("No students registered yet.")
        return
    choice = ask("Sort by (1) average, highest first or (2) name: ",
                 lambda x: x in ("1", "2"), "Enter 1 or 2.")
    ordered = results.sort_students(students, "average" if choice == "1" else "name")
    print()
    print(reports.student_table(ordered))


def show_statistics(students):
    name, chosen = pick_class(students)
    if not chosen:
        return
    print()
    print(reports.statistics_text(chosen))


def save_report(students):
    name, chosen = pick_class(students)
    if not chosen:
        return
    text = reports.full_class_report(chosen, name.upper() if name else None)
    try:
        path = reports.save_text_report(text)
    except OSError as err:
        print(f"Could not write the report: {err}")
    else:
        print(f"Report saved to {path}")


def export_csv(students):
    try:
        path = reports.export_csv(students)
    except OSError as err:
        print(f"Could not export: {err}")
    else:
        print(f"CSV exported to {path}")


# ---------- main loop ----------

def main():
    students = storage.load_students()
    print(f"Today is {datetime.now().strftime('%A, %d %B %Y')}")

    actions = {
        "1": add_student,
        "2": view_students,
        "3": search_student,
        "4": update_student,
        "5": delete_student,
        "6": record_scores,
        "7": update_score,
        "8": show_report_card,
        "9": show_class_list,
        "10": show_statistics,
        "11": save_report,
        "12": export_csv,
    }

    while True:
        print(MENU)
        try:
            choice = input("Choose an option: ").strip()
            if choice == "0":
                storage.save_students(students)
                print("Data saved. Goodbye!")
                break
            action = actions.get(choice)
            if action is None:
                print("Please choose a number from the menu.")
            else:
                action(students)
        except (KeyboardInterrupt, EOFError):
            print("\nExiting, saving data first.")
            storage.save_students(students)
            break


if __name__ == "__main__":
    main()
