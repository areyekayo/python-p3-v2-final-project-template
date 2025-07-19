# lib/helpers.py
from models.expense import Expense
from models.user import User
from models.payment import Payment

def list_users():
    """Lists all users and their income."""
    users = User.get_all()
    for i, user in enumerate(users, start=1):
        print(f'    {i}: {user.name}, income: ${user.income}')
    return users

def find_user_by_name():
    """Gets a user by their name."""
    name = input("Enter a user's name: ")
    user = User.find_by_name(name)
    return user if user else print(f'User {name} not found\n')

def find_user_by_id(user_id):
    """Gets a user by ID, to be used by other helper functions."""
    user = User.find_by_id(user_id)
    return user if user else None

def create_user():
    """Creates a new user."""
    name = input("Enter the new user's name: ")
    income = input("Enter the user's yearly income as a whole number: ")
    try:
        user = User.create(name, income)
        print(f'Success: {user}\n')
    except Exception as exc:
        print(f'Error creating the user: {exc}\n')

def update_user(user):
    """Updates an existing user."""
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
    """Deletes a user."""
    if not isinstance(user, User):
        raise TypeError(f"Expected user to be an instance of the User class, got {type(user).__name__}")
    else:
        print(f'User {user.name} deleted\n')
        user.delete()

def get_user_expenses(user):
    """Gets a user's expenses."""
    if not isinstance(user, User):
        raise TypeError(f"Expected user to be an instance of the User class, got {type(user).__name__}")
    else:
        expenses = user.expenses()
        print(f"Listing {user.name}'s expenses: ")
        for expense in expenses:
            print(f'    Date: {expense.purchase_date}, Category: {expense.purchase_category}, Store: {expense.store}, Amount: {expense.expense_amount:.2f}, Payer: {user.name}, Settled: {bool(expense.is_settled)}, Settled Date: {expense.settled_date}' )

def list_user_details(user):
    pass

def enter_expense(payer=None):
    """Creates a new expense, including payments for users who owe the payer."""
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

    print(f"Successfully created new expense by {payer.name}: {expense.purchase_date}, {expense.purchase_category} purchase at {expense.store} for ${expense.expense_amount:.2f}")

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
            print(f"    {i}. Pay {recipient.name} ${payment.payment_amount:.2f} for {expense.purchase_category} purchase at {expense.store} on {expense.purchase_date}")
    
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

def list_owed_payments():
    owed_payments = Payment.get_unpaid_payments()
    if not owed_payments:
        print("All payments have been made!")
        return None
    else:
        print("All owed payments:")
        for i, payment in enumerate(owed_payments, start=1):
            recipient = User.find_by_id(payment.recipient_id)
            ower = User.find_by_id(payment.ower_id)
            expense = Expense.find_by_id(payment.expense_id)
            print(f"    {i}. {ower.name} owes {recipient.name} ${payment.payment_amount:.2f} for purchase at {expense.store} on {expense.purchase_date}")
        return owed_payments

def make_payments():
    while True:
        payments = list_owed_payments()
        if len(payments) == 0:
            break
        else:
            print("Enter a payment number to make, or 0 to go back: ")
            try:
                payment_num = int(input(">"))
                if payment_num == 0:
                    break
                if 1 <= payment_num <= len(payments):
                    payment = payments[payment_num - 1]
                    settle_payment(payment.id)
                else:
                    print(f"Please enter a number between 1 and {len(payments)}")
            except ValueError:
                print("Invalid value, please try again.")
 

def settle_payment(payment_id=None):
    """Settles a payment for an expense."""     
    if payment := Payment.find_by_id(payment_id):
        payment.settle_payment()
        recipient = User.find_by_id(payment.recipient_id)
        ower = User.find_by_id(payment.ower_id)
        print(f"Success: {ower.name} paid {recipient.name} ${payment.payment_amount:.2f}")
        expense = Expense.find_by_id(payment.expense_id)
        if expense.is_expense_fully_repaid() == True:
            print(f"{recipient.name}'s purchase at {expense.store} is now fully settled!")
            expense.settle()
    else: print(f"Payment not found")

