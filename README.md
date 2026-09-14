# python_basics

칸트 부트캠프 **AX 풀스택 개발자 과정**에서 진행한 파이썬 · 데이터베이스 실습을 모아둔 저장소입니다.
챕터별 과제부터, 배운 내용을 합쳐 만든 가계부 프로그램까지 기록하고 있습니다.

---

## 폴더 구성

| 폴더 | 내용 |
| --- | --- |
| `assignments/` | 챕터별 확장 실습 답안 (01 · AI 시대에 데이터베이스를 왜 배워야 하는가 / 02 · 데이터와 DBMS의 기본 개념) |
| `chapter03/` | PostgreSQL과 DBeaver로 실습 환경 검증하기 |
| `chapter04/` | pandas로 분석 질문을 데이터 흐름으로 옮기는 실습 |
| `chapter05/`, `ch05/`, `python_plus/` | 추가 실습 노트북 |
| `AX2_mission/` | SQL 미션 — CRUD부터 조회·집계까지 작성한 쿼리와 실행 결과 캡처 |
| `chapter23_expense_tracker/` | 가계부 프로그램 (아래 참고) |
| `data/` | 실습용 데이터 |

---

## 가계부 프로그램

`chapter23_expense_tracker/`

지출을 기록하고 조회하는 프로그램입니다.
CSV 파일로 시작해 **PostgreSQL로 옮겼고**, 터미널과 웹 화면 두 가지 방식으로 쓸 수 있습니다.

| 파일 | 역할 |
| --- | --- |
| `expense_tracker.py` | 터미널 버전. 입력값을 3단계로 검증한 뒤 DB에 저장합니다 |
| `server.py` | 표준 라이브러리 `http.server` 기반 JSON API 서버 (포트 `5050`) |
| `expense_ledger.html` | 브라우저에서 사용하는 화면 |
| `db.py` | `psycopg2` 연결과 쿼리 |
| `migrate_csv_to_db.py` | 기존 CSV 데이터를 DB로 옮기는 스크립트 (중복 이관 방지) |

### 실행 방법

**1. 패키지 설치**

```bash
pip install psycopg2-binary python-dotenv
```

**2. 테이블 생성**

```bash
psql -d expense_tracker -f schema.sql
```

```sql
CREATE TABLE expenses (
    id          SERIAL PRIMARY KEY,
    date        DATE    NOT NULL,
    category    TEXT    NOT NULL,
    description TEXT    NOT NULL,
    amount      INTEGER NOT NULL CHECK (amount > 0)
);
```

**3. 접속 정보 설정**

`.env.example`을 복사해 `.env`를 만들고 본인 환경에 맞게 채웁니다.

```bash
cp .env.example chapter23_expense_tracker/.env
```

```env
DB_NAME=expense_tracker
DB_USER=postgres
DB_PASSWORD=여기에_실제_비밀번호_입력
DB_HOST=localhost
DB_PORT=5432
```

**4. 실행**

```bash
# 터미널 버전
python chapter23_expense_tracker/expense_tracker.py

# 웹 버전 → http://localhost:5050
python chapter23_expense_tracker/server.py
```

---

## 사용 기술

`Python` · `PostgreSQL` · `psycopg2` · `pandas` · `Jupyter Notebook` · `SQL`

---

## 참고

- `.env`는 커밋하지 않습니다. 접속 정보는 `.env.example`을 복사해 로컬에서만 관리합니다.
- 과제 파일과 캡처 이미지에는 비밀번호, 접속 정보 등이 포함되지 않도록 확인 후 올리고 있습니다.
