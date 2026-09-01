import csv
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "data" / "expenses.csv"
HTML_PATH = BASE_DIR / "expense_ledger.html"
FIELDNAMES = ["date", "category", "description", "amount"]
PORT = 5050


def read_expenses():
    if not CSV_PATH.exists():
        return []
    rows = []
    with open(CSV_PATH, "r", encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            try:
                amount = int(row["amount"])
            except (KeyError, ValueError, TypeError):
                continue
            rows.append({
                "date": row.get("date", ""),
                "category": row.get("category", ""),
                "description": row.get("description", ""),
                "amount": amount,
            })
    return rows


def write_expenses(rows):
    CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CSV_PATH, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def parse_expense_payload(data):
    date = str(data.get("date", "")).strip()
    category = str(data.get("category", "")).strip()
    description = str(data.get("description", "")).strip()
    amount = int(data.get("amount"))
    if not date or not category or not description or amount <= 0:
        return None
    return {"date": date, "category": category, "description": description, "amount": amount}


class Handler(BaseHTTPRequestHandler):
    def _send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_html(self):
        if not HTML_PATH.exists():
            self.send_error(404, "expense_ledger.html not found")
            return
        body = HTML_PATH.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json_body(self):
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length) if length else b""
        return json.loads(raw.decode("utf-8")) if raw else {}

    def _expense_index_from_path(self):
        parts = urlparse(self.path).path.strip("/").split("/")
        if len(parts) != 3 or parts[0] != "api" or parts[1] != "expenses":
            return None
        try:
            return int(parts[2])
        except ValueError:
            return None

    def do_GET(self):
        path = urlparse(self.path).path
        if path in ("/", "/index.html"):
            self._send_html()
        elif path == "/api/expenses":
            self._send_json(read_expenses())
        else:
            self.send_error(404)

    def do_POST(self):
        if urlparse(self.path).path != "/api/expenses":
            self.send_error(404)
            return
        try:
            expense = parse_expense_payload(self._read_json_body())
        except (ValueError, TypeError):
            expense = None
        if expense is None:
            self._send_json({"error": "invalid payload"}, 400)
            return
        rows = read_expenses()
        rows.append(expense)
        write_expenses(rows)
        self._send_json(read_expenses())

    def do_PUT(self):
        idx = self._expense_index_from_path()
        if idx is None:
            self.send_error(404)
            return
        try:
            expense = parse_expense_payload(self._read_json_body())
        except (ValueError, TypeError):
            expense = None
        if expense is None:
            self._send_json({"error": "invalid payload"}, 400)
            return
        rows = read_expenses()
        if idx < 0 or idx >= len(rows):
            self._send_json({"error": "not found"}, 404)
            return
        rows[idx] = expense
        write_expenses(rows)
        self._send_json(read_expenses())

    def do_DELETE(self):
        idx = self._expense_index_from_path()
        if idx is None:
            self.send_error(404)
            return
        rows = read_expenses()
        if idx < 0 or idx >= len(rows):
            self._send_json({"error": "not found"}, 404)
            return
        rows.pop(idx)
        write_expenses(rows)
        self._send_json(read_expenses())


def main():
    with ThreadingHTTPServer(("127.0.0.1", PORT), Handler) as httpd:
        print(f"http://localhost:{PORT} 에서 실행 중입니다. Ctrl+C로 종료하세요.")
        httpd.serve_forever()


if __name__ == "__main__":
    main()
