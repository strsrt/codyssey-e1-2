import json
import random
from datetime import datetime
from pathlib import Path


class GracefulExit(Exception):
    """Raised when input ends or the user interrupts the game."""


class Quiz:
    """Represents one multiple-choice quiz question."""

    def __init__(self, question, choices, answer, hint=""):
        if not isinstance(question, str) or not question.strip():
            raise ValueError("문제는 비어 있을 수 없습니다.")
        if (
            not isinstance(choices, list)
            or len(choices) != 4
            or any(not isinstance(choice, str) or not choice.strip() for choice in choices)
        ):
            raise ValueError("선택지는 비어 있지 않은 항목 4개여야 합니다.")
        if type(answer) is not int or answer not in range(1, 5):
            raise ValueError("정답은 1~4 사이의 정수여야 합니다.")
        if hint is None:
            hint = ""
        if not isinstance(hint, str):
            raise ValueError("힌트는 문자열이어야 합니다.")

        self.question = question.strip()
        self.choices = [choice.strip() for choice in choices]
        self.answer = answer
        self.hint = hint.strip()

    def display(self, index):
        print(f"\n{index}. {self.question}")
        for number, choice in enumerate(self.choices, 1):
            print(f"   ({number}) {choice}")

    def show_hint(self):
        if self.hint:
            print(f"💡 힌트: {self.hint}")
        else:
            print("💡 힌트가 등록되지 않았습니다.")

    def is_correct(self, answer):
        return answer == self.answer

    def to_dict(self):
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
            "hint": self.hint,
        }


