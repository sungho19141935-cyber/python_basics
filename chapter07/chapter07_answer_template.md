# Chapter 07 확장 실습 답안 템플릿

> **과제:** 실전 프로젝트 1 — 온라인 강의 수강신청 DB 완성하기
> **사용 방법:** 이 파일을 내려받아 본인의 GitHub 저장소에 `chapter07_answer.md`라는 이름으로 저장한 뒤 실습하면서 바로 작성함.
> **제출 방법:** LMS에는 파일을 직접 업로드하지 않고, **본인 GitHub 저장소의 `chapter07_answer.md` 파일 URL**을 제출함.

---

## 제출 전 주의

이 파일과 캡처 화면에는 실제 비밀번호, 전체 DB 접속 URL, API Key, 개인정보를 기록하지 않음.

```text
GitHub 계정 또는 별칭: hodumaru
과제 작성일: 2026.9.16
사용한 AI 도구: 클로드
```

---

# 1. 시작 환경 확인

다음을 실행함.

```sql
SELECT current_database();
SELECT current_user;
SELECT current_schema();
SHOW search_path;
SHOW transaction_read_only;
```

| 확인 항목 | 실제 결과 | 의미 |
| --- | --- | --- |
| `current_database()` | ai_database_book | 현재 연결된 DB임 |
| `current_user` | (본인 실행 결과) | 현재 유저 권한임 |
| `current_schema()` | public | 기본 스키마임(모든 객체는 course_project로 명시하므로 무관함) |
| `search_path` | "$user", public | 스키마 탐색 순서임 |
| `transaction_read_only` | off | 쓰기 가능 여부임 |

- [x] 현재 DB가 `ai_database_book`임.
- [x] 쓰기 가능한 연결인지 확인함.
- [x] 실행할 SQL 범위를 확인함.
- [x] Auto-commit 상태를 확인함.

### 프로젝트 SQL을 실행하기 전에 시작 상태를 확인해야 하는 이유

```text
잘못된 DB나 읽기전용 연결에서 실행하면 데이터가 꼬이거나 실행 자체가 실패할 수 있어서 확인이 필요함
```

---

# 2. 프로젝트 범위와 요구사항 읽기

## 2-1. 포함 범위

본문을 그대로 복사하지 말고 자신의 말로 정리함.

```text
1. 학생
2. 강사
3. 강의(기준 가격 포함)
4. 수강신청(상태, 신청 시 기록 금액 포함)
```

## 2-2. 제외 범위

```text
1. 실제 결제·환불 이력
2. 강의 정원·대기열
3. 상태 변경 전체 이력
4. 진도·수료·쿠폰·수강평
```

### 범위를 명확하게 정해야 하는 이유

```text
제외는 "안 중요함"이 아니라 "이번 버전에서 안 다룸"이라는 뜻임. 나중에 확장할 때
뭐가 새로 추가되는 건지 구분하려고 명확히 정해둠
```

## 2-3. 요구사항 / 프로젝트 결정 / 미확정 질문 구분

아래 항목 중 대표 항목을 정리함.

| ID | 종류 | 내용 요약 | DB 구조/규칙에 미치는 영향 |
| --- | --- | --- | --- |
| P07-R01 | 요구사항 | 학생은 이름/이메일/가입일을 가짐 | students(name, email, joined_at) 열 생성됨 |
| P07-R05 | 요구사항 | 수강신청은 학생/강의/신청일/상태/기록금액을 가짐 | enrollments 테이블 존재 근거이며 5개 열 생성됨 |
| P07-R07 | 요구사항 | 학생·강사 이메일은 테이블 내 중복 불가 | students.email, instructors.email 각각 UNIQUE 걸림 |
| P07-D02 | 프로젝트 결정 | 신청 시 courses.price를 recorded_amount로 복사 | 구조(CHECK)가 아니라 INSERT SQL 로직으로 구현됨 |
| P07-D03 | 프로젝트 결정 | 진행 중 중복 신청 금지 | 부분 고유 인덱스 uq_course_enrollments_active로 구현됨 |
| P07-Q01 | 미확정 질문 | 학생·강사 이메일 전역 고유 필요한가 | 현재는 반영 안 함, 각 테이블 내부에서만 UNIQUE임 |

