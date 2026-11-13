import os
import tempfile
import unittest

import results
import storage
from student import Student, is_valid_dob, is_valid_id, search_students


def make_student(sid="NH001", name="Ada Obi", marks=(80, 70, 60, 90, 75)):
    s = Student(sid, name, "SS2A", "Female", "12-05-2010")
    for subject, mark in zip(results.DEFAULT_SUBJECTS, marks):
        s.set_score(subject, mark)
    return s


class TestSystem(unittest.TestCase):
    def test_total_average_grade(self):
        s = make_student()
        self.assertEqual(results.total_score(s), 375)
        self.assertEqual(results.average_score(s), 75)
        self.assertEqual(results.get_grade(75), "A")
        self.assertEqual(results.get_grade(39.9), "F")
        self.assertEqual(results.get_grade(40), "D")

    def test_validation(self):
        self.assertTrue(is_valid_id("NH001"))
        self.assertFalse(is_valid_id("XY1"))
        self.assertTrue(is_valid_dob("01-02-2010"))
        self.assertFalse(is_valid_dob("31-02-2010"))
        self.assertFalse(is_valid_dob("01-01-2999"))

    def test_sort_and_search(self):
        a = make_student("NH001", "Ada Obi", (50,) * 5)
        b = make_student("NH002", "Chidi Eze", (90,) * 5)
        self.assertEqual(results.sort_students([a, b])[0], b)
        self.assertEqual(results.sort_students([b, a], "name")[0], a)
        self.assertEqual(search_students([a, b], "chid"), [b])

    def test_storage_round_trip_and_missing_file(self):
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "students.json")
            self.assertEqual(storage.load_students(path), [])
            storage.save_students([make_student()], path)
            loaded = storage.load_students(path)
            self.assertEqual(loaded[0].name, "Ada Obi")
            self.assertEqual(results.total_score(loaded[0]), 375)

    def test_corrupted_file(self):
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "students.json")
            with open(path, "w") as f:
                f.write("{not json")
            self.assertEqual(storage.load_students(path), [])
            self.assertTrue(os.path.exists(path + ".bak"))

    def test_statistics(self):
        a = make_student("NH001", "Ada Obi", (50,) * 5)
        b = make_student("NH002", "Chidi Eze", (90,) * 5)
        stats = results.class_statistics([a, b])
        self.assertEqual(stats["class_average"], 70)
        self.assertEqual(stats["highest"][0], 90)
        self.assertEqual(stats["lowest"][0], 50)


if __name__ == "__main__":
    unittest.main()
