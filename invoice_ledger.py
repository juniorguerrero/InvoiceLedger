"""Run a local InvoiceLedger demo using fictional records."""

import argparse
from contextlib import closing
from pathlib import Path
import sqlite3


SCHEMA = """
CREATE TABLE IF NOT EXISTS invoices (
    reference TEXT PRIMARY KEY,
    customer TEXT NOT NULL,
    issued_on TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS invoice_lines (
    reference TEXT NOT NULL REFERENCES invoices(reference),
    line_id TEXT NOT NULL,
    description TEXT NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_cents INTEGER NOT NULL CHECK (unit_cents >= 0),
    PRIMARY KEY (reference, line_id)
);
CREATE TABLE IF NOT EXISTS payments (
    payment_id TEXT PRIMARY KEY,
    reference TEXT NOT NULL REFERENCES invoices(reference),
    amount_cents INTEGER NOT NULL CHECK (amount_cents > 0)
);
CREATE TABLE IF NOT EXISTS expenses (
    expense_id TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    amount_cents INTEGER NOT NULL CHECK (amount_cents > 0)
);
"""


def seed_demo(db):
    with db:
        db.execute(
            "INSERT INTO invoices VALUES (?, ?, ?) ON CONFLICT DO NOTHING",
            ("DEMO-001", "Paper Lantern Studio", "2030-05-10"),
        )
        db.executemany(
            "INSERT INTO invoice_lines VALUES (?, ?, ?, ?, ?) ON CONFLICT DO NOTHING",
            [
                ("DEMO-001", "L1", "Menu design", 2, 3500),
                ("DEMO-001", "L2", "Print proof", 1, 1500),
            ],
        )
        db.execute(
            "INSERT INTO payments VALUES (?, ?, ?) ON CONFLICT DO NOTHING",
            ("PAY-DEMO-001", "DEMO-001", 3000),
        )
        db.execute(
            "INSERT INTO expenses VALUES (?, ?, ?) ON CONFLICT DO NOTHING",
            ("EXP-DEMO-001", "Paper samples", 1250),
        )


def snapshot(db):
    totals = db.execute(
        """
        SELECT (SELECT COALESCE(SUM(quantity * unit_cents), 0) FROM invoice_lines),
               (SELECT COALESCE(SUM(amount_cents), 0) FROM payments),
               (SELECT COALESCE(SUM(amount_cents), 0) FROM expenses)
        """
    ).fetchone()
    billed, received, expenses = totals
    return {
        "Invoiced": billed,
        "Payments received": received,
        "Outstanding": billed - received,
        "Expenses": expenses,
    }


def format_euros(cents):
    sign = "-" if cents < 0 else ""
    amount, remainder = divmod(abs(cents), 100)
    return f"{sign}EUR {amount:,}.{remainder:02d}"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=Path("invoice-ledger.sqlite3"))
    parser.add_argument("command", choices=("seed-demo", "snapshot"))
    args = parser.parse_args()

    with closing(sqlite3.connect(args.db)) as db:
        db.execute("PRAGMA foreign_keys = ON")
        db.executescript(SCHEMA)
        if args.command == "seed-demo":
            seed_demo(db)
        for label, cents in snapshot(db).items():
            print(f"{label}: {format_euros(cents)}")


if __name__ == "__main__":
    main()