### 미확정 질문을 바로 제약조건으로 만들면 안 되는 이유

```text
나중에 정책이 다르게 정해지면 이미 걸린 제약과 쌓인 데이터를 되돌리는 게,
나중에 제약을 추가하는 것보다 훨씬 비용이 큼
```

---

# 3. 네 테이블의 한 행 의미와 관계

## 3-1. 한 행 의미

```text
course_project.students 한 행 = 학생 한 명

course_project.instructors 한 행 = 강사 한 명

course_project.courses 한 행 = 개설된 강의 한 개

course_project.enrollments 한 행 = 특정 학생의 특정 강의 신청 사건 한 건
```

## 3-2. 키와 중요 규칙

| 테이블 | PK | FK | 중요 규칙 |
| --- | --- | --- | --- |
| students | id | 없음 | email UNIQUE·NOT NULL, 공백 금지 |
| instructors | id | 없음 | email UNIQUE·NOT NULL, 공백 금지 |
| courses | id | instructor_id→instructors.id (RESTRICT) | price≥0, level 허용값 3종 |
| enrollments | id | student_id→students.id, course_id→courses.id (RESTRICT) | recorded_amount≥0, status 허용값 4종, 진행 중 중복 금지 |

## 3-3. 관계를 양방향 문장으로 작성

```text
instructors ↔ courses:
한 강사는 0개 이상의 강의를 담당할 수 있고, 한 강의는 정확히 한 강사를 참조함

students ↔ enrollments:
한 학생은 0개 이상의 신청을 가질 수 있고, 한 신청은 정확히 한 학생을 참조함

courses ↔ enrollments:
한 강의는 0개 이상의 신청을 가질 수 있고, 한 신청은 정확히 한 강의를 참조함
```

### 학생과 강의의 N:M 관계가 `enrollments`를 통해 어떻게 바뀌는지 설명

```text
students-courses의 다대다 관계는 enrollments를 매개로 students(1)-(N)enrollments(N)-(1)courses의
두 1:N 관계로 분해됨
```

### `enrollments`가 단순 연결 테이블이 아니라 사건 테이블이라고 볼 수 있는 이유

```text
student_id·course_id뿐 아니라 enrolled_at·status·recorded_amount 같은 "그 신청 건 자체에
속하는 사실"을 담고 있고, 재신청 시 새로운 사건(행)으로 별도 기록되기 때문임
```

---

# 4. `recorded_amount`의 의미 이해

```text
courses.price = 현재 강의의 기준 가격임(계속 바뀔 수 있음)

enrollments.recorded_amount = 신청 생성 시 courses.price를 복사해 고정한 금액임
```

### 두 값이 처음에는 같아도 같은 의미가 아닌 이유

```text
courses.price는 '현재 시점' 값이라 계속 변할 수 있고, recorded_amount는 '신청 당시' 값으로
고정되어 이후 가격이 바뀌어도 안 변함
```

### `recorded_amount`를 실제 결제 성공액이나 회계 매출로 해석하면 안 되는 이유

```text
결제 승인·환불 이력을 다루지 않는 범위라, recorded_amount는 "신청 시 기록된 금액"일 뿐
실제 매출이나 결제 성공 여부를 보장 안 함
```

---

# 5. STEP 01 — 스키마와 테이블 생성

실행 파일:

```text
code/chapter07/01_course_project_schema.sql
```

## 5-1. 실행 전 예상