class QuizGame:
    """Manages quizzes, gameplay, scores, and persisted game state."""

    def __init__(self, file_path=None):
        self.file_path = Path(file_path) if file_path else Path(__file__).with_name("state.json")
        self.quizzes = []
        self.best_score = None
        self.score_history = []
        self.load_data()

    @staticmethod
    def default_quizzes():
        return [
            Quiz(
                "Python에서 리스트 끝에 요소를 추가하는 메서드는?",
                ["add()", "push()", "append()", "insert()"],
                3,
                "리스트의 마지막에 값을 넣는 메서드입니다.",
            ),
            Quiz(
                "Python에서 딕셔너리의 키와 값을 가져오는 메서드는?",
                ["items()", "values()", "keys()", "getall()"],
                1,
                "키와 값을 함께 쌍으로 제공하는 메서드입니다.",
            ),
            Quiz(
                "반복 가능한 객체의 각 항목을 순회할 때 사용하는 키워드는?",
                ["while", "for", "loop", "each"],
                2,
                "주로 for item in items: 형태로 사용합니다.",
            ),
            Quiz(
                "함수에서 값을 반환할 때 사용하는 키워드는?",
                ["send", "yield", "return", "break"],
                3,
                "함수의 결과를 호출자에게 전달할 때 사용합니다.",
            ),
            Quiz(
                "Python에서 참과 거짓을 나타내는 값의 올바른 표기는?",
                ["true / false", "TRUE / FALSE", "True / False", "yes / no"],
                3,
                "Python은 대문자 T/F로 시작합니다.",
            ),
        ]

    @staticmethod
    def _parse_state(data):
        if not isinstance(data, dict):
            raise ValueError("최상위 데이터는 객체여야 합니다.")
        raw_quizzes = data.get("quizzes")
        if not isinstance(raw_quizzes, list):
            raise ValueError("quizzes는 목록이어야 합니다.")

        quizzes = []
        for item in raw_quizzes:
            if not isinstance(item, dict):
                raise ValueError("퀴즈 항목은 객체여야 합니다.")
            quizzes.append(Quiz(item["question"], item["choices"], item["answer"], item.get("hint", "")))

        best_score = data.get("best_score")
        if best_score is not None and (type(best_score) is not int or best_score < 0):
            raise ValueError("best_score는 0 이상의 정수 또는 null이어야 합니다.")

        raw_history = data.get("score_history", [])
        score_history = []
        if raw_history is not None:
            if not isinstance(raw_history, list):
                raise ValueError("score_history는 목록이어야 합니다.")
            for entry in raw_history:
                if not isinstance(entry, dict):
                    raise ValueError("score_history 항목은 객체여야 합니다.")
                if not isinstance(entry.get("played_at"), str):
                    raise ValueError("score_history의 played_at은 문자열이어야 합니다.")
                total_questions = entry.get("total_questions")
                score = entry.get("score")
                if type(total_questions) is not int or total_questions < 0:
                    raise ValueError("total_questions는 0 이상의 정수이어야 합니다.")
                if type(score) is not int:
                    raise ValueError("score는 정수이어야 합니다.")
                score_history.append({
                    "played_at": entry["played_at"],
                    "total_questions": total_questions,
                    "score": score,
                })

        return quizzes, best_score, score_history

    def load_data(self):
        if not self.file_path.exists():
            self.quizzes = self.default_quizzes()
            self.best_score = None
            self.score_history = []
            self.save_data()
            return

        try:
            with self.file_path.open("r", encoding="utf-8") as file:
                self.quizzes, self.best_score, self.score_history = self._parse_state(json.load(file))
        except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
            print(f"⚠️ 데이터 파일을 읽을 수 없거나 손상되었습니다 ({error}). 기본 퀴즈로 초기화합니다.")
            self.quizzes = self.default_quizzes()
            self.best_score = None
            self.score_history = []
            self.save_data()

    def save_data(self):
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
            "score_history": self.score_history,
        }
        try:
            with self.file_path.open("w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
                file.write("\n")
        except OSError as error:
            print(f"⚠️ 데이터를 저장하지 못했습니다: {error}")
            return False
        return True

    def get_input(self, prompt, input_type=str, valid_range=None):
        while True:
            try:
                value = input(prompt).strip()
            except (KeyboardInterrupt, EOFError) as error:
                print("\n👋 입력이 중단되어 데이터를 저장하고 안전하게 종료합니다.")
                raise GracefulExit from error

            if not value:
                print("⚠️ 입력이 비어 있습니다. 다시 입력해 주세요.")
                continue

            try:
                converted = input_type(value)
            except ValueError:
                print("⚠️ 숫자가 필요한 항목에는 숫자를 입력해 주세요." if input_type is int else "⚠️ 올바른 형식으로 입력해 주세요.")
                continue

            if valid_range is not None and converted not in valid_range:
                print(f"⚠️ 허용된 범위({valid_range[0]}~{valid_range[-1]})의 값을 입력해 주세요.")
                continue
            return converted

    def add_quiz(self):
        question = self.get_input("새로운 문제 입력: ")
        choices = [self.get_input(f"선택지 {number} 입력: ") for number in range(1, 5)]
        answer = self.get_input("정답 번호 (1~4): ", int, range(1, 5))
        hint = input("힌트 입력 (없으면 엔터): ").strip()
        self.quizzes.append(Quiz(question, choices, answer, hint))
        if self.save_data():
            print("✅ 퀴즈가 추가되었습니다!")

    def delete_quiz(self):
        if not self.quizzes:
            print("삭제할 퀴즈가 없습니다.")
            return

        print("\n--- 퀴즈 삭제 ---")
        for number, quiz in enumerate(self.quizzes, 1):
            print(f"{number}. {quiz.question}")

        index = self.get_input("삭제할 퀴즈 번호: ", int, range(1, len(self.quizzes) + 1))
        deleted = self.quizzes.pop(index - 1)
        if self.save_data():
            print(f"✅ '{deleted.question}' 퀴즈를 삭제했습니다.")

    def show_list(self):
        print("\n--- 퀴즈 목록 ---")
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return
        for number, quiz in enumerate(self.quizzes, 1):
            print(f"{number}. {quiz.question}")

    def play_game(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없어 게임을 시작할 수 없습니다.")
            return

        quiz_pool = self.quizzes[:]
        random.shuffle(quiz_pool)
        total_questions = self.get_input(f"몇 문제를 풀까요? (1~{len(quiz_pool)}): ", int, range(1, len(quiz_pool) + 1))
        selected = quiz_pool[:total_questions]

        correct_answers = 0
        hint_penalty = 0
        print("\n🚀 퀴즈를 시작합니다!")
        for number, quiz in enumerate(selected, 1):
            quiz.display(number)
            used_hint = False
            while True:
                answer_input = self.get_input("정답 번호 입력 (1~4, h: 힌트): ").lower()
                if answer_input == "h":
                    quiz.show_hint()
                    if not used_hint:
                        hint_penalty += 1
                        used_hint = True
                    continue
                try:
                    answer = int(answer_input)
                except ValueError:
                    print("⚠️ 1~4 사이의 숫자 또는 h를 입력해 주세요.")
                    continue
                if answer not in range(1, 5):
                    print("⚠️ 1~4 사이의 숫자를 입력해 주세요.")
                    continue
                break

            if quiz.is_correct(answer):
                print("✅ 정답입니다!")
                correct_answers += 1
            else:
                print(f"❌ 틀렸습니다. 정답은 {quiz.answer}번입니다.")

        final_score = correct_answers - hint_penalty
        previous_best = self.best_score
        record = {
            "played_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_questions": total_questions,
            "score": final_score,
        }
        self.score_history.append(record)
        if previous_best is None or final_score > previous_best:
            self.best_score = final_score
        self.save_data()

        print(f"\n게임 종료! 정답 수: {correct_answers}/{total_questions}, 최종 점수: {final_score}")
        if previous_best is None or final_score > previous_best:
            print("🎉 최고 점수를 갱신했습니다!")
        elif previous_best is not None and final_score == previous_best:
            print("🏅 현재 최고 점수와 동일합니다.")

    def show_score(self):
        if self.best_score is None:
            print("\n아직 퀴즈를 푼 기록이 없습니다.")
        else:
            print(f"\n🏆 현재 최고 점수: {self.best_score}")

    def show_score_history(self):
        print("\n--- 점수 기록 ---")
        if not self.score_history:
            print("아직 기록된 게임 결과가 없습니다.")
            return
        for index, record in enumerate(self.score_history, 1):
            print(f"{index}. {record['played_at']} | 문제 수: {record['total_questions']} | 점수: {record['score']}")

    def run(self):
        while True:
            print("\n--- 퀴즈 게임 메뉴 ---")
            print("1. 퀴즈 풀기  2. 퀴즈 추가  3. 퀴즈 목록  4. 최고 점수 확인  5. 퀴즈 삭제  6. 점수 기록  7. 종료")
            choice = self.get_input("선택: ", int, range(1, 8))
            if choice == 1:
                self.play_game()
            elif choice == 2:
                self.add_quiz()
            elif choice == 3:
                self.show_list()
            elif choice == 4:
                self.show_score()
            elif choice == 5:
                self.delete_quiz()
            elif choice == 6:
                self.show_score_history()
            else:
                print("게임을 종료합니다.")
                self.save_data()
                return


def main():
    game = QuizGame()
    try:
        game.run()
    except GracefulExit:
        game.save_data()


if __name__ == "__main__":
    main()
