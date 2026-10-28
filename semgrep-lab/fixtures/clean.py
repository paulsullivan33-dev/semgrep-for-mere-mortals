"""The same little shop program, written the careful way.

The lab scans this file to show what "no findings" looks like:
the same jobs as fixtures/shop.py, with the dangerous shapes
removed.
"""

import sqlite3
import subprocess


def find_item(cursor, name):
    # The query text is fixed; the name travels separately, as
    # a parameter, and can never become part of the SQL.
    cursor.execute("SELECT price FROM items WHERE name = ?", (name,))
    return cursor.fetchone()


def run_report(path):
    # No shell: the program and its arguments stay separate.
    subprocess.call(["ls", "-l", path])
