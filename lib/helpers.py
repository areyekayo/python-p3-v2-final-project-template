# lib/helpers.py
from models.expense import Expense
from models.user import User
from models.payment import Payment

def list_users():
    users = User.get_all()
    for user in users: 
        print(f'{user.id}: {user.name}')

def find_user_by_name():
    name = input("Enter a user's name: ")
    user = User.find_by_name(name)
    print(user) if user else print(
        f'User {name} not found\n'
    )
    return user

def find_user_by_id(user_id):
    user = User.find_by_id(user_id)
    print(user) if user else print(
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

def update_user(user_id):
    if user := User.find_by_id(user_id):
        try:
            name = input("Enter the user's new name: ")
            user.name = name
            income = input("Enter the user's new income: ")
            user.income = income
            user = User.update(name, income)
        except Exception as exc:
            print(f'Error updating user: {exc}\n')
    else: print(f'User not found')

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

    print(f"Successfully created new expense by ${user.name}: {expense.purchase_date}, {expense.purchase_category}, {expense.store}, {expense.expense_amount}")
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


def exit_program():
    print("Goodbye!")
    exit()
