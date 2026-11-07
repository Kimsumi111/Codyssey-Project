# Codyssey Project

코디세이 미션별 실습 코드와 기록을 정리한 저장소입니다.

## 미션 목록

| 미션 | 내용 | 폴더 |
| --- | --- | --- |
| 1-1 | 개발 워크스테이션 구축: Linux CLI, Docker, Git/GitHub | [mission-1-1](mission-1-1/README.md) |
| 1-2 | Python 콘솔 퀴즈 프로그램 | [mission-1-2](mission-1-2/) |

## 파일 구조

```text
Codyssey-Project/
├── README.md
├── mission-1-1/
│   ├── README.md
│   ├── Dockerfile
│   └── index.html
└── mission-1-2/
    ├── quiz.py
    └── state.json
```

## 미션 1-1 실행

저장소 루트에서 아래 폴더로 이동한 뒤 Docker 명령을 실행합니다. 상세 실습 기록은 [미션 1-1 README](mission-1-1/README.md)에 있습니다.

```bash
cd mission-1-1
docker build -t my-web-server .
```

## 미션 1-2 실행

Python 3.10 이상 환경에서 저장소 루트를 기준으로 실행합니다.

```bash
python mission-1-2/quiz.py
```

퀴즈 풀기, 퀴즈 추가, 목록 보기, 최고 점수 확인 기능을 제공합니다. 퀴즈와 최고 점수는 퀴즈 프로젝트 폴더의 `mission-1-2/state.json`에 UTF-8 JSON으로 저장합니다. `quizzes`는 문제 목록이며 각 문제는 `question`, `choices`, `answer`를 가집니다. `best_score`는 최고 정답 수이고, `null`이면 아직 게임 기록이 없는 상태입니다.