def list_unsettled_expenses():
    """Lists expenses that have not been paid back in full."""
    expenses = Expense.get_unsettled_expenses()
    for i, expense in enumerate(expenses, start=1):
        payer = User.find_by_id(expense.payer_id)
        print(f"    {i}. {payer.name} made purchase at {expense.store} on {expense.purchase_date} for ${expense.expense_amount:.2f}")
    return expenses

def update_expense(expense):
    """Updates an expense. Note: need to also update payments, if the purchase amount changes."""
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
                Date: {expense.purchase_date}, Category: {expense.purchase_category}, Store: {expense.store}, Amount: {expense.expense_amount:.2f}, Payer: {payer.name}, Settled: {bool(expense.is_settled)}, Settled Date: {expense.settled_date}\n""")
        except Exception as exc:
            print(f"Error updating expense: {exc}\n")

def get_expense_unsettled_payments(expense):
    """Gets an expense's unsettled payments."""
    if not isinstance(expense, Expense):
        raise TypeError(f"Expense should be an instance of Expense Class, got {type(expense).__name__}")
    else:
        unsettled_payments = expense.unsettled_payments()
        if unsettled_payments:
            recipient = User.find_by_id(expense.payer_id)
            print(f"\nExpense has {len(unsettled_payments)} pending payments.")
            for i, payment in enumerate(unsettled_payments, start=1):
                ower = User.find_by_id(payment.ower_id)
                print(f"    {i}. {ower.name} owes {recipient.name} ${payment.payment_amount:.2f} for purchase at {expense.store} on {expense.purchase_date}")
        else: print(f"Expense has no unsettled payments.")
        return unsettled_payments if unsettled_payments else None

def settle_expense(expense):
    pass
    # """Settles an expense if all owed payments have been made."""
    # if not isinstance(expense, Expense):
    #     raise TypeError(f"Expense should be an instance of Expense Class, got {type(expense).__name__}")
    # else:
    #     if expense.is_expense_fully_repaid() == True:
    #         expense.settle()
    #         print("Expense has been paid back, and is now settled!")
    #         return
    #     else:
    #         unsettled_payments = expense.unsettled_payments()
    #         recipient = User.find_by_id(expense.payer_id)
    #         print(f"Expense has {len(unsettled_payments)} unsettled payments.")
    #         for i, payment in enumerate(unsettled_payments, start=1):
    #             ower = User.find_by_id(payment.ower_id)
    #             print(f"    {i}: {ower.name} owes {recipient.name} ${payment.payment_amount:.2f} for purchase at {expense.store} on {expense.purchase_date}")
    #         print("Select a payment to make: ")
    #         choice = int(input(">"))
    #         if choice == "Y":
    #             settle_payment(payment.id)
    #         else:
                
    #         if expense.is_expense_fully_repaid() == True:
    #             print("Expense is fully paid back!")
    #             expense.settle()

def report():
    """Prints a high level report for the main CLI menu, listing users and their unsettled payments, as well as whether any expenses can be settled (no pending payments)."""

    unsettled_expenses = Expense.get_unsettled_expenses()
    users = User.get_all()
    for user in users:
        owed_payments = user.get_owed_payments()
        if len(owed_payments) > 0:
            print(f"    {user.name} owes {len(owed_payments)} payments.")
        else:
            print(f"    {user.name} doesn't owe any payments.")

    fully_paid_expenses = [expense for expense in unsettled_expenses if expense.is_expense_fully_repaid() == True and expense.is_settled == 0]
    
    if len(fully_paid_expenses) > 0:
        print(f"    {len(fully_paid_expenses)} expenses are fully paid back and can be settled.")

def exit_program():
    print("Goodbye!")
    exit()
