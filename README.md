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

## 6. 개발 워크스테이션: Linux CLI 및 권한

### 6.1 실행 환경

Docker 웹 서버 실습은 Ubuntu Linux 환경(`GNIA-C201-H02`)에서 진행하였으며, Linux 파일 권한 변경 실습은 Ubuntu on WSL2 환경(`GNIA-C401-A03`)에서 수행하였다. 두 환경 모두 Bash 터미널을 사용하였다.

### 6.2 터미널 조작과 경로

파일과 디렉터리를 관리하는 기본 Linux CLI 명령어를 정리하였다.

```bash
pwd                    # 현재 디렉터리
ls -la                 # 숨김 파일 포함 목록
mkdir -p ~/codyssey/practice
cd ~/codyssey/practice
touch example.txt
echo "Hello Codyssey" > example.txt
cat example.txt
cp example.txt backup.txt
mv backup.txt renamed.txt
rm renamed.txt
mkdir test-dir
rmdir test-dir
```

절대 경로는 `/`에서 시작하며, 상대 경로는 현재 작업 폴더를 기준으로 한다. 예를 들어 현재 폴더가 `/home/user/docker-web`이면 `/home/user/docker-web/index.html`은 절대 경로이고 `./index.html`은 상대 경로다. 기존 바인드 마운트에서 사용한 `$(pwd)/index.html`은 현재 작업 폴더의 절대 경로를 이용한다.

### 6.3 파일 및 디렉터리 권한 변경

Linux의 권한은 읽기 `r=4`, 쓰기 `w=2`, 실행/경로 진입 `x=1`로 표현된다. 권한 숫자는 소유자·그룹·기타 사용자 순서로 적용한다. 예를 들어 `644`는 `rw-r--r--`, `755`는 `rwxr-xr-x`다.

**실습 환경:** Ubuntu on WSL2, `GNIA-C401-A03`, 2026-11-07, `~/codyssey/permission-practice`

**실행 명령**

```bash
mkdir -p ~/codyssey/permission-practice
cd ~/codyssey/permission-practice
touch permission.txt
chmod 600 permission.txt
ls -l permission.txt
chmod 644 permission.txt
ls -l permission.txt
mkdir permission-dir
chmod 700 permission-dir
ls -ld permission-dir
chmod 755 permission-dir
ls -ld permission-dir
```

**터미널 출력**

```text
-rw------- 1 rlatnal4125031 rlatnal4125031 0 Nov 7 16:23 permission.txt
-rw-r--r-- 1 rlatnal4125031 rlatnal4125031 0 Nov 7 16:23 permission.txt
drwx------ 2 rlatnal4125031 rlatnal4125031 4096 Nov 7 16:23 permission-dir
drwxr-xr-x 2 rlatnal4125031 rlatnal4125031 4096 Nov 7 16:23 permission-dir
```

파일은 `600 → 644`, 디렉터리는 `700 → 755`로 정상 변경되었다. 파일 권한은 `ls -l`, 디렉터리 권한은 `ls -ld`로 확인했다.

---

## 7. Docker 점검 및 운영 명령

Docker 이미지는 실행에 필요한 파일·설정을 담은 읽기 전용 템플릿이며, 컨테이너는 이를 기반으로 생성하는 실행 인스턴스다. 컨테이너 자체의 저장 레이어는 삭제 시 사라질 수 있으므로, 영속 데이터는 별도 볼륨이나 마운트로 관리한다.

### 7.1 버전·데몬·hello-world 확인

Docker 설치 상태와 데몬 동작 여부는 다음 명령으로 확인한다.

```bash
cat /etc/os-release
echo "$SHELL"
docker --version
docker info
git --version
docker run --rm hello-world
```

`docker --version`은 Docker CLI 버전을, `docker info`는 엔진 및 데몬 연결 상태를 확인한다. `docker run --rm hello-world`는 이미지를 실행해 Docker 환경이 정상 동작하는지 점검하는 명령이다.

### 7.2 Docker 운영

```bash
docker pull nginx:alpine
docker images
docker ps
docker ps -a
docker logs my-web-server
docker stats --no-stream
```

`docker images`는 이미지 목록, `docker ps -a`는 종료된 컨테이너를 포함한 목록, `docker logs`는 출력 로그, `docker stats`는 리소스 사용량을 확인한다. 명령 실행 시 컨테이너 존재 여부에 주의한다.

**컨테이너 실행 로그**

```text
CONTAINER ID   IMAGE          STATUS         PORTS
df60b115fe66   nginx:alpine   Up 4 seconds   0.0.0.0:8081->80/tcp
```

### 7.3 Ubuntu 컨테이너 실행 및 내부 명령

Ubuntu 컨테이너에서 대화형 터미널을 실행하고 내부 명령어를 확인하는 절차는 다음과 같다.

```bash
docker run -it --name ubuntu-practice ubuntu:24.04 bash
# 컨테이너 내부
pwd
ls -la
echo "Hello from Ubuntu"
exit
# 호스트에서
docker ps -a
docker start ubuntu-practice
docker exec ubuntu-practice echo "Exec test"
```

`docker attach`는 실행 중인 주 프로세스에 연결하며, `docker exec`는 실행 중인 컨테이너에서 추가 명령을 실행한다. 주 프로세스가 종료된 컨테이너에서는 먼저 `docker start`가 필요하다.

### 7.4 커스텀 이미지 빌드 검증

본 저장소의 `Dockerfile`은 `nginx:alpine`을 베이스로 사용하고, `COPY index.html`로 기본 콘텐츠를 교체한다. `EXPOSE 80`은 내부 포트를 문서화하는 설정이며 호스트 포트 게시와는 다르다.

