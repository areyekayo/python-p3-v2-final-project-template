# lib/helpers.py
from models.expense import Expense
from models.user import User
from models.payment import Payment

def list_users():
    users = User.get_all()
    for user in users: 
        print(f'{user.id}: {user.name}, income: ${user.income}')

def find_user_by_name():
    name = input("Enter a user's name: ")
    user = User.find_by_name(name)
    print(f"Found {user.name}, income: {user.income}") if user else print(
        f'User {name} not found\n'
    )
    return user

def find_user_by_id(user_id):
    user = User.find_by_id(user_id)
    print(f"Found {user.name}, income: {user.income}") if user else print(
        f"User not found"
    )
    return user

def create_user():
    name = input("Enter the new user's name: ")
    income = input("Enter the user's yearly income as a whole number: ")
    try:
        user = User.create(name, income)
        print(f'Success: {user}\n')
    except Exception as exc:
        print(f'Error creating the user: {exc}\n')

def update_user(user):
    try:
        name = input("Enter the user's new name: ")
        user.name = name
        income = input("Enter the user's new income: ")
        user.income = income
        print(f"Successfully updated user: {user.name}, income: {user.income}")
        user.update()
    except Exception as exc:
        print(f'Error updating user: {exc}\n')

def delete_user(user_id):
    if user := User.find_by_id(user_id):
        user.delete()
        print(f'User {user.name} deleted\n')
    else: print(f'User not found \n')


def get_user_expenses(user_id):
    if user := User.find_by_id(user_id):
        expenses = user.expenses()
        print(f"Listing {user.name}'s expenses: ")
        for expense in expenses:
            print(f'    Date: {expense.purchase_date}, Category: {expense.purchase_category}, Store: {expense.store}, Amount: {expense.expense_amount}, Payer: {user.name}, Settled: {bool(expense.is_settled)}, Settled Date: {expense.settled_date}' )
    else: print(f'User not found\n')

def enter_expense(payer_id=None):
    purchase_date = input("Enter the purchase date: ")
    purchase_category = input("Enter the purchase category (Groceries, Restaurant, Home Supplies, Event, Bar): ")
    store = input("Enter the store where purchase was made: ")
    expense_amount = input("Enter the expense amount (ex 12.34): ")

    if payer_id == None:
        name = input("Enter the user name who paid for the expense: ")
        user = User.find_by_name(name)
    else:
        user = User.find_by_id(payer_id)

    expense = Expense.create(purchase_date, purchase_category, store, expense_amount, user.id, is_settled=0)

    print(f"Successfully created new expense by {user.name}: {expense.purchase_date}, {expense.purchase_category}, {expense.store}, {expense.expense_amount}")

    while True:
        print(f"Enter the names of users who will pay {user.name} back for this expense, separated by commas: ")
        ower_input = input("> ")
        try: 
            ower_names = [item.strip() for item in ower_input.split(',')]
            owers = [User.find_by_name(ower) for ower in ower_names]
            expense.calculate_payment([ower.id for ower in owers])
            return expense
        except: 
            ValueError("Ower names must be separated by a comma and space")
    
def get_user_owed_payments(ower_id=None):
    """Gets payments that are owed by payer_id"""
    if ower_id == None:
        name = input("Enter the name of the person who owes payments")
        ower = User.find_by_name(name)
    else:
        ower = User.find_by_id(ower_id)
    payments = ower.get_owed_payments()

    if len(payments) == 0:
        print(f"{ower.name} has no owed payments!")
        return None
    else:
        print(f"{ower.name} has {len(payments)} unpaid payments: ")
        for payment in payments:
            recipient = User.find_by_id(payment.recipient_id)
            expense = Expense.find_by_id(payment.expense_id)
            print(f"    {payment.id}: {ower.name} owes {recipient.name} ${payment.payment_amount} for {expense.purchase_category} purchase at {expense.store}")
    
    return payments

def make_payment(payment_id):
    if payment := Payment.find_by_id(payment_id):
        payment.settle_payment()
        recipient = User.find_by_id(payment.recipient_id)
        ower = User.find_by_id(payment.ower_id)
        print(f"Success: {ower.name} paid {recipient.name} ${payment.payment_amount}")
    else: print(f"Payment not found")

def list_unsettled_expenses():
    expenses = Expense.find_unsettled_expenses()
    for expense in expenses:
        payer = User.find_by_id(expense.payer_id)
        print(f"{expense.id}: {payer.name} made purchase at {expense.store} on {expense.purchase_date} for ${expense.expense_amount}")

def find_expense_by_id(expense_id):
    expense = Expense.find_by_id(expense_id)
    print(expense) if expense else print("Expense not found")
    return expense


def update_expense(expense):
    try:
        purchase_date = input("Enter the expense's purchase date:")
        purchase_category = input("Enter the purchase category (Groceries, Restaurant, Home Supplies, Event, Bar): ")
        store = input("Enter the store where the purchase was made: ")
        expense_amount = input("Enter the expense amount: ")
        payer_name = input("Enter the name of the person who paid for the expense: ")
        expense.purchase_date = purchase_date
        expense.purchase_category = purchase_category
        expense.store = store
        expense.expense_amount = expense_amount
        payer = User.find_by_name(payer_name)
        expense.payer_id = payer.id
        expense.update()
        print(f"""\nSuccessfully updated expense: 
            Date: {expense.purchase_date}, Category: {expense.purchase_category}, Store: {expense.store}, Amount: {expense.expense_amount}, Payer: {payer.name}, Settled: {bool(expense.is_settled)}, Settled Date: {expense.settled_date}\n""")
    except Exception as exc:
        print(f"Error updating expense: {exc}\n")


def settle_expense(expense):
    pass
def exit_program():
    print("Goodbye!")
    exit()
