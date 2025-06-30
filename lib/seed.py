from models.__init__ import CONN, CURSOR
from models.expense import Expense
from models.user import User
from models.payment import Payment

def seed_database():
    Expense.drop_table()
    User.drop_table()
    Payment.drop_table()
    User.create_table()
    Expense.create_table()
    Payment.create_table()

    sam = User.create("Sam", 100000)
    alex = User.create("Alex", 50000)
    steph = User.create("Steph", 75000)
    expense1 = Expense.create("2025-01-01", "Groceries", "Hannaford", 88.50,
                               sam.id, 0)
    expense2 = Expense.create("2025-01-01", "Home Supplies", "Amazon", 43.76,
                                 sam.id, 0)
    expense3 =Expense.create("2025-01-02", "Bar", "Diane's", 68.00, alex.id, 0)
    expense4 = Expense.create("2025-01-03", "Event", "Lincoln Center", 100.00,
                               alex.id, 0)
    expense5 = Expense.create("2025-01-05", "Restaurant", "Tosco's", 47.34, 
                              sam.id, 0)
    expense6 = Expense.create("2025-01-05", "Groceries", "Adam's", 110.14, 
                              alex.id, 0)
    expense7 = Expense.create("2025-01-05", "Home Supplies", "Adam's", 34.50,
                              steph.id, 0)

    expense1.calculate_payment([alex.id, steph.id])
    expense2.calculate_payment([alex.id])
    expense3.calculate_payment([sam.id, steph.id])
    expense4.calculate_payment([sam.id, steph.id])
    expense5.calculate_payment([steph.id])
    expense6.calculate_payment([steph.id, sam.id])
    expense7.calculate_payment([sam.id, alex.id])

seed_database()