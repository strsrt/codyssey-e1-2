import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from main import GracefulExit, Quiz, QuizGame


class QuizBehaviorTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.game = QuizGame(Path(self.temp_dir.name) / "state.json")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_is_correct_matches_only_the_answer(self):
        quiz = Quiz("Question?", ["A", "B", "C", "D"], 2)

        self.assertTrue(quiz.is_correct(2))
        self.assertFalse(quiz.is_correct(1))

    def test_get_input_trims_and_retries_invalid_values(self):
        answers = iter(["", "abc", "9", " 2 "])
        output = io.StringIO()
        with patch("builtins.input", side_effect=lambda _: next(answers)), redirect_stdout(output):
            answer = self.game.get_input("Answer: ", int, range(1, 5))

        self.assertEqual(answer, 2)
        self.assertIn("비어 있습니다", output.getvalue())
        self.assertIn("숫자가 필요한", output.getvalue())
        self.assertIn("허용된 범위", output.getvalue())

    def test_get_input_allows_empty_optional_hint(self):
        with patch("builtins.input", return_value="   "):
            hint = self.game.get_input("Hint: ", allow_empty=True)

        self.assertEqual(hint, "")

    def test_get_input_converts_eof_to_graceful_exit(self):
        output = io.StringIO()
        with patch("builtins.input", side_effect=EOFError), redirect_stdout(output):
            with self.assertRaises(GracefulExit):
                self.game.get_input("Answer: ")

        self.assertIn("안전하게 종료", output.getvalue())


if __name__ == "__main__":
    unittest.main()