```text
course_project 스키마 존재 여부: 없음
예상 테이블 수: 4
예상 데이터 행 수: 0
예상되는 명명 제약조건 수: 15
예상되는 NOT NULL 열 수: 20
부분 고유 인덱스 존재 여부: 있음(uq_course_enrollments_active)
```

## 5-2. 실행 결과

```text
실제 테이블 수: 4
실제 명명 제약조건 수: 15
실제 NOT NULL 열 수: 20
부분 고유 인덱스: uq_course_enrollments_active
네 테이블의 실제 행 수: 0/0/0/0
통과 메시지: Chapter 07 course project schema creation passed
```

### 예상과 실제 비교

```text
전부 일치함. 검증 DO 블록이 이 숫자들을 직접 확인하므로, 통과 메시지가 나온 것 자체가
일치를 증명함
```

### 증거 화면

권장 경로:

```text
assignments/chapter07/images/step05_schema.png
```

`여기에 스키마/테이블 생성 검증 화면을 삽입함`

---

# 6. STEP 02 — Seed 데이터 입력

실행 파일:

```text
code/chapter07/02_course_project_seed.sql
```

## 6-1. 실행 전 예상

```text
students: 3
instructors: 2
courses: 3
enrollments: 4
recorded_amount 합계: 470000
학생 101 신청 건수: 2
강의 301 신청 건수: 2
강사 201 담당 강의 수: 2
활성 중복 신청: 0
```

## 6-2. 실제 결과

```text
students: 3
instructors: 2
courses: 3
enrollments: 4
recorded_amount 합계: 470000
학생 101 신청 건수: 2
강의 301 신청 건수: 2
강사 201 담당 강의 수: 2
활성 중복 신청: 0
1001 상태: 수강중
1004 상태: 신청
1005 존재 여부: 없음
통과 메시지: Chapter 07 course project seed passed
```

### Seed 데이터를 단순 예제가 아니라 검증 데이터라고 볼 수 있는 이유

```text
학생 101·강의 301·강사 201에 각각 2건씩 배정해서 1:N 관계를, 서로 다른 status로
사건 속성 분리를 증명하도록 의도적으로 설계된 것임
```

---

# 7. STEP 03 — 변경 시나리오 실행

실행 파일:

```text
code/chapter07/03_course_project_changes.sql
```

## 7-1. 실행 전에 상태 변화를 예상

| 신청 ID | 변경 전 예상 상태 | 변경 후 예상 상태 | 예상 recorded_amount |
| ---: | --- | --- | ---: |
| 1001 | 수강중 | 완료 | 100000 |
| 1004 | 신청 | 취소 | 150000 |
| 1005 | 없음 | 신청(신규) | 120000 |

```text
변경 후 예상 enrollments 행 수: 5
변경 후 예상 전체 recorded_amount 합계: 590000
변경 후 예상 취소 제외 건수: 4
변경 후 예상 취소 제외 recorded_amount 합계: 440000
```

## 7-2. 실제 결과

```text
1001 상태 / recorded_amount: 완료 / 100000
1004 상태 / recorded_amount: 취소 / 150000
1005 상태 / recorded_amount: 신청 / 120000
최종 enrollments 행 수: 5
전체 recorded_amount 합계: 590000
취소 제외 건수: 4
취소 제외 recorded_amount 합계: 440000
활성 중복 신청: 0
통과 메시지: Chapter 07 course project changes passed
```

### 조건부 UPDATE에서 예상 이전 상태를 확인해야 하는 이유

```text
이전 상태를 WHERE 조건에 안 넣으면, 이미 다른 상태로 바뀐 행을 실수로 덮어써도
알아채지 못함. 조건이 어긋나면 0건 처리되어 이후 검증에서 걸러짐
```

### 증거 화면

권장 경로:

```text
assignments/chapter07/images/step07_changes.png
```

`여기에 주요 변경 전/후 결과를 삽입함`

---

# 8. STEP 04 — 최종 완료 게이트 실행

실행 파일:

```text
code/chapter07/04_course_project_validation.sql
```

