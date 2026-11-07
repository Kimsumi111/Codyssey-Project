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

# json 파일에서 퀴즈 데이터를 읽어와 Quiz 객체로 변환
with open(STATE_PATH, "r", encoding="utf-8") as file:
    state = json.load(file)

quizzes = [
    Quiz(item["question"], item["choices"], item["answer"])
    for item in state["quizzes"]
]

def run_quiz(quizzes):
    score = 0

    for quiz in quizzes:
        quiz.print_quiz()

        while True:    # 정답 번호를 입력받아 1~4 사이의 숫자인지 확인
            user_answer = int(input("정답 번호(1~4): "))

            if 1 <= user_answer <= 4:
                break

            print("1~4 사이의 숫자를 입력하세요.")

        if quiz.check_answer(user_answer):
            score += 1

    print(f"총 점수: {score}/{len(quizzes)}")
    
def main():
    while True:
        print("\n=== 퀴즈 프로그램 ===")       # 퀴즈 프로그램 메뉴 출력
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록 보기")
        print("4. 점수 확인")
        print("5. 종료")
        print("=== 선택해주세요. ===")

        choice = input("선택: ")

        switch = {
            "1": lambda: run_quiz(quizzes),    # lambda를 사용하여 함수를 호출할 때 인자를 전달하지 않고 실행
            "2": lambda: print("아직 구현하지 않은 기능입니다."),
            "3": lambda: print("아직 구현하지 않은 기능입니다."),
            "4": lambda: print("아직 구현하지 않은 기능입니다."),
            "5": exit
        }

        action = switch.get(choice)   # 선택한 번호에 연결된 함수 가져오기

        if action is not None:        # 선택한 번호가 존재하면
            action()                  # 함수 실행
        else:
            print("1~5 중 하나를 입력해주세요.")


if __name__ == "__main__":
    main()

