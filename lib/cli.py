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
   find_expense_by_id,
   update_expense,
)

def main():
    while True:
        menu()
        choice = input("> ")
        if choice == "1":
            user_menu()
        elif choice == "2":
            expense_menu()
        elif choice == "0":
            exit_program()
        else:
            print("Invalid choice")


def menu():
    print("Please select an option:")
    print("     1. Users")
    print("     2. Expenses")
    print("     0. Exit")

def user_menu():
    while True:

        print("Select an option:")
        print("     1. List Users")
        print("     2. Search User Name")
        print("     3. Create user")
        print("     0. Back to Main Menu")
        choice = input("> ")
        if choice == "1":
            list_users()
            print("Select a user: ")
            id = int(input(">"))
            user = find_user_by_id(id)
        elif choice == "2":
            user = find_user_by_name()
        elif choice == "3":
            user = create_user()
        elif choice == "0":
            menu()
            return
        
        if user:
            while True:
                print(f"Select an option for {user.name}: ")
                print("     1. Update User")
                print("     2. Delete User")
                print("     3. Enter an expense")
                print("     4. List user's expenses")
                print("     5. Make a payment")
                print("     0. Back")
                option = input("> ")
                if option == "1":
                    update_user(user.id)
                elif option == "2":
                    delete_user(user.id)
                elif option == "3":
                    enter_expense(user.id)
                elif option == "4":
                    get_user_expenses(user.id)
                elif option == "5":
                    while True:
                        owed_payments = get_user_owed_payments(user.id)
                        if len(owed_payments) > 0:
                            print("Enter the payment number to make. Type '0' when finished:")
                            option = input(">")
                            if option == "0":
                                return
                            else:
                                id = int(option)
                                payment = next((payment for payment in owed_payments if payment.id == id), None)
                                make_payment(payment.id)
                        else: 
                            print(f"{user.name} has no pending payments.")
                            return
                elif option == "0":
                    return
            
def expense_menu():
    while True:
        print("Select an option:")
        print("     1. Enter new expense")
        print("     2. List unsettled expenses")
        print("     0. Back to Main Menu")

        choice = input(">")
        if choice == "1":
            expense = enter_expense()
        elif choice == "2":
            list_unsettled_expenses()
            print("Select an expense: ")
            id = int(input(">"))
            expense = find_expense_by_id(id)
        elif choice == "0":
            menu()
            return

        if expense:
            while True:
                print("Select an option:")
                print("     1. Update expense")
                print("     0. Back")
                expense_choice = input(">")
                if expense_choice == "1":
                    update_expense(expense)
                elif expense_choice == "0":
                    return



                

if __name__ == "__main__":
    main()
