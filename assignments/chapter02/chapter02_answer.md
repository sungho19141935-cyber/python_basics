# Chapter 02 확장 실습 답안 템플릿

> **과제:** 데이터와 DBMS의 기본 개념  
> **사용 방법:** 이 파일을 내려받아 본인의 GitHub 저장소에 `chapter02_answer.md`라는 이름으로 저장한 뒤 실습하면서 바로 작성합니다.  
> **제출 방법:** LMS에는 파일을 직접 업로드하지 않고, **본인 GitHub 저장소의 `chapter02_answer.md` 파일 URL**을 제출합니다.

---

## 제출 전 개인정보 주의

LMS에서 제출자를 확인할 수 있으므로 이 공개 Markdown 파일에 학번이나 실명을 반드시 적을 필요는 없습니다.

```text
GitHub 계정 또는 별칭: hodumaru
과제 작성일:26.9.3.
사용한 AI 도구: 클로드
```

> 실제 비밀번호, API Key, 전체 DB 접속 URL, 개인정보가 포함된 화면은 올리지 않습니다.

---

# 1. PostgreSQL에서 현재 위치 확인

## 1-1. 실행한 SQL

```sql
SELECT version();
SELECT current_database();
SELECT current_user;
SELECT current_schema();
SHOW search_path;
```

## 1-2. 실행 결과 기록

```text
PostgreSQL 버전:PostgreSQL 18.6 on x86_64-windows, compiled by msvc-19.44.35228, 64-bit
현재 데이터베이스: ax_evaluation
현재 사용자: ax_evaluation
현재 스키마: public
search_path: "$user", public
```

## 1-3. 구조를 내 말로 설명

```text
PostgreSQL은: SQL을 사용하는 DBMS

현재 접속한 데이터베이스는: ax_evaluation

스키마는: public

DBeaver 또는 psql 같은 도구는: postgreSQL 에 접속해서 결과를 보여주는 프로그램
```

## 1-4. 계층 구조 완성

```text
사용자
→ DBeaver
→ PostgreSQL DBMS
→ Databasse
→ 스키마
→ 테이블
→ 행 / 열
```

## 1-5. 증거 화면

권장 경로:

```text
assignments/chapter02/images/step01_environment.png
```

```markdown
![PostgreSQL 현재 위치 확인](./images/step01_environment.png)
```

`여기에 STEP 1 핵심 증거 화면을 삽입하세요.`

---

# 2. 데이터베이스 안의 스키마와 테이블 관찰

## 2-1. 스키마 조회 결과

실행한 SQL:

```sql
SELECT schema_name
FROM information_schema.schemata
ORDER BY schema_name;
```

관찰한 스키마 이름 중 3개 이내를 적습니다.

```text
1.public
2.pg_toast_temp_99
3.pg_temp_99
```

### `public`은 무엇인가요?

```text
나의 설명:기본 스키마
```

### 데이터베이스와 스키마는 같은 것인가요?

```text
나의 설명: 스키마는 테이블을 모아둔 공간
```

## 2-2. 현재 보이는 테이블 조회

```sql
SELECT table_schema, table_name
FROM information_schema.tables
WHERE table_type = 'BASE TABLE'
  AND table_schema NOT IN ('pg_catalog', 'information_schema')
ORDER BY table_schema, table_name;
```

```text
조회된 사용자 테이블 수 또는 눈에 띈 테이블: 69

아직 테이블이 거의 없어도 괜찮은 이유: 테이블이 많다고 좋은게 아니기 때문
```

## 2-3. 관찰 정리

```text
PostgreSQL 서버 안에는 여러 데이터베이스가 있을 수 있다.
한 데이터베이스 안에는 여러 스키마가 있을 수 있다.
스키마 안에는 테이블과 같은 객체가 존재한다.
```

---

# 3. TEMP TABLE로 테이블·행·열·키 직접 확인

ㅍ

각 테이블의 **한 행 의미**를 적습니다.

| 테이블 | 한 행의 의미 |
| --- | --- |
| `ch02_students` | 학생 한 명 |
| `ch02_courses` | 강의 한 개 |
| `ch02_enrollments` | 수강신청 한 건 |

## 3-2. 열의 의미 확인

