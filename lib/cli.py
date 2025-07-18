# lib/cli.py

from helpers import (
   list_users,
   find_user_by_name,
   find_user_by_id,
   create_user,
   update_user,
   delete_user,
   get_user_expenses,
   enter_expense,
   exit_program,
   get_user_owed_payments,
   make_payment,
   list_unsettled_expenses,
   update_expense,
   settle_expense,
   get_expense_unsettled_payments,
   list_users_with_owed_payments
)

def main():
    while True:
        menu()
        choice = input("> ")
        if choice == "1":
            enter_expense()
        elif choice == "2":
            while True:
                print("Users who owe payments:")
                owers = list_users_with_owed_payments()
                if not owers:
                    break
                print("Enter the user number making a payment. Type '0' when finished:")
                user_choice = int(input(">"))
                if user_choice == 0:
                    break
                else:
                    user = owers[user_choice - 1]
                    while True:
                        owed_payments = get_user_owed_payments(user.id)
                        if not owed_payments:
                            break
                        print("Enter the payment number to make. Type '0' when finished:")
                        option = int(input(">"))
                        if option == 0:
                            break
                        else:
                            selected_number= int(option)
                            payment = owed_payments[selected_number - 1]
                            make_payment(payment.id)

        elif choice == "3":
            user_menu()
        elif choice == "4":
            expense_menu()
        elif choice == "0":
            exit_program()
        else:
            print("Invalid choice")


def menu():
    print("\nWelcome to the Fair Bills app!")
    print("Please select an option: ")
    print("     1. Enter new expense")
    print("     2. Make a payment")
    print("     3. Manage Users")
    print("     4. Manage Expenses")
    print("     0. Exit")

def user_menu():
    while True:
        user = None
        print("USER MENU")
        print("-------------------")
        print("Select an option:")
        print("     1. List Users")
        print("     2. Search User Name")
        print("     3. Create user")
        print("     0. Back to Main Menu")
        choice = input("> ")

        if choice == "1":
            while True:
                users = list_users()
                print("Select a user. Enter 0 to go back: ")
                try: 
                    user_num = int(input(">"))
                    user = users[user_num - 1]
                    if user:
                        break
                    elif id == 0:
                        break
                    elif not user: 
                        print(f"Invalid user selection. Please try again.")
                except ValueError: 
                    print("Invalid input. Please try again.")
        elif choice == "2":
            user = find_user_by_name()
        elif choice == "3":
            user = create_user()
        elif choice == "0":
            return
        else: 
            print("Invalid option, try again.")
        
        if user:
            print(f"\nSelected {user.name}, income: {user.income}.")
            while True:
                print(f"Select an option for {user.name}: ")
                print("     1. Update User")
                print("     2. Delete User")
                print("     3. List user's expenses")
                print("     0. Back")
                option = input("> ")
                if option == "1":
                    update_user(user)
                elif option == "2":
                    delete_user(user)
                elif option == "3":
                    get_user_expenses(user)
                elif option == "0":
                    break
                else:
                    print("Invalid option, try again")
            
def expense_menu():
    while True:
        print("EXPENSE MENU")
        print("-------------------")
        print("Select an option:")
        print("     1. Enter new expense")
        print("     2. List unsettled expenses")
        print("     0. Back to Main Menu")

        choice = input(">")
        if choice == "1":
            expense = enter_expense()
        elif choice == "2":
            print("Listing all unsettled expenses...")
            expenses = list_unsettled_expenses()
            print("Select an expense: ")
            exp_choice = int(input(">"))
            expense = expenses[exp_choice - 1]
        elif choice == "0":
            return

        if expense:
            while True:
                payer = find_user_by_id(expense.payer_id)
                print(f"\nExpense selected: {payer.name}'s purchase at {expense.store} on {expense.purchase_date} for ${expense.expense_amount}")
                print("Select an option:")
                print("     1. Update expense")
                print("     2. Settle expense")
                print("     0. Back")
                expense_choice = input(">")
                if expense_choice == "1":
                    update_expense(expense)
                elif expense_choice == "2":

                    # move this logic into the settle_expense helper function
                    while True:
                        owed_payments = get_expense_unsettled_payments(expense)
                        if not owed_payments:
                            break
                        else:
                            print("Enter the payment number to make. Enter '0' when finished.")
                            payment_choice = input(">")
                            if payment_choice == "0":
                                break
                            else:
                                settle_expense(expense)


                elif expense_choice == "0":
                    break

if __name__ == "__main__":
    main()
