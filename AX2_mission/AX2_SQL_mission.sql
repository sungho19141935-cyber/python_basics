-- =========================================================
-- Part 1. 기본 CRUD (입력 / 조회 / 수정 / 삭제)
-- =========================================================

insert into  practice1.members
(name, email, age, joined_at)
VALUES
	('김민수','minsu@example.com',25,'2026-08-01'),
	('김소은','soeun@example.com',29,'2026-05-20'),
	('박채린','chae@example.com',31,'2026-11-11'),
	('김성호','sungho@example.com',20,'2026-10-09'),
	('이형석','mama@example.com',28,'2026-03-15');

SELECT*FROM practice1.members;

select name, email
from practice1.members;

select *
from practice1.members
where age <= 25;

select *
from practice1.members
where name in ('김민수');

select *
from practice1.members
order by age desc;

select *
from practice1.members
order by joined_at asc;

UPDATE practice1.members
SET age = 30
WHERE member_id = 1;

delete FROM practice1.members
WHERE member_id = 5;


-- =========================================================
-- Part 2. 집계 함수 / 그룹화 / 서브쿼리 / 개념 정리
-- =========================================================

select count (*)
from practice1.members;

select avg(age) as average_age
from practice1.members;

select max(age) as max_age
from practice1.members;

select min(age) as min_age
from practice1.members;

select (age / 10) * 10 AS age_group,
       COUNT(*) AS member_count
from members
group by (age / 10) * 10
order by age_group;

select *
from practice1.members
order by joined_at desc
limit 1;

select *
from members
where age > (select  avg(age) from members);

select *
from members
where email = 'soeun@example.com';

select *
from members
where age >= 20
	and name like '김%';


-- ---------------------------------------------------------
-- 개념 정리 질문 (서술형)
-- ---------------------------------------------------------

PRIMARY KEY는 왜 필요한가요?
- 테이블 내 모든 행을 서로 식별을 위함

WHERE 없이 UPDATE 또는 DELETE를 실행하면 어떤 문제가 발생할 수 있나요?
- 모든 데이터에 해당 돼 아주 위험

SELECT *와 필요한 컬럼만 선택하는 SQL의 차이는 무엇인가요?
- * 은 모든 컬럼을 가져오는 방식이고, 특정 컬럼만 지정하면 그 데이터만 골라 조회

COUNT()와 AVG()는 각각 어떤 값을 계산하나요?
- 갯수와 평균

Python에서 데이터를 처리하는 것과 DB에서 SQL로 데이터를 조회하는 것의 차이를 어떻게 이해했나요?
- 다수가 사용하시 위해선 SQL이 필수적이라 생각
