import json
import os
from random import choices

class Quiz:
    """퀴즈 정보를 담는 클래스"""
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices  # 리스트 형태 [선택지1, 2, 3, 4]
        self.answer = answer    # 정답 번호 (1~4)

    def display(self, index):
        print(f"\n{index}. {self.question}")
        for i, choice in enumerate(self.choices, 1):
            print(f"   ({i}) {choice}")

    def to_dict(self):
        return {"question": self.question, "choices": self.choices, "answer": self.answer}
class QuizGame:
    """게임 로직 및 데이터 관리를 담당하는 클래스"""
    def __init__(self):
        self.file_path = "state.json"
        self.quizzes = []
        self.best_score = 0
        self.load_data()

    def load_data(self):
        """파일 로드 및 손상 시 복구 로직"""
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.quizzes = [Quiz(**q) for q in data.get("quizzes", [])]
                    self.best_score = data.get("best_score", 0)
            else:
                self.set_default_quizzes()
        except (json.JSONDecodeError, KeyError):
            print("⚠️ 데이터 파일이 손상되었습니다. 기본 데이터로 초기화합니다.")
            self.set_default_quizzes()

    def set_default_quizzes(self):
        # 본인이 선택한 주제의 퀴즈 5개 이상 작성
        self.quizzes = [
            Quiz("Python에서 리스트 끝에 요소를 추가하는 메서드는?", ["add()", "push()", "append()", "insert()"], 3),
            # ... 추가 4개 이상
        ]
        self.save_data()

    def save_data(self):
        data = {
            "quizzes": [q.to_dict() for q in self.quizzes],
            "best_score": self.best_score
        }
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    def get_input(self, prompt, input_type=str, valid_range=None):
        """공통 입력 처리: 공백 제거, 타입 변환, 범위 검증, 예외 처리"""
        while True:
            try:
                user_input = input(prompt).strip()

                if not user_input:
                    print("⚠️ 입력이 비어 있습니다. 다시 입력해 주세요.")
                    continue

                converted_input = input_type(user_input)

                if valid_range and converted_input not in valid_range:
                    print(f"⚠️ {valid_range[0]}~{valid_range[-1]} 사이의 숫자를 입력해 주세요.")
                    continue

                return converted_input

            except ValueError:
                print("⚠️ 유효한 형식이 아닙니다. 숫자를 입력해 주세요.")
            except (KeyboardInterrupt, EOFError):
                print("\n\n👋 프로그램을 안전하게 종료합니다.")
                self.save_data()
                exit()

    def add_quiz(self):
        question = input("새로운 문제 입력: ")
        choices = []
        for i in range(1, 5):
            choices.append(input(f"선택지 {i} 입력: "))
        answer = int(input("정답 번호 (1~4): "))
        self.quizzes.append(Quiz(question, choices, answer))
        self.save_data()
        print("✅ 퀴즈가 추가되었습니다!")

    def show_list(self):
        print("\n--- 퀴즈 목록 ---")
        for i, q in enumerate(self.quizzes, 1):
            print(f"{i}. {q.question}")

    def play_game(self):
        current_score = 0
        print("\n🚀 퀴즈를 시작합니다!")
        for i, q in enumerate(self.quizzes, 1):
            q.display(i)              # 문제 + 보기 출력
            user_ans = input("정답 번호 입력 (1~4): ").strip()
        if user_ans == str(q.answer):    # 숫자를 문자로 비교
            print("✅ 정답입니다!")
            current_score += 1
        else:
            print(f"❌ 틀렸습니다. 정답은 {q.answer}번입니다.")

        print(f"\n게임 종료! 당신의 점수: {current_score}/{len(self.quizzes)}")
        if current_score > self.best_score:
            self.best_score = current_score
            self.save_data()
            print("🎉 최고 점수 갱신!")

    def show_score(self):
        print(f"\n🏆 현재 최고 점수: {self.best_score}")

    def run(self):
        while True:
            print("\n--- 퀴즈 게임 메뉴 ---")
            print("1. 퀴즈 풀기  2. 퀴즈 추가  3. 퀴즈 목록  4. 최고 점수 확인  5. 종료")
            choice = self.get_input("선택: ", int, range(1, 6))
            if choice == 1: self.play_game()
            elif choice == 2: self.add_quiz()
            elif choice == 3: self.show_list()
            elif choice == 4: self.show_score()
            elif choice == 5: 
                print("게임을 종료합니다.")
                break
            else: print("잘못된 선택입니다.")

if __name__ == "__main__":
    game = QuizGame()
    game.run()