#!/usr/bin/env python3
# lib/debug.py

from __init__ import CONN, CURSOR
from expense import Expense
from user import User
import ipdb

def reset_database():
    Expense.drop_table()
    User.drop_table()
    User.create_table()
    Expense.create_table()

    sam = User.create("Sam", 100000)
    alex = User.create("Alex", 50000)
    Expense.create("2025-01-01", "Groceries", "Hannaford", 88.50, sam.id, alex.id, 0)
    Expense.create("2025-01-01", "Home Supplies", "Amazon", 43.76, sam.id, alex.id, 0)
    Expense.create("2025-01-02", "Bar", "Diane's", 68.00, alex.id, sam.id, 0)
    Expense.create("2025-01-03", "Event", "Lincoln Center", 100.00, alex.id, sam.id, 0)
    Expense.create("2025-01-05", "Restaurant", "Tosco's", 47.34, sam.id, alex.id, 0)
    Expense.create("2025-01-05", "Groceries", "Adam's", 110.14, alex.id, sam.id, 0)

reset_database()
ipdb.set_trace()