### `ch02_students`

| 열 | 값의 의미 | 내부 식별자 / 업무 식별자 / 일반 속성 |
| --- | --- | --- |
| `id` | 학생 식별 번호 | 내부 식별자 |
| `student_number` | 특성 | 내부 식뱔자 |
| `name` | 이름 | 일반 속성 |
| `major` | 전공 | 일반 속성 |

### `ch02_enrollments`

| 열 | 값의 의미 | PK / FK / 일반 속성 |
| --- | --- | --- |
| `id` | 수강신청 한 건 | PK |
| `student_id` | 학생 한 명 | FK |
| `course_id` | 강의 한 개 | FK |
| `status` | 진행 상태 | 일반 속성 |

## 3-3. 입력된 행 수

```text
students 행 수: 3
courses 행 수: 2
enrollments 행 수:3
```

## 3-4. 내부 식별자와 업무 식별자

```text
students.id가 필요한 이유: enrollments에서 학생 한 명의 정보가 필요함

student_number가 필요한 이유: 학생의 학번을 확인하기 위함

둘을 항상 같은 값으로 사용하지 않아도 되는 이유: 담고 있는 정보가 다를 수 있기 때문
```

## 3-5. 숫자처럼 보이는 학번을 문자열로 저장한 이유

```text
나의 설명: 숫자로 하면 수량으로 파악하게 되기에 식별을 위해서는 문자열로 저장해야 함
```
---

# 4. 테이블과 조회 결과는 다르다

## 4-1. 원본 테이블 행 수

```text
ch02_students 전체 행 수: 3
```

## 4-2. 일부 열만 조회

실행 SQL:

```sql
SELECT name, major
FROM ch02_students
ORDER BY id;
```

```text
원본 테이블의 열 수와 조회 결과의 열 수가 다른 이유: 이름과 전공을 같이 호출
```

## 4-3. 조건을 적용한 조회

실행 SQL:

```sql
SELECT id, student_number, name, major
FROM ch02_students
WHERE major = '컴퓨터공학'
ORDER BY id;
```

```text
원본 테이블 행 수:3
조회 결과 행 수:2
원본 테이블의 데이터가 삭제된 것인가?: no
그렇게 판단한 이유: 컴퓨터공학만 보여달라는 조건을 걺
```

## 4-4. 정렬 결과 비교

```sql
SELECT id, name
FROM ch02_students
ORDER BY name ASC;

SELECT id, name
FROM ch02_students
ORDER BY name DESC;
```

```text
ASC 결과의 첫 학생: 김민지
DESC 결과의 첫 학생: 이준호

이 실험을 통해 ORDER BY에 대해 알게 된 점: 한글도 역순이 가능 하구나
```

## 4-5. 증거 화면

권장 경로:

```text
assignments/chapter02/images/step04_result_set.png
```

`여기에 STEP 4 핵심 증거 화면을 삽입하세요.`

---

# 5. PK와 FK를 실제로 관찰

## 5-1. 정상 데이터의 관계 읽기

다음 SQL 결과를 보고 작성합니다.

```sql
SELECT
    e.id AS enrollment_id,
    s.name AS student_name,
    c.title AS course_title,
    e.status
FROM ch02_enrollments AS e
JOIN ch02_students AS s
    ON s.id = e.student_id
JOIN ch02_courses AS c
    ON c.id = e.course_id
ORDER BY e.id;
```

```text
한 행이 의미하는 것: 학생 수강신천 정보

같은 student_id가 여러 enrollment 행에서 반복될 수 있는 이유: student_id는 enrollment에서 unique가 아님

같은 course_id가 여러 enrollment 행에서 반복될 수 있는 이유: 각각의 수강 관계를 별도의 enrollment_id로 구분하기 때문
```

## 5-2. 기본키 중복 오류 관찰

중복 PK 입력을 시도한 결과:

```text
실행 성공 / 실패: 실패
오류 메시지에서 확인한 핵심 단어:
duplicate key
PRIMARY KEY
already exists
왜 실패했다고 생각하는가: 중복 된 PK값을 입력해서 PK값은 고유해서
```

## 5-3. 존재하지 않는 학생을 참조하는 FK 오류 관찰

