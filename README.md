# Student Result Management System

A menu-driven Python program for managing student records and results at New Horizon.
It registers students, records subject scores, works out totals, averages and grades,
and produces report cards and class reports. Everything is saved in a JSON file so
data is still there the next time the program runs.

Built for the *Introduction to Python Programming* project.

- **Name:** YOUR FULL NAME
- **Matric number:** YOUR MATRIC NUMBER
- **Department:** Computer Science

## How to run

You need Python 3.8 or newer. No extra packages are required.

```
git clone https://github.com/YOUR-USERNAME/student-result-system.git
cd student-result-system
python main.py
```

On some systems the command is `python3 main.py`.

The repository comes with four sample students in `data/students.json` so you can try
the menu straight away. Delete that file if you want to start with an empty system;
the program creates a new one when it saves.

## Features

**Student management:** add, view, search (by ID or part of a name), update and delete students.

**Results:** record scores for the five default subjects (English Language, Mathematics,
Physics, Chemistry, Biology) plus any extra subject you want to add, update a single
score later, and print a report card with the student's position in class.

**Reports:** class list sorted by average (highest first) or by name, class statistics
(highest and lowest score, class average, best and weakest student, average per subject),
a text report saved to `reports/`, and a CSV export.

**Data:** saved to `data/students.json` after every change and loaded when the program
starts. A missing file is handled, and a corrupted file is kept as `students.json.bak`
instead of being lost.

## Grading

| Average | Grade | Remark |
|---------|-------|-----------|
| 70 - 100 | A | Excellent |
| 60 - 69 | B | Very Good |
| 50 - 59 | C | Good |
| 40 - 49 | D | Pass |
| 0 - 39 | F | Fail |

## Input rules

- Student ID: `NH` followed by 3 to 5 digits, e.g. `NH001` (checked with a regular expression)
- Date of birth: `DD-MM-YYYY`, must be a real date that is not in the future
- Scores: numbers from 0 to 100

## Project structure

```
student_result_system/
├── main.py          menu and user input
├── student.py       Student class, ID/date validation, search
├── results.py       totals, averages, grades, sorting, class statistics
├── storage.py       loading and saving JSON
├── reports.py       report card, class sheet, text and CSV output
├── test_system.py   unit tests
├── data/
│   └── students.json
├── reports/         generated reports go here
└── README.md
```

## Running the tests

```
python -m unittest test_system -v
```

## Python concepts used

- Variables, data types and type conversion (`float()` on score input)
- `if/elif/else`, `for` and `while` loops
- Lists, tuples (grade table, genders), dictionaries (scores, menu actions)
- Functions with parameters and return values
- Sorting with `sorted()`, `key` and `lambda`
- Exception handling with `try/except/else/finally`
- File handling with JSON and CSV
- Modules: the code is split across several `.py` files
- A `Student` class with methods, `to_dict` and `from_dict`
- `datetime` for the result date and date of birth checks
- Standard library: `os`, `json`, `csv`, `re`, `datetime`, `tempfile`, `unittest`
- Regular expressions for validating student IDs