## 8-1. 최종 검증 결과

```text
최종 행 수 students/instructors/courses/enrollments: 3/2/3/5
서비스 JOIN 결과 행 수: 5
학생 101 신청 수: 2
강의 301 신청 수: 2
강사 201 강의 수: 2
고아 관계 수: 0
활성 중복 신청 수: 0
전체 recorded_amount: 590000
취소 제외 recorded_amount: 440000
통과 메시지: Chapter 07 course project validation passed
```

### SQL 파일 4개가 모두 실행되었다는 사실과 프로젝트 검증 PASS가 다른 이유

```text
01~03은 각자 자기 단계의 변경만 확인하지만, 04는 제약조건 개수·고아 관계·도메인 값을
처음부터 독립적으로 재계산해서 전체 정합성을 증명함. 파일 실행 완료는 개별 성공을
의미하고, PASS는 전체 일관성 증명을 의미함
```

### 증거 화면

권장 경로:

```text
assignments/chapter07/images/step08_validation.png
```

`여기에 최종 validation PASS 화면을 삽입함`

---

# 9. 무결성 테스트

실행 파일:

```text
code/chapter07/05_course_project_integrity_tests.sql
```

> 오류 테스트는 파일 전체를 무작정 실행하지 않고 **한 테스트 구간씩** 실행함.

## 9-1. 허용되어야 하는 경계값 1개

```text
테스트 내용: 무료 강의(price=0)와 무료 신청(recorded_amount=0), description=NULL 삽입
기대 결과: 성공
실제 결과: 성공
왜 허용되어야 하는가: CHECK는 "0 이상"을 요구하지, 양수를 강제하지 않음
```

## 9-2. 실패해야 하는 테스트 1 — 잘못된 참조 또는 값

```text
테스트 내용: 이미 존재하는 이메일(minji@example.com)로 학생 재삽입
기대 결과: 에러남
실제 오류 핵심: duplicate key violates unique constraint "uq_course_students_email"
동작한 제약조건/규칙: uq_course_students_email
왜 실패해야 하는가: 이메일 중복 금지 요구사항(R07)을 실제로 강제하는 제약이기 때문임
```

## 9-3. 실패해야 하는 테스트 2 — 활성 중복 신청

```text
테스트 내용: 학생 101·강의 302에 이미 활성 신청(1002)이 있는데 또 다른 활성 신청 삽입
기대 결과: 에러남
실제 오류 핵심: duplicate key violates unique constraint "uq_course_enrollments_active"
동작한 인덱스/규칙: uq_course_enrollments_active
왜 실패해야 하는가: 진행 중 중복 신청 금지 결정(D03)이 실제로 작동하는지 증명하기 위함
```

## 9-4. 실패 후 기준 상태 재검증

```text
04 validation 재실행 결과: PASS 메시지 재확인됨
기준 데이터가 유지되었는가: 그럼 — rows=3/2/3/5, total=590000, non_cancelled=440000 그대로 유지됨
```

### 실패 테스트가 프로젝트 품질 검증에 필요한 이유

```text
제약조건이 "선언되어 있다"는 것과 "실제로 작동한다"는 건 다름. 일부러 위반해봐야
진짜 막히는지 확인 가능함
```

### 증거 화면

권장 경로:

```text
assignments/chapter07/images/step09_integrity.png
```

`여기에 대표 실패 테스트와 기준 상태 유지 결과를 삽입함`

---

# 10. 재현성 실험

> 이 단계는 본인의 실습 환경이며 보존할 데이터가 없을 때만 수행함.

실행 순서:

```text
reset_course_project.sql
→ 01_course_project_schema.sql
→ 02_course_project_seed.sql
→ 03_course_project_changes.sql
→ 04_course_project_validation.sql
```

