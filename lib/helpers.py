# lib/helpers.py
from models.expense import Expense
from models.user import User
from models.payment import Payment

def list_users():
    users = User.get_all()
    for i, user in enumerate(users, start=1):
        print(f'    {i}: {user.name}, income: ${user.income}')
    return users

def find_user_by_name():
    name = input("Enter a user's name: ")
    user = User.find_by_name(name)
    return user if user else print(f'User {name} not found\n')

def find_user_by_id(user_id):
    user = User.find_by_id(user_id)
    return user if user else None

def create_user():
    name = input("Enter the new user's name: ")
    income = input("Enter the user's yearly income as a whole number: ")
    try:
        user = User.create(name, income)
        print(f'Success: {user}\n')
    except Exception as exc:
        print(f'Error creating the user: {exc}\n')

def update_user(user):
    if not isinstance(user, User):
        raise TypeError(f"Expected user to be an instance of the User class, got {type(user).__name__}")
    else:
        try:
            name = input("Enter the user's new name: ")
            user.name = name
            income = input("Enter the user's new income: ")
            user.income = income
            print(f"Successfully updated user: {user.name}, income: {user.income}")
            user.update()
        except Exception as exc:
            print(f'Error updating user: {exc}\n')

def delete_user(user):
    if not isinstance(user, User):
        raise TypeError(f"Expected user to be an instance of the User class, got {type(user).__name__}")
    else:
        print(f'User {user.name} deleted\n')
        user.delete()

def get_user_expenses(user):
    if not isinstance(user, User):
        raise TypeError(f"Expected user to be an instance of the User class, got {type(user).__name__}")
    else:
        expenses = user.expenses()
        print(f"Listing {user.name}'s expenses: ")
        for expense in expenses:
            print(f'    Date: {expense.purchase_date}, Category: {expense.purchase_category}, Store: {expense.store}, Amount: {expense.expense_amount}, Payer: {user.name}, Settled: {bool(expense.is_settled)}, Settled Date: {expense.settled_date}' )

def list_user_details(user):
    pass

def enter_expense(payer=None):
    purchase_date = input("Enter the purchase date: ")
    purchase_category = input("Enter the purchase category (Groceries, Restaurant, Home Supplies, Event, Bar): ")
    store = input("Enter the store where purchase was made: ")
    expense_amount = input("Enter the expense amount (ex 12.34): ")

    if payer == None:
        while True:
            name = input("Enter the user name who paid for the expense: ")
            try: 
                payer = User.find_by_name(name)
                if not payer:
                    print("User not found, try again")
                    continue
                else: 
                    break
            except: 
                Exception("User not found")
                continue

    expense = Expense.create(purchase_date, purchase_category, store, expense_amount, payer.id, is_settled=0)

    print(f"Successfully created new expense by {payer.name}: {expense.purchase_date}, {expense.purchase_category} purchase at {expense.store} for ${expense.expense_amount}")

    while True:
        print(f"Enter the names of users who will pay {payer.name} back for this expense, separated by commas: ")
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
        name = input("Enter the name of the person who owes payments: ")
        ower = User.find_by_name(name)
    else:
        ower = User.find_by_id(ower_id)
    payments = ower.get_owed_payments()

    if len(payments) == 0:
        print(f"{ower.name} has no owed payments!")
        return None
    else:
        print(f"{ower.name} has {len(payments)} unpaid payments: ")
        for i, payment in enumerate(payments, start=1):
            recipient = User.find_by_id(payment.recipient_id)
            expense = Expense.find_by_id(payment.expense_id)
            print(f"    {i}: Pay {recipient.name} ${payment.payment_amount} for {expense.purchase_category} purchase at {expense.store} on {expense.purchase_date}")
    
    return payments

def list_users_with_owed_payments():
    """Gets users who owe payments, listing their names and number of payments"""
    users = User.get_all()
    owers = [user for user in users if len(user.get_owed_payments()) > 0]
    if not owers:
        print("No payments are owed!")
        return None
    else:
        for i, ower in enumerate(owers, start=1):
            print(f"    {i}. {ower.name} owes {len(ower.get_owed_payments())} payments.")
    return owers

def make_payment(payment_id=None):        
    if payment := Payment.find_by_id(payment_id):
        payment.settle_payment()
        recipient = User.find_by_id(payment.recipient_id)
        ower = User.find_by_id(payment.ower_id)
        print(f"Success: {ower.name} paid {recipient.name} ${payment.payment_amount}")
    else: print(f"Payment not found")

def list_unsettled_expenses():
    expenses = Expense.find_unsettled_expenses()
    for i, expense in enumerate(expenses, start=1):
        payer = User.find_by_id(expense.payer_id)
        print(f"    {i}: {payer.name} made purchase at {expense.store} on {expense.purchase_date} for ${expense.expense_amount}")
    return expenses

# def find_expense_by_id(expense_id):
#     expense = Expense.find_by_id(expense_id)
#     print(expense) if expense else print("Expense not found")
#     return expense

def update_expense(expense):
    if not isinstance(expense, Expense):
        raise TypeError(f"Expense should be an instance of Expense Class, got {type(expense).__name__}")
    else:
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

def get_expense_unsettled_payments(expense):
    if not isinstance(expense, Expense):
        raise TypeError(f"Expense should be an instance of Expense Class, got {type(expense).__name__}")
    else:
        unsettled_payments = expense.unsettled_payments()
        if unsettled_payments:
            recipient = User.find_by_id(expense.payer_id)
            print(f"\nExpense has {len(unsettled_payments)} pending payments.")
            for i, payment in enumerate(unsettled_payments, start=1):
                ower = User.find_by_id(payment.ower_id)
                print(f"    {i}: {ower.name} owes {recipient.name} ${payment.payment_amount} for purchase at {expense.store} on {expense.purchase_date}")
        else: print(f"Expense has no unsettled payments.")
        return unsettled_payments if unsettled_payments else None


def settle_expense(expense):
    if not isinstance(expense, Expense):
        raise TypeError(f"Expense should be an instance of Expense Class, got {type(expense).__name__}")
    else:
        unsettled_payments = expense.unsettled_payments()
        if len(unsettled_payments) == 0:
            expense.settle()
            print("Expense has been paid back, and is now settled!")
            return
        else:
            recipient = User.find_by_id(expense.payer_id)
            while True: 
                print(f"Expense has {len(unsettled_payments)} unsettled payments.")
                for i, payment in enumerate(unsettled_payments, start=1):
                    ower = User.find_by_id(payment.ower_id)
                    print(f"    {i}: {ower.name} owes {recipient.name} ${payment.payment_amount} for purchase at {expense.store} on {expense.purchase_date}")
                    choice = input("Make this payment now? Enter Y/N")
                    if choice == "Y":
                        make_payment(payment.id)
                    else:
                        continue
                

def exit_program():
    print("Goodbye!")
    exit()
