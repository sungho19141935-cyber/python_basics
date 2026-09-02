import db


def add_expense(expenses):  # 사용자 입력을 받아 지출 1건을 DB에 추가하고 expenses 리스트에도 반영한다.
    date = input("날짜(YYYY-MM-DD): ").strip()
    category = input("카테고리: ").strip()
    description = input("내용: ").strip()

    # 1차 검증: 필수 문자열 항목이 비어 있는지 확인
    if not date or not category or not description:
        print("날짜, 카테고리, 내용은 비워 둘 수 없습니다.")
        return

    # 2차 검증: 금액이 정수로 변환되는지 확인 (예: "만원"처럼 숫자가 아닌 입력 방지)
    try:
        amount = int(input("금액: "))
    except ValueError:
        print("금액은 정수로 입력해 주세요.")
        return

    # 3차 검증: 정수 변환은 되지만 요구사항에 맞지 않는 값(0 이하) 방지
    # int() 실패(ValueError)와는 성격이 다른 문제라서 별도 조건문으로 분리
    if amount <= 0:
        print("금액은 0보다 큰 값으로 입력해 주세요.")
        return

    # CSV 버전과 다르게, 여기서 바로 DB에 INSERT한다 (메모리에만 쌓아두지 않음).
    expense = db.add_expense(date, category, description, amount)
    expenses.append(expense)
    print("지출 내역을 추가했습니다.")


def show_expenses(expenses):  # expenses 리스트 전체를 번호를 매겨 출력한다.
    if not expenses:
        print("등록된 지출이 없습니다.")
        return

    print("\n=== 지출 내역 ===")
    number = 1
    for expense in expenses:
        print(
            f"{number}. {expense['date']} | "
            f"{expense['category']} | "
            f"{expense['description']} | "
            f"{expense['amount']:,}원"
        )
        number += 1


def calculate_total(expenses):  # 모든 지출 amount를 더한 전체 합계를 반환한다.
    total = 0
    for expense in expenses:
        total += expense["amount"]
    return total


def calculate_by_category(expenses):  # 카테고리별로 amount를 누적한 딕셔너리를 반환한다.
    # 예: {"식비": 12000, "교통": 1500}
    category_totals = {}
    for expense in expenses:
        category = expense["category"]
        amount = expense["amount"] 
        if category in category_totals:
            category_totals[category] += amount
        else:
            category_totals[category] = amount
    return category_totals


def main():
    # 프로그램 시작 시 DB에 저장된 지출을 불러와서 이어서 작업할 수 있게 한다.
    expenses = db.list_expenses()

    while True:
        print("\n=== 개인 지출 관리 ===")
        print("1. 지출 추가")
        print("2. 지출 목록")
        print("3. 지출 요약")
        print("4. 새로고침 (DB에서 다시 불러오기)")
        print("0. 종료")
        choice = input("메뉴 선택: ").strip()

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            show_expenses(expenses)
        elif choice == "3":
            # 전체 합계와 카테고리별 합계를 함께 보여준다.
            print("전체 지출:", calculate_total(expenses))
            print(calculate_by_category(expenses))
        elif choice == "4":
            # DB는 추가할 때마다 바로 저장되므로, 따로 "저장"할 게 없다.
            # 대신 웹페이지 등 다른 곳에서 바뀐 내용을 다시 불러오는 용도로 바꿨다.
            expenses = db.list_expenses()
            print("DB에서 다시 불러왔습니다.")
        elif choice == "0":
            break
        else:
            print("메뉴 번호를 다시 선택해 주세요.")


if __name__ == "__main__":
    main()

    db_rows = db.list_expenses()
    import pandas as pd

    df = pd.DataFrame(db_rows)
    print("전체 지출:", df["amount"].sum())
    print(df.groupby("category")["amount"].sum())