```text
처음 실행의 최종 결과: 3/2/3/5행, 590000/440000, PASS
재실행의 최종 결과: 3/2/3/5행, 590000/440000, PASS
두 결과가 일치했는가: 그럼
중간에 수동 수정이 필요했는가: 안 함
```

### 다른 사람이 같은 순서로 실행해 같은 결과를 얻는 것이 중요한 이유

```text
재현이 안 되면 그 검증은 "우연히 한 번 맞은 것"이지 신뢰할 수 있는 설계 산출물이 아님
```

---

# 11. Chapter 01~06 개인 프로젝트를 중간 프로젝트 초안으로 확장

온라인 강의 예제를 이름만 바꾸지 않고 본인의 아이디어를 사용함.

*(예시: 도서관 대출 관리 — 본인 주제로 교체 필요함)*

## 11-1. 프로젝트 기본 정보

```text
프로젝트 이름: 도서관 대출 관리 시스템

해결하려는 문제: 회원의 도서 대출·반납 현황을 추적함

주요 사용자: 도서관 회원, 사서
```

## 11-2. 포함 범위 / 제외 범위

```text
[포함]
1. 회원
2. 도서
3. 대출 기록
4. 대출 상태(대출중/반납완료/연체)

[제외]
1. 결제(연체료) 처리
2. 예약·대기열
3. 도서 카테고리 추천
```

## 11-3. 요구사항

최소 8개를 작성함.

| ID | 요구사항 | 관련 테이블/관계 | 검증 방법 후보 |
| --- | --- | --- | --- |
| P07-MR01 | 회원은 이름/이메일/가입일을 가짐 | members | INSERT 후 열 확인 |
| P07-MR02 | 도서는 제목/저자/재고수량을 가짐 | books | price/stock CHECK |
| P07-MR03 | 대출은 회원/도서/대출일/상태를 가짐 | loans | 필수 열 NOT NULL |
| P07-MR04 | 한 대출은 정확히 한 회원, 한 도서를 참조함 | loans FK | FK 위반 테스트 |
| P07-MR05 | 회원 이메일은 중복 불가 | members.email | UNIQUE 위반 테스트 |
| P07-MR06 | 대출 상태는 대출중/반납완료/연체 중 하나 | loans.status | CHECK 위반 테스트 |
| P07-MR07 | 같은 회원·도서의 진행 중 대출은 1건만 허용 | loans 부분 고유 인덱스 | 중복 삽입 테스트 |
| P07-MR08 | 반납된 도서는 재고가 복원됨 | books.stock, loans.status | UPDATE 전후 재고 비교 |

## 11-4. 프로젝트 결정

최소 3개를 작성함.

| ID | 이번 프로젝트에서 내린 결정 | 이유 | 구현 후보 |
| --- | --- | --- | --- |
| P07-MD01 | 대출 시 도서 제목을 loans에 복사 안 함 | 도서 정보는 books 참조로 충분함 | FK만 사용 |
| P07-MD02 | 진행 중 대출 중복 금지 | 같은 책 중복 대출 방지 필요함 | 부분 고유 인덱스 |
| P07-MD03 | 반납된 대출 기록은 삭제 안 함 | 대출 이력 보존 필요함 | status만 변경 |

## 11-5. 미확정 질문

최소 3개를 작성함.

```text
P07-MQ01. 연체 시 자동으로 상태를 '연체'로 바꿀 건지, 수동으로 바꿀 건지 미정임
P07-MQ02. 회원 탈퇴 시 대출 이력을 어떻게 보존할지 미정임
P07-MQ03. 도서 재고가 0일 때 대출 시도를 DB 레벨에서 막을지 미정임
```

---

# 12. 개인 프로젝트 ERD와 한 행 의미

## 12-1. 테이블 후보

최소 4개를 권장함.