존재하지 않는 `student_id`를 사용한 수강신청 입력 결과:

```text
실행 성공 / 실패:실패
오류 메시지에서 확인한 핵심 단어:
foreign key
violates
REFERENCES
왜 실패했다고 생각하는가: 존재하지 않는 id를 fk로 가져올 수 없음
```

## 5-4. PK와 FK의 차이 정리

```text
PK는다른 행과 구별해서 유일하게 식별하기 위한 키이다.

FK는 고유 행을 여러 다른 행들이 참조하기 위한 키이다.

FK 값이 여러 행에서 반복될 수 있는 이유는
다른 테이블의 그 유일한 값을 가리키는 포인터 때문이다.
```

## 5-5. 증거 화면

권장 경로:

```text
assignments/chapter02/images/step05_pk_fk.png
```

> 오류 메시지는 전체 화면이 아니라 테이블명·constraint·참조 오류가 보이는 정도만 캡처합니다.

`여기에 STEP 5 핵심 증거 화면을 삽입하세요.`

---

# 6. 관계와 카디널리티를 자연어로 설명

현재 임시 데이터 기준으로 작성합니다.

```text
학생 한 명은 여러 수강신청을 가질 수 있는가?: 네

강의 한 개는 여러 수강신청을 가질 수 있는가?: 네

수강신청 한 건은 학생 몇 명을 참조하는가?: 1

수강신청 한 건은 강의 몇 개를 참조하는가?: 1
```

아래 구조를 완성합니다.

```text
students 1 ── ___1:n___ enrollments ___n:1___ ── 1 courses
```

### 학생과 강의가 N:M 관계라고 볼 수 있는 이유

```text
나의 설명: 한 명이 여러 강의를 들을 수 있기 때문
```

> 아직 0개 허용 여부, 필수 관계, 삭제 정책까지 확정하지 않습니다. 그런 규칙은 Chapter 05~06에서 다룹니다.

---

# 7. AI가 만든 테이블 구조 직접 검토

## 7-1. AI에게 묻기 전에 내가 먼저 찾은 문제

다음 구조를 보고 최소 4개를 적습니다.

```sql
CREATE TABLE student_courses (
    student_name VARCHAR(50),
    student_email VARCHAR(100),
    course_title VARCHAR(100),
    instructor_name VARCHAR(50)
);
```

```text
문제 1. pk가 없음
문제 2. fk 안 가져옴
문제 3. name으로 동명이인 구분 불가
문제 4.
```

## 7-2. AI 검토 요청 프롬프트

사용한 핵심 프롬프트를 기록합니다.

```text
REATE TABLE student_courses (
    student_name VARCHAR(50),
    student_email VARCHAR(100),
    course_title VARCHAR(100),
    instructor_name VARCHAR(50)

);
이 코드가 잘못된 점은 내가 생각했을 때 pk가 없고 불러오는 fk 가 없는 거 같은데 혹시 이거 외에 더 잘못된 부분이 있다면 알려줄래?
```

## 7-3. AI 제안과 나의 판단

AI의 지적 또는 제안	동의 / 수정 / 보류	나의 근거
PK가 필요하다	동의	각 데이터를 고유하게 식별하기 위해 PK가 필요하다.
FK가 필요하다	동의	학생, 과목, 교수 등의 테이블과 관계를 연결해야 하기 때문이다.
학생 이름과 이메일을 직접 저장하면 중복이 발생할 수 있다	동의	한 학생이 여러 과목을 수강하면 같은 학생 정보가 여러 번 저장될 수 있다.
이름 대신 student_id를 사용하는 것이 좋다	동의	이름은 동명이인이 있을 수 있지만 student_id는 학생을 고유하게 식별할 수 있다.
course_title, instructor_name 대신 각각 course_id, instructor_id를 사용하는 것이 좋다	동의	이름이나 과목명은 변경될 수 있으므로 PK를 FK로 참조하는 것이 데이터 관리에 적합하다.
## 7-4. 본문과 대조한 항목

AI 설명 중 최소 하나를 `chapter02.md`와 비교합니다.

