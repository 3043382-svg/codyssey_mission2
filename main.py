import json


class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer

    def show(self):
        print(self.question)
        for i, choice in enumerate(self.choices, start=1):
            print(f"{i}. {choice}")

    def check(self, user_answer):
        return user_answer == self.answer


class QuizGame:
    def __init__(self):
        self.quizzes = [
            Quiz("세상에서 가장 뜨거운 과일은?", ["딸기", "사과", "천도복숭아", "바나나"], 3),
            Quiz("도둑이 가장 싫어하는 아이스크림은?", ["설레임", "누가바", "체포탱탱", "죠스바"], 3),
            Quiz("바나나가 웃으면?", ["바나나킥", "바나나우유", "바나나핏", "바나나맛"], 1),
            Quiz("아이폰의 사과 모양은?", ["사과", "깨문애플", "파인애플", "애플주스"], 3),
            Quiz("바람이 귀엽게 부는 곳은?", ["고양", "분당", "성남", "서울"], 2),
        ]
        self.best_score = 0

    def show_menu(self):
        print("\n[ 아재개그 퀴즈 게임 ]")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")

    def get_valid_number(self, prompt, min_value, max_value):
        while True:
            user_input = input(prompt).strip()

            if user_input == "":
                print("입력이 비어있습니다. 다시 입력해주세요.")
                continue

            if not user_input.isdigit():
                print("숫자로 입력해주세요.")
                continue

            number = int(user_input)

            if number < min_value or number > max_value:
                print(f"{min_value}부터 {max_value} 사이의 숫자를 입력해주세요.")
                continue

            return number

    def add_quiz(self):
        print("\n새로운 퀴즈를 추가합니다.")

        while True:
            question = input("문제를 입력하세요: ").strip()
            if question == "":
                print("문제를 비워둘 수 없습니다. 다시 입력해주세요.")
                continue
            break

        choices = []
        for i in range(1, 5):
            while True:
                choice_text = input(f"선택지 {i}: ").strip()
                if choice_text == "":
                    print("선택지를 비워둘 수 없습니다. 다시 입력해주세요.")
                    continue
                break
            choices.append(choice_text)

        answer = self.get_valid_number("정답 번호 (1-4): ", 1, 4)

        new_quiz = Quiz(question, choices, answer)
        self.quizzes.append(new_quiz)

        print("퀴즈가 추가되었습니다!")
        self.save()

    def show_list(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        print(f"\n등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        for i, quiz in enumerate(self.quizzes, start=1):
            print(f"[{i}] {quiz.question}")

    def show_score(self):
        if self.best_score == 0:
            print("아직 퀴즈를 풀지 않았습니다.")
            return

        print(f"\n최고 점수: {self.best_score}문제 정답")

    def save(self):
        data = {
            "quizzes": [
                {
                    "question": quiz.question,
                    "choices": quiz.choices,
                    "answer": quiz.answer
                }
                for quiz in self.quizzes
            ],
            "best_score": self.best_score
        }

        with open("state.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load(self):
        try:
            with open("state.json", "r", encoding="utf-8") as f:
                data = json.load(f)

            self.quizzes = [
                Quiz(q["question"], q["choices"], q["answer"])
                for q in data["quizzes"]
            ]
            self.best_score = data["best_score"]

        except FileNotFoundError:
            print("저장된 데이터가 없어 기본 퀴즈로 시작합니다.")

        except (json.JSONDecodeError, KeyError):
            print("데이터 파일이 손상되어 기본 퀴즈로 시작합니다.")

    def play(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        score = 0
        total = len(self.quizzes)

        for quiz in self.quizzes:
            quiz.show()
            user_answer = self.get_valid_number("정답 번호를 입력하세요: ", 1, len(quiz.choices))

            if quiz.check(user_answer):
                print("정답입니다!")
                score += 1
            else:
                print(f"오답입니다. 정답은 {quiz.answer}번입니다.")

        print(f"\n결과: {total}문제 중 {score}문제 정답!")

        if score > self.best_score:
            self.best_score = score
            print("새로운 최고 점수입니다!")
            self.save()

    def run(self):
        while True:
            self.show_menu()
            choice = input("메뉴를 선택하세요: ").strip()

            if choice == "1":
                self.play()
            elif choice == "2":
                self.add_quiz()
            elif choice == "3":
                self.show_list()
            elif choice == "4":
                self.show_score()
            elif choice == "5":
                print("게임을 종료합니다.")
                break
            else:
                print("1부터 5 사이의 숫자를 입력해주세요.")


game = QuizGame()
game.load()
game.run()