import os
from pathlib import Path

import psycopg2
import psycopg2.extras
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


def get_connection():
    return psycopg2.connect(
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        host=os.environ.get("DB_HOST", "localhost"),
        port=os.environ.get("DB_PORT", "5432"),
    )


def _row_to_dict(row):
    d = dict(row)
    d["date"] = d["date"].isoformat()
    return d


def list_expenses():
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                "SELECT id, date, category, description, amount FROM expenses ORDER BY date, id"
            )
            return [_row_to_dict(row) for row in cur.fetchall()]
    finally:
        conn.close()


def add_expense(date, category, description, amount):
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                """
                INSERT INTO expenses (date, category, description, amount)
                VALUES (%s, %s, %s, %s)
                RETURNING id, date, category, description, amount
                """,
                (date, category, description, amount),
            )
            row = _row_to_dict(cur.fetchone())
        conn.commit()
        return row
    finally:
        conn.close()


def update_expense(expense_id, date, category, description, amount):
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                """
                UPDATE expenses
                SET date = %s, category = %s, description = %s, amount = %s
                WHERE id = %s
                RETURNING id, date, category, description, amount
                """,
                (date, category, description, amount, expense_id),
            )
            row = cur.fetchone()
        conn.commit()
        return _row_to_dict(row) if row else None
    finally:
        conn.close()


def delete_expense(expense_id):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM expenses WHERE id = %s", (expense_id,))
            deleted = cur.rowcount
        conn.commit()
        return deleted > 0
    finally:
        conn.close()