```bash
docker build -t my-web-server .
docker images
docker run -d -p 8080:80 --name my-web my-web-server
curl http://localhost:8080
```

웹 서버 접속 결과는 **2.4절의 실행 화면**에서 확인할 수 있다.

---

## 8. Docker 네트워크 및 마운트 이해

Docker 컨테이너는 기본적으로 네트워크 네임스페이스로 인터페이스·라우팅 테이블·포트 공간 등이 분리된다. `-p 8080:80`은 호스트의 8080 포트로 유입된 연결을 컨테이너 내부의 80 포트로 전달한다. 컨테이너의 `EXPOSE 80` 선언만으로 호스트에서 바로 접속할 수 있는 것은 아니다.

| 항목 | 바인드 마운트 | Docker 볼륨 |
|---|---|---|
| 저장 위치 | 지정한 호스트 파일·경로 | Docker 관리 영역 |
| 주요 용도 | 개발 중 소스 파일 즉시 반영 | 컨테이너 삭제 후 데이터 보존 |
| 장점 | 호스트에서 파일 직접 수정 | Docker가 저장소를 관리 |
| 주의점 | 호스트 경로·권한에 의존 | 볼륨 자체를 삭제하면 데이터 손실 가능 |

실습에서는 바인드 마운트의 `:ro` 옵션으로 컨테이너 내부 파일을 읽기 전용으로 마운트했다. `$(pwd)`는 현재 경로를 확장하므로 `Dockerfile`과 `index.html`이 있는 작업 디렉터리에서 명령을 실행해야 한다.

---

## 9. Git 및 GitHub 연동

Git은 로컬 변경 이력·브랜치를 관리하고, GitHub는 저장소를 원격으로 호스팅해 공유와 협업을 지원한다.

**Git 설정 및 확인 명령**

```bash
git config --global user.name "YOUR_NAME"
git config --global user.email "YOUR_EMAIL"
git config --global init.defaultBranch main
git config --list
git remote -v
git branch --show-current
git status
```

저장소: https://github.com/Kimsumi111/Codyssey-Project

VSCode Source Control에서 변경 파일과 원격 저장소 연결 상태를 확인할 수 있다. Git 설정 및 연동 정보를 공유할 때는 토큰·비밀번호·개인키·인증 코드를 공개하지 않도록 주의한다.

---

## 10. 트러블슈팅

### 10.1 호스트 포트 8080 충돌

- **문제:** 새 Nginx 컨테이너를 실행할 때 기존 8080 포트 사용으로 충돌 발생
- **원인 가설:** 기존 컨테이너 또는 다른 프로세스가 동일 포트를 점유
- **확인:** `docker ps`로 컨테이너 확인. 필요하다면 `sudo lsof -nP -iTCP:8080 -sTCP:LISTEN`으로 포트 점유 프로세스 확인
- **조치:** 호스트 포트를 8081로 변경

```bash
docker run -d -p 8081:80 --name my-web-server nginx:alpine
docker ps
```

**포트 변경 후 컨테이너 상태**

```text
CONTAINER ID   IMAGE          STATUS         PORTS
df60b115fe66   nginx:alpine   Up 4 seconds   0.0.0.0:8081->80/tcp
```

### 10.2 웹페이지 한글 깨짐

- **문제:** 웹 브라우저에서 한글이 깨져 보임
- **원인 가설:** HTML 문자셋 선언 또는 파일 저장 인코딩 불일치
- **확인 방법:** `file -bi index.html`, `cat index.html`, `curl -I http://localhost:8081`
- **조치 방안:** HTML `<head>`에 `<meta charset="UTF-8">`을 명시하고 파일을 UTF-8로 저장

HTML에 UTF-8 문자셋을 선언하고 파일 인코딩을 UTF-8로 저장하여 한글 깨짐 문제를 점검한다.

### 10.3 Git push 오류

**발생한 오류**

```text
error: src refspec main does not match any
error: failed to push some refs
```

로컬 `main` 브랜치가 없거나 최초 커밋이 없는 경우 발생할 수 있어, 브랜치와 커밋 상태를 확인한다.

```bash
git branch
git log -1
git status
git add .
git commit -m "Initial commit"
git branch -M main
git push -u origin main
```

GitHub 원격 저장소에 `README.md`, `Dockerfile`, `index.html`을 업로드하였다.

---

## 11. 실습 결과 및 결론

이번 실습을 통해 Dockerfile 기반 웹 서버를 구축하고, Docker 컨테이너의 실행 및 데이터 관리 방식을 확인하였다.

1. **Dockerfile**을 사용하여 Nginx 웹 서버 이미지를 생성하였다.
2. **포트 매핑**을 통해 호스트에서 컨테이너 내부의 웹 서버에 접속하였다.
3. **바인드 마운트**를 통해 컨테이너 재시작 없이 HTML 파일 변경 사항이 반영되는 것을 확인하였다.
4. **Docker 볼륨**을 통해 컨테이너 삭제 후에도 저장된 데이터가 유지됨을 확인하였다.

이를 통해 Docker 컨테이너의 실행 환경과 데이터 저장 영역이 분리되어 있음을 이해할 수 있었다. Linux CLI의 파일·디렉터리 조작, 절대·상대 경로, 파일 권한을 정리하고, WSL2 Ubuntu에서 `chmod`를 사용해 파일 및 디렉터리 권한을 변경하여 출력 결과를 확인하였다.
