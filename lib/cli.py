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
   exit_program
)

def main():
    while True:
        menu()
        choice = input("> ")
        if choice == "1":
            user_menu()
        elif choice == "0":
            exit_program()
        else:
            print("Invalid choice")


def menu():
    print("Please select an option:")
    print("1. Users")
    print("0. Exit")

def user_menu():
    while True:

        print("Select an option:")
        print("1. List Users")
        print("2. Search User Name")
        print("3. Create user")
        print("0. Back to Main Menu")
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
        
        if user:
            print(f'Selected {user.name}.')
            print("Select an option: ")
            print("1. Update User")
            print("2. Delete User")
            print("3. Enter an expense")
            print("4. List user's expenses")
            print("0. Back")
            option = input("> ")
            if option == "1":
                update_user(user.id)
            elif option == "2":
                delete_user(user.id)
            elif option == "3":
                enter_expense(user.id)
            elif option == "4":
                get_user_expenses(user.id)
            elif option == "0":
                return
                
        
        


if __name__ == "__main__":
    main()
