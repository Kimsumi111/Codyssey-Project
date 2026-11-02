# 미션 1-1. Docker 실습 - 웹 서버 구축 및 데이터 영속성 검증

## 1. 실습 개요

Docker를 활용하여 Nginx 기반 웹 서버를 컨테이너화하고, 포트 매핑을 통해 웹페이지에 접속한다. 또한 바인드 마운트(Bind Mount)와 Docker 볼륨(Volume)을 활용하여 파일 변경 반영 및 데이터 영속성을 검증한다.

### 실습 목표
- Dockerfile을 이용한 Docker 이미지 빌드
- Docker 컨테이너 생성 및 실행
- 포트 매핑을 통한 웹 서버 접속
- 바인드 마운트를 통한 파일 변경 반영 확인
- Docker 볼륨을 통한 데이터 영속성 검증


## 2. Dockerfile을 이용한 웹 서버 구축

<img width="1521" height="661" alt="image" src="https://github.com/user-attachments/assets/d9c8fb25-3935-4b7f-a568-33a0e4e0983d" />

### 2.1 Dockerfile 작성

```dockerfile
FROM nginx:alpine

COPY index.html /usr/share/nginx/html/index.html

EXPOSE 80
```

- `FROM`: Nginx Alpine 이미지 사용
- `COPY`: HTML 파일을 컨테이너 내부 웹 서버 경로로 복사
- `EXPOSE`: 컨테이너의 80번 포트 사용 명시

### 2.2 Docker 이미지 빌드

```bash
docker build -t my-web-server .
```

### 2.3 Docker 컨테이너 실행

```bash
docker run -d -p 8080:80 --name my-web my-web-server
```

- `-d`: 백그라운드 실행
- `-p 8080:80`: 호스트 8080 포트와 컨테이너 80 포트 연결
- `--name`: 컨테이너 이름 지정

### 2.4 웹 서버 접속 확인

```bash
docker ps
curl http://localhost:8080
```

웹 브라우저에서 `http://localhost:8080`으로 접속하여 HTML 페이지가 정상적으로 출력되는지 확인한다.

**실행 결과**

<img width="526" height="447" alt="스크린샷 2026-11-02 130244" src="https://github.com/user-attachments/assets/48804757-2ef8-4536-b952-b6f901cdf03b" />


---

## 3. 바인드 마운트(Bind Mount) 검증

### 3.1 바인드 마운트 적용

호스트의 `index.html` 파일을 컨테이너 내부의 Nginx 웹페이지 경로에 연결한다.

기존 8080 포트 사용 컨테이너를 제거한 후 실행한다.

```bash
docker rm -f my-web

docker run -d \
  -p 8080:80 \
  --name my-web-server \
  -v "$(pwd)/index.html:/usr/share/nginx/html/index.html:ro" \
  nginx:alpine
```

### 3.2 HTML 파일 수정

```bash
nano index.html
```

HTML 파일의 내용을 다음과 같이 수정한다.

```html
<h1>안녕하세요 수미에요!</h1>
<p>바인드 마운트 변경 반영 성공!</p>
```

### 3.3 변경 사항 확인

```bash
curl http://localhost:8080
```

컨테이너를 재시작하거나 이미지를 다시 빌드하지 않고 수정된 내용이 웹페이지에 반영되는지 확인한다.

**검증 결과**

<img width="616" height="501" alt="스크린샷 2026-11-02 143929" src="https://github.com/user-attachments/assets/5959e56b-f586-4522-bb64-bfe43f4fe77f" />


호스트 파일의 수정 사항이 컨테이너 내부 웹 서버에 즉시 반영됨을 확인하였다.

---

## 4. Docker 볼륨(Volume) 데이터 영속성 검증

### 4.1 Docker 볼륨 생성

```bash
docker volume create my-data
```

생성된 볼륨을 확인한다.

```bash
docker volume ls
```

### 4.2 볼륨을 연결한 컨테이너 실행

```bash
docker run -d \
  --name volume-test \
  -v my-data:/data \
  alpine sleep infinity
```

### 4.3 컨테이너 내부에 데이터 저장

```bash
docker exec volume-test sh -c \
  'echo "Hello Docker Volume!" > /data/test.txt'
```

저장한 파일의 내용을 확인한다.

```bash
docker exec volume-test cat /data/test.txt
```

출력 결과:

```text
Hello Docker Volume!
```

### 4.4 컨테이너 삭제

```bash
docker rm -f volume-test
```

기존 컨테이너를 삭제하여 데이터가 유지되는지 검증한다.

### 4.5 새로운 컨테이너에서 데이터 확인

```bash
docker run --rm \
  -v my-data:/data \
  alpine cat /data/test.txt
```

출력 결과:

```text
Hello Docker Volume!
```

**검증 결과**

<img width="1535" height="531" alt="스크린샷 2026-11-02 142658" src="https://github.com/user-attachments/assets/e7a34bfa-d653-4b6f-9263-cdfd07d1d823" />


기존 컨테이너를 삭제한 후 새로운 컨테이너에서 동일한 볼륨을 연결했을 때, 저장된 데이터가 유지됨을 확인하였다.

---

## 5. 바인드 마운트와 Docker 볼륨 비교

| 구분 | Bind Mount | Docker Volume |
|---|---|---|
| 저장 위치 | 호스트의 지정 경로 | Docker 관리 영역 |
| 관리 주체 | 사용자 | Docker |
| 주요 목적 | 파일 공유 및 변경 반영 | 데이터 영속성 |
| 실습 방법 | HTML 파일 수정 | 컨테이너 삭제 후 데이터 확인 |
| 검증 결과 | 수정 사항 즉시 반영 | 기존 데이터 유지 |

---

## 6. 실습 결과 및 결론

이번 실습을 통해 Dockerfile 기반 웹 서버를 구축하고, Docker 컨테이너의 실행 및 데이터 관리 방식을 확인하였다.

1. **Dockerfile**을 사용하여 Nginx 웹 서버 이미지를 생성하였다.
2. **포트 매핑**을 통해 호스트에서 컨테이너 내부의 웹 서버에 접속하였다.
3. **바인드 마운트**를 통해 컨테이너 재시작 없이 HTML 파일 변경 사항이 반영되는 것을 확인하였다.
4. **Docker 볼륨**을 통해 컨테이너 삭제 후에도 저장된 데이터가 유지됨을 확인하였다.

이를 통해 Docker 컨테이너의 실행 환경과 데이터 저장 영역이 분리되어 있음을 이해할 수 있었다.
