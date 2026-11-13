"""Loading and saving student data (JSON)."""

import json
import os

from student import Student

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DATA_FILE = os.path.join(DATA_DIR, "students.json")


def load_students(path=DATA_FILE):
    """Read students from the JSON file. A missing file just means no students yet."""
    students = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)
    except FileNotFoundError:
        print("No data file found yet, starting with an empty list.")
    except json.JSONDecodeError:
        # keep the broken file so nothing is lost, then start fresh
        backup = path + ".bak"
        os.replace(path, backup)
        print(f"Data file was corrupted. Copy kept as {os.path.basename(backup)}.")
    else:
        try:
            students = [Student.from_dict(item) for item in raw]
        except (KeyError, TypeError):
            print("Data file has an unexpected format, starting with an empty list.")
    finally:
        print(f"Loaded {len(students)} student(s).")
    return students


def save_students(students, path=DATA_FILE):
    """Write all students to disk. Returns True if it worked."""
    folder = os.path.dirname(path)
    os.makedirs(folder, exist_ok=True)
    temp_path = path + ".tmp"
    try:
        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump([s.to_dict() for s in students], f, indent=4)
        os.replace(temp_path, path)  # swap in only after the write finished
    except OSError as err:
        print(f"Could not save data: {err}")
        return False
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
    return True
