import json

class Question:
    """퀴즈 하나하나의 정보를 담는 클래스"""
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

class QuizManager:
    """퀴즈 게임의 로직(로드, 실행, 저장)을 담당하는 클래스"""
    def __init__(self, file_path):
        self.file_path = file_path
        self.questions = []
        self.score = 0
        self.load_questions()

    def load_questions(self):
        """JSON 파일에서 퀴즈 데이터를 읽어옵니다."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.questions = [Question(q['question'], q['answer']) for q in data]
        except FileNotFoundError:
            print("퀴즈 파일을 찾을 수 없습니다.")

    def start_quiz(self):
        """게임을 시작하고 사용자 입력을 처리합니다."""
        print("🚀 퀴즈 게임을 시작합니다!")
        for q in self.questions:
            user_answer = input(f"문제: {q.question} -> ").strip()
            if user_answer.lower() == q.answer.lower():
                print("✅ 정답입니다!")
                self.score += 1
            else:
                print(f"❌ 틀렸습니다. 정답은 '{q.answer}'입니다.")
        
        print(f"\n게임 종료! 최종 점수: {self.score}/{len(self.questions)}")

# 프로그램 실행부
if __name__ == "__main__":
    manager = QuizManager("quiz.json")
    manager.start_quiz()