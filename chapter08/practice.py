# chapter 09

# LEVEL 1. 조건식부터 True/False를 맞혀라
#다음 코드를 실행하지 말고 각 조건식의 결과와 출력 여부를 예상하세요.

score = 75
if score >= 60:
    print("PASS")
if score > 80:
    print("HIGH")
if score != 75:
    print("DIFFERENT")

# 정답은 if문 가장 윗 줄에 해당되기 때문에 "PASS"가 나올 것 

# ----------------------------------------------------------------------------

#LEVEL 2. 경계값 세 개로 조건을 검증하라
# 다음 두 조건을 비교합니다
'''
age = 18
if age >= 18:
    print("입장 가능")

age = 18
if age > 18:
    print("입장 가능")
'''
# 아래 코드는 18세 초과부터 되기 때문에 18세는 입장 불가임

# ------------------------------------------------------------------------------

# LEVEL 3. if-else 두 갈래를 모두 실행해 보라

score = 55

if score >= 60:
    print("통과입니다.")
else:
    print("다시 도전하세요.")
# 결과는 "다시 도전하세요"

# 30도 이상 → "더워요!"
# 30도 미만 → "선선해요!"

temperature = 29

if temperature <= 30:
    print("더워요!")
else:
    print("시원해요")

# ---------------------------------------------------------------------

# LEVEL 4. if-elif-else에서 조건 순서를 설계하라
score = 95

if score >= 60:
    print("D 이상")
elif score >= 70:
    print("C 이상")
elif score >= 80:
    print("B 이상")
elif score >= 90:
    print("A")
else:
    print("F")
# 가장 좁은 범위를 위에 설정해야 함

# ----------------------------------------------------------------------
# LEVEL 5. and, or, not으로 조건을 설계하라
age = 22
has_ticket = True

# 20세 이상이고 티켓이 있으면 → "입장 가능"
# 그렇지 않으면 → "입장 불가"

if age >=20 and has_ticket:
    print ("입장 가능")
else:
    print("입장 불가")

# -----------------------------------------------------------------------

#LEVEL 10. DECISION BOSS CHALLENGE — 요구사항을 조건으로 설계하라
'''
1. 점수가 90 이상이고 출석률이 90 이상이며 과제를 제출했다면
   → "우수 수료"

2. 그렇지 않지만 점수가 60 이상이고 출석률이 80 이상이며 과제를 제출했다면
   → "수료"

3. 나머지는
   → "미수료"
'''

namme = input("이름 : ")
score = int(input("점수 : "))
date_per = float(input("출석률 :"))
homework = input("과제 제출 여부 : (y/n)").lower()

if score >= 90 and date_per >= 80 and homework == "y":
    print ("우수 수료")
elif score >= 60 and date_per >= 80 and homework == "y":
    print ("수료")
else:
    print("미수료")