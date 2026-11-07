import json
from pathlib import Path

STATE_PATH = Path(__file__).parent / "state.json"

# Quiz 클래스 정의
class Quiz:
    def __init__(self, question, choices, answer):   # 퀴즈 객체 초기화
        self.question = question
        self.choices = choices
        self.answer = answer
 
    def print_quiz(self):    # 퀴즈 문제와 선택지 출력
        print(self.question)

        for i in range(4):
            print(f"{i+1}. {self.choices[i]}")

    def check_answer(self, user_answer):    # 사용자가 입력한 정답과 실제 정답을 비교
        if user_answer == self.answer:
            print("정답!")
            return True
        else:
            print("땡!")
            return False

