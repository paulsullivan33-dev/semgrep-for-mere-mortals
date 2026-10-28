"""A tiny stock program for a fictional corner shop.

Written for this guide's lab. It is deliberately full of the
kind of mistakes the lab's rules look for. Do not copy any of
it into a real program.
"""

import hashlib
import sqlite3
import subprocess

# A password written straight into the source code.
DB_PASSWORD = "s3cret-shop-password"


def find_item(cursor, name):
    # The query is built by gluing the caller's text into the SQL.
    query = "SELECT price FROM items WHERE name = '%s'" % name
    cursor.execute(query)
    return cursor.fetchone()


def search(cursor):
    # Text typed by a person flows straight into a query.
    name = input("Item name: ")
    cursor.execute("SELECT price FROM items WHERE name = '" + name + "'")
    return cursor.fetchone()


def run_report(command):
    # The shell is asked to make sense of one long string.
    subprocess.call("ls -l " + command, shell=True)


def hash_password(password):
    # MD5 is far too fast to protect a password.
    return hashlib.md5(password.encode()).hexdigest()


def calculate(expression):
    # eval() will happily run anything it is handed.
    return eval(expression)


def add(a, b):
    # Nothing wrong here. A good rule leaves this line alone.
    return a + b
