# InvoiceLedger

InvoiceLedger is a starter for an offline invoice and expense tracker. It seeds a fictional invoice, line items, a partial payment, and an expense into SQLite. The command-line snapshot reports invoiced sales, payments received, outstanding balances, and expenses in EUR.

## Run the demo

With Python 3.10 or later, run these commands from the project directory.

```sh
python3 invoice_ledger.py --db demo.sqlite3 seed-demo
python3 invoice_ledger.py --db demo.sqlite3 snapshot
```

Expected totals are EUR 85.00 invoiced, EUR 30.00 received, EUR 55.00 outstanding, and EUR 12.50 in expenses. You can repeat the seed command on the same database to check that the demo stays consistent.

## Sample workbook

`examples/invoice-import.xlsx` is a fictional import fixture. Its Sales sheet includes two rows sharing an invoice reference and a third row with an intentionally invalid quantity. The valid rows represent EUR 85.00 in sales.

## Planned work

- Preview and validate Excel uploads, then save accepted rows as invoice drafts.
- Create branded PDF templates and retain an archive of issued invoices.
- Record payments, import expenses, and reconcile dashboard figures against the underlying records.

The starter uses only the Python standard library. No license is declared.
