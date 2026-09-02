import csv
from pathlib import Path

import db

BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "data" / "expenses.csv"


def main():
    existing = db.list_expenses()
    if existing:
        print(f"이미 DB에 {len(existing)}건이 있습니다. 중복 이관을 막기 위해 중단합니다.")
        return

    with open(CSV_PATH, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    added = 0
    for row in rows:
        try:
            amount = int(row["amount"])
        except (KeyError, ValueError):
            print("건너뜀 (금액 오류):", row)
            continue
        db.add_expense(row["date"], row["category"], row["description"], amount)
        added += 1

    print(f"{added}건을 CSV에서 DB로 이관했습니다.")


if __name__ == "__main__": 
    main()