```text
AI가 설명한 내용:왜 같은 student_id가 반복될까?
한 학생이 여러 과목을 수강할 수 있기 때문

본문에서 확인한 내용: 학생 1명이 여러 수강신청을 가질 수 있기 때문

일치 / 부분 일치 / 수정 필요: 일치

내가 최종적으로 이해한 내용: FK는 자동으로 UNIQUE가 되는 값이 아님
```

## 7-5. 증거 화면

권장 경로:

```text
assignments/chapter02/images/step07_ai_review.png
```

`여기에 AI 검토 과정의 핵심 화면을 삽입하세요.`

---

# 8. Chapter 01의 개인 서비스 아이디어를 DB 용어로 다시 표현

Chapter 01에서 정한 개인 서비스 주제를 그대로 사용하거나 새 주제를 정해도 됩니다.

## 8-1. 서비스 기본 정보

```text
서비스 이름:스터디 모임 관리
서비스 목적:여러 사람이 함께 진행하는 스터디 모임의 멤버, 일정, 출석, 과제 제출을 한곳에서 관리한다.
```

## 8-2. PostgreSQL 구조 후보

```text
데이터베이스 이름 후보:study_management_db
스키마 이름 후보: study_app
```

> 아직 실제 데이터베이스나 스키마를 생성하지 않아도 됩니다.

## 8-3. 테이블 후보와 한 행 의미

최소 3개를 작성합니다.
| 테이블 후보 | 한 행의 의미 | 내부 ID 후보 | 업무 식별자 후보 |
| --- | --- | --- | --- |
| users | 서비스에 등록된 회원 한 명 | id | email |
| study_groups | 개설된 스터디 모임 한 개 | id | 없음 |
| memberships | 특정 회원이 특정 스터디에 가입한 내역 한 건 | id | (user_id, group_id) 조합 |
| schedules | 특정 스터디에서 진행되는 일정(모임) 한 개 | id | 없음 |
| attendances | 특정 회원이 특정 일정에 출석한 기록 한 건 | id | (schedule_id, user_id) 조합 |
| assignments | 특정 스터디에서 출제된 과제 한 개 | id | 없음 |
| submissions | 특정 회원이 특정 과제에 제출한 내역 한 건 | id | (assignment_id, user_id) 조합 |
## 8-4. FK 후보

```text
1. study_groups.id $\rightarrow$ memberships.group_id
   이유: 한 스터디에 여러 회원이 가입 가능 

2. schedules.id $\rightarrow$ attendances.schedule_id
   이유: 한 일정에 여러 출석 기록이 생성 될 수 있음
```

## 8-5. 자연어 관계 문장

```text
1. 한 회원은 여러 과제를 제출 할 수 있다
2.  한 회원이 여러 스터디 모임장을 맡을 수 있다
3.  
```

## 8-6. 아직 확정하지 않을 정책

```text
Q1. 탈퇴 멤버가 다시 가입하면 새로운 DB로 저장해야 하나?
Q2.과제 제출 기한을 넘길 시 데이터를 어떻게 처리 하나?
Q3.
```

---

# 9. AI를 개인 구조의 검토자로 사용

## 9-1. 사용한 프롬프트

```text
나는 데이터베이스 초보자입니다.

Chapter 02까지 학습했고 아직 ERD와 정규화는 정식으로 배우지 않았습니다.

내 서비스 구조 초안은 다음과 같습니다.
서비스 이름: [작성]

테이블 후보와 한 행 의미:
- [테이블 1 / 한 행 의미]
- [테이블 2 / 한 행 의미]
- [테이블 3 / 한 행 의미]

내부 식별자 후보:
- [작성]
업무 식별자 후보:
- [작성]
FK 후보:
- [작성]
미확정 정책:
- [작성]
정답 설계를 대신 작성하지 말고 다음을 질문 형태로 검토해 주세요.
1. DBMS / database / schema / table을 혼동한 곳
2. 한 행 의미가 모호한 곳
3. 내부 식별자와 업무 식별자를 혼동한 곳
4. PK와 FK 역할을 잘못 이해한 곳
5. FK가 필요한데 빠진 관계 후보
6. 아직 업무 담당자에게 확인해야 할 정책
근거 없이 정책을 확정하지 마세요.

```

## 9-2. AI가 질문한 내용 중 유용했던 것