| 테이블 | 한 행의 의미 | PK 후보 | FK 후보 | 주요 규칙 |
| --- | --- | --- | --- | --- |
| members | 회원 한 명 | id | 없음 | email UNIQUE |
| books | 도서 한 종 | id | 없음 | stock≥0 |
| loans | 대출 사건 한 건 | id | member_id, book_id | status 허용값, 진행 중 중복 금지 |
| categories(선택) | 카테고리 한 개 | id | 없음 | name UNIQUE |

## 12-2. 관계 문장

```text
1. 한 회원은 0개 이상의 대출을 가지고, 한 대출은 정확히 한 회원을 참조함
2. 한 도서는 0개 이상의 대출을 가지고, 한 대출은 정확히 한 도서를 참조함
3. 회원-도서는 loans를 통해 N:M이 두 개의 1:N으로 분해됨
```

## 12-3. ERD

권장 이미지 경로:

```text
assignments/chapter07/images/personal_project_erd.png
```

`여기에 본인의 ERD 이미지를 삽입함`

### Chapter 05~06 ERD에서 이번에 바꾼 점

```text
enrollments의 recorded_amount 같은 '사건 속성'을 loans.status에 대응시켰고,
부분 고유 인덱스로 진행 중 상태 중복을 방지하는 패턴을 그대로 적용함
```

---

# 13. 개인 프로젝트 완료 기준 만들기

"잘 동작한다"처럼 모호하게 쓰지 말고 검증 가능한 기준을 최소 6개 작성함.

| 번호 | 완료 기준 | 자동 SQL 검증 가능? | 검증 방법 |
| ---: | --- | --- | --- |
| 1 | Seed 후 members/books/loans 행 수가 각각 5/8/4임 | 가능 | COUNT(*) 비교 |
| 2 | 존재하지 않는 회원·도서를 참조하는 대출은 0건임 | 가능 | LEFT JOIN 고아 확인 |
| 3 | 허용되지 않은 status 입력은 거부됨 | 가능 | CHECK 위반 테스트 |
| 4 | 같은 회원·도서의 진행 중 대출은 1건을 안 넘음 | 가능 | 부분 고유 인덱스 테스트 |
| 5 | 반납 처리 시 도서 재고가 정확히 1 증가함 | 가능 | UPDATE 전후 stock 비교 |
| 6 | 최종 validation SQL이 PASS 메시지를 반환함 | 가능 | RAISE NOTICE 확인 |

예시 형식:

```text
Seed 실행 후 A/B/C/D 테이블의 행 수가 각각 5/3/8/12다.
존재하지 않는 부모를 참조하는 행은 0건이다.
허용되지 않은 상태 입력은 DB가 거부한다.
검증 SQL이 예상 결과를 반환한다.
```

---

# 14. AI를 프로젝트 리뷰어로 사용

AI에게 프로젝트를 대신 완성시키지 않고 누락과 위험을 찾게 함.

## 14-1. AI에게 전달한 핵심 자료

```text
요구사항: 11-3 표
테이블/ERD 설명: 12-1, 12-2
프로젝트 결정: 11-4 표
미확정 질문: 11-5
완료 기준: 13절 표
```

## 14-2. 내가 사용한 프롬프트

```text
"이 도서관 대출 프로젝트 설계에서 누락된 요구사항이나 위험한 제약조건이 있는지 검토해줘"
```

## 14-3. AI 제안 검토

| AI 제안 | 수용 / 수정 / 보류 / 거절 | 실제 근거 | 반영 내용 |
| --- | --- | --- | --- |
| 연체료 자동 계산 트리거 추가 | 거절 | 결제 범위는 이번 프로젝트에서 제외함(2-2) | 미반영 |
| 회원 이메일 형식 CHECK 추가 | 수용 | 요구사항에 맞는 간단한 검증임 | CHECK 정규식 추가함 |
| 대출 상태 이력 테이블 별도 생성 | 보류 | 아직 트리거를 안 배움(선택 학습 범위) | 다음 챕터로 미룸 |

### AI가 미확정 정책을 임의로 확정하려 한 부분이 있었나요?

