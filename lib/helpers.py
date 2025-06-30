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
        for expense in expenses:
            print(f'{expense}')
    else: print(f'User not found\n')



def exit_program():
    print("Goodbye!")
    exit()