```text
1. 내가 놓쳤던 부분을 바로 잡아줌
2. 에러 코드 해석을 도와줌
3. 전체 틀을 잡는데 유익
```

## 9-3. AI가 너무 빨리 결정한 내용 또는 내가 보류한 내용

```text
1. 바로 정답을 내줘 내가 학습할 기회가 날아감
2.
```

## 9-4. 검토 후 수정한 구조

| 수정 전 | 수정 후 | 수정 이유 |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |

---

# 10. 최종 개념 정리

아래 문장을 본인의 말로 완성합니다.

```text
PostgreSQL은 SQL을 사용하는 dbms이다.

DBeaver 또는 psql은 값을 받아 결과값을 확인할수 있는 곳 이다.

데이터베이스와 스키마의 차이는 데이터베이스는 정보이고  이다.

테이블 한 행은 한 명의 정보 이다.

조회 결과가 원본 테이블과 다른 이유는 조회 결과는 조건에 따라 달라지기 때문 이다.

내부 식별자와 업무 식별자의 차이는 내부 식별자는 고유의 키이지만 업무 식별자는 그 값을 받아 다른 행에도 사용하는  이다.

PK는 고유의 키(UNIQUE) 이다.

FK는 부모 행에서 자식 행에서도 사용하는 이다.
```

---

# 11. 이번 Chapter에서 새롭게 알게 된 점

최소 3개를 작성합니다.

```text
1. 조회 결과를 어떻게 하느냐에 따라 보여지는 데이터가 달라짐
2. 테이블을 만들 때는 PK가 필수
3. 
```

## 아직 헷갈리는 내용

```text
1. CRUD와 SQL
2.
```

## AI에게 다시 질문하고 싶은 내용

```text
내가 데이터 에넗리스트가 되기 위해서 지금 배우는 내용에서 어떤 점을 선택과 집중을 해야할까 단계별로 설명해줘
```

---

# 12. 제출 전 자기 점검

- [ ] PostgreSQL에서 현재 database / schema / search_path를 확인했다.
- [ ] DBMS, database, schema, table을 구분해서 설명할 수 있다.
- [ ] TEMP TABLE 3개를 생성하고 직접 데이터를 조회했다.
- [ ] 각 테이블의 한 행 의미를 작성했다.
- [ ] 테이블과 조회 결과가 다르다는 것을 실제 SQL로 확인했다.
- [ ] `ORDER BY`를 사용하지 않으면 업무 순서를 가정하면 안 된다는 점을 이해했다.
- [ ] 내부 식별자와 업무 식별자의 차이를 설명할 수 있다.
- [ ] PK 중복 입력 실패를 직접 확인했다.
- [ ] 존재하지 않는 FK 참조 실패를 직접 확인했다.
- [ ] FK 값이 반복될 수 있는 이유를 설명할 수 있다.
- [ ] AI가 만든 테이블을 내가 먼저 검토했다.
- [ ] AI 설명 중 최소 하나를 본문과 대조했다.
- [ ] 개인 서비스의 테이블 후보를 3개 이상 작성했다.
- [ ] 개인 서비스의 FK 후보와 미확정 정책을 기록했다.
- [ ] 실제 비밀번호·API Key·민감한 접속 정보가 포함되지 않았는지 확인했다.
- [ ] 이미지 링크가 GitHub에서 정상적으로 보이는지 확인했다.

---

# 13. GitHub 제출 정보

답안 파일 권장 위치:

```text
assignments/chapter02/chapter02_answer.md
```

이미지 권장 위치:

```text
assignments/chapter02/images/
```

LMS 제출 URL 형식:

```text
https://github.com/<SUNGHO19141935@GMAIL.COM>/<https://github.com/sungho19141935-cyber>/blob/main/assignments/chapter02/chapter02_answer.md
```

## 최종 확인

- [ ] 위 URL을 로그아웃 상태 또는 다른 브라우저에서 열어도 확인 가능하다.
- [ ] Markdown이 정상 렌더링된다.
- [ ] 이미지가 깨지지 않는다.
- [ ] LMS에 교수자 템플릿 URL이 아니라 **내 답안 파일 URL**을 제출했다.