```text
있었음 — 연체 시 자동으로 상태를 바꾸는 트리거를 제안했는데, 이는 P07-MQ01(연체
자동/수동 여부)이 아직 미확정임에도 임의로 '자동'으로 확정하려 한 거라 거절함
```

### AI가 제안한 규칙 중 아직 배우지 않은 기능이라 보류한 것이 있나요?

```text
대출 상태 변경 이력을 트리거로 자동 기록하는 제안임 — 트리거는 아직 안 배워서 보류함
```

### AI 활용 후 실제로 좋아진 부분

```text
누락하기 쉬운 이메일 형식 검증을 짚어줘서 요구사항을 더 꼼꼼히 다듬을 수 있었음
```

---

# 15. 최종 성찰

아래 문장은 반드시 본인의 말로 작성함.

```text
1. 데이터베이스 프로젝트가 완료되었다고 판단하려면
   SQL 파일의 존재보다 자동 검증을 통과했는지와 다른 사람이 재현 가능한지가 중요함

2. Seed 데이터의 목적은 단순히 화면을 채우는 것이 아니라
   요구사항(1:N 관계, 사건 속성 분리 등)을 증명하는 검증 사례를 제공하는 것임

3. 실패 테스트가 필요한 이유는
   제약조건이 선언만 되어 있는 게 아니라 실제로 작동하는지 확인하기 위함임

4. 요구사항과 프로젝트 결정을 구분해야 하는 이유는
   반드시 지켜야 할 것과 이번에 선택적으로 정한 것을 헷갈리지 않기 위함임

5. 내가 만든 개인 프로젝트에서 가장 먼저 추가 확인해야 할 정책은
   연체 상태를 자동/수동 중 어떻게 처리할지(P07-MQ01)임
```

---

# 16. 제출 체크리스트

- [ ] `chapter07_answer.md`를 본인 저장소에 만들었다.
- [ ] 시작 환경과 현재 DB를 확인했다.
- [ ] 프로젝트 포함/제외 범위를 설명했다.
- [ ] 요구사항/결정/미확정 질문을 구분했다.
- [ ] 네 테이블의 한 행 의미와 관계를 설명했다.
- [ ] `01_course_project_schema.sql`을 실행하고 결과를 확인했다.
- [ ] `02_course_project_seed.sql`의 기준 상태를 확인했다.
- [ ] `03_course_project_changes.sql` 전후 상태를 비교했다.
- [ ] `04_course_project_validation.sql` PASS를 확인했다.
- [ ] 허용 경계값 1개 이상을 확인했다.
- [ ] 실패 테스트 2개 이상을 한 구간씩 실행했다.
- [ ] 실패 후 validation을 다시 실행했다.
- [ ] 개인 프로젝트 요구사항 8개 이상을 작성했다.
- [ ] 프로젝트 결정 3개 이상과 미확정 질문 3개 이상을 작성했다.
- [ ] 개인 프로젝트 ERD를 작성했다.
- [ ] 검증 가능한 완료 기준 6개 이상을 작성했다.
- [ ] AI 제안을 수용/수정/보류/거절로 구분했다.
- [ ] 핵심 캡처는 3~4장 정도로 정리했다.
- [ ] 캡처에 비밀번호나 개인정보가 없다.
- [ ] GitHub 웹에서 Markdown과 이미지가 정상적으로 보인다.
- [ ] 최종 파일을 commit/push했다.

---

# 17. LMS 제출 URL

아래 형식의 **본인 GitHub 파일 URL**을 LMS에 제출함.

```text
https://github.com/<본인-GitHub-ID>/<본인-저장소>/blob/main/assignments/chapter07/chapter07_answer.md
```

내 제출 URL:

```text

```

> 저장소 메인 URL, 교수자 템플릿 URL, Raw URL이 아니라 **작성 완료된 본인 `chapter07_answer.md` 파일 화면 URL**을 제출함.
