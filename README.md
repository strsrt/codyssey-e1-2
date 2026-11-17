# Python 퀴즈 게임

## 프로젝트 개요

Python 기초 개념을 익히는 콘솔 기반 퀴즈 게임입니다. 문제를 풀고, 힌트를 활용하며, 점수와 기록을 JSON 파일로 저장해 재사용할 수 있습니다.

## 퀴즈 주제와 선정 이유

주제는 Python 기본 문법입니다. 리스트, 딕셔너리, 반복문, 함수, 논리값은 실제 프로그래밍을 시작할 때 가장 자주 접하는 개념이어서 선택했습니다.

## 실행 방법

Python 3가 설치된 환경에서 프로젝트 폴더로 이동해 다음 명령으로 실행합니다.

```text
python main.py
```

다음처럼 바로 실행해도 같은 프로그램이 동작합니다.

```text
python quiz_game.py
```

## 기능 목록

- 랜덤으로 문제 순서를 섞어 출제
- 문제 수를 직접 선택해 퀴즈 풀기
- 힌트 보기 기능과 힌트 사용 시 점수 차감
- 새 퀴즈 추가(문제, 선택지 4개, 정답 번호, 힌트)
- 등록된 퀴즈 삭제
- 퀴즈 목록 확인
- 최고 점수 확인 및 갱신
- 모든 게임 기록 확인
- 빈 입력, 숫자 변환 실패, 범위 밖 입력 재입력 처리
- Ctrl+C, EOF 등 안전 종료 처리
- 상태 파일이 없거나 손상되면 기본 퀴즈 복구

## 파일 구조

```text
.
├── main.py       # Quiz, QuizGame 클래스와 게임 로직
├── quiz_game.py  # main.py를 호출하는 실행 진입점
├── state.json    # 퀴즈, 최고 점수, 점수 기록 저장 파일
├── README.md
├── .gitignore
└── __pycache__/
```

## 데이터 파일 설명

`state.json`은 프로젝트 루트에 위치하며 UTF-8 인코딩으로 저장됩니다. 파일 구조는 다음과 같습니다.

- `quizzes`: 문제 목록
  - `question`: 문제 내용
  - `choices`: 선택지 4개
  - `answer`: 정답 번호(1~4)
  - `hint`: 힌트 문자열
- `best_score`: 최고 점수
- `score_history`: 각 게임의 기록 목록
  - `played_at`: 게임 종료 시각
  - `total_questions`: 푼 문제 수
  - `score`: 최종 점수

```json
{
  "quizzes": [
    {
      "question": "질문",
      "choices": ["선택지 1", "선택지 2", "선택지 3", "선택지 4"],
      "answer": 1,
      "hint": "간단한 힌트"
    }
  ],
  "best_score": 3,
  "score_history": [
    {
      "played_at": "2026-11-17 14:00:00",
      "total_questions": 5,
      "score": 3
    }
  ]
}
```

> Clone practice note: this line was added from the cloned repository.
