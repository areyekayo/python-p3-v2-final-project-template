# lib/cli.py

from helpers import (
   list_users,
   find_user_by_name,
   find_user_by_id,
   create_user,
   update_user,
   delete_user,
   get_user_expenses,
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
        print("0. Back to Main Menu")
        choice = input("> ")
        if choice == "1":
            list_users()
            print("Select a user: ")
            id = int(input(">"))
            user = find_user_by_id(id)
        elif choice == "2":
            user = find_user_by_name()
        elif choice == "0":
            return

        print(f'Selected {user.name}')
        
        


if __name__ == "__main__":
    main()
