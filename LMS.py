# AUTHOR: Ignatius Chan
# ADMIN NO / GRP: <230653K / AA2303>

# import modules
import json
from tabulate import tabulate
import sys
import time
import os
import msvcrt as m


# opening booklist
try:
    file = open("booklist.json", "r+")
    filedata = json.load(file)
    file.close()
except:
    filedata = []

# opening list of registered accounts
try:
    filey = open("accounts.json", "r+")
    accounts = json.load(filey)
    filey.close()
except:
    accounts = []

# opening keybinds
try:
    filo = open("keybinds.json", "r+")
    keys = json.load(filo)
    filo.close()
except:
    keys = []


main = False  # initializing main (main menu active or not)
login = False  # initializing login (user login status)
passwordy = False  # initializing passwordy (password validation)

# initializing tabulate headers
head = ["ISBN", "Book Name", "Book Type", "Quantity"]
keyheads = [
    "add book button",
    "update book button",
    "view books button",
    "search book button",
    "delete book button",
    "log out button",
    "settings button",
]
sethead = ["settings", "keys"]
acchead = ["username", "password"]


# wait for keypress
def wait():
    m.getch()


# clear screen
def clearscreen():
    os.system("cls" if os.name == "nt" else "clear")


# savbook in json file
def savebooks():
    with open("booklist.json", "w") as file:
        json.dump(filedata, file, indent=4)


# save settings in json file
def savesettings():
    with open("keybinds.json", "w") as filo:
        json.dump(keys, filo, indent=4)


# save accounts in json file
def saveaccs():
    with open("accounts.json", "w") as filey:
        json.dump(accounts, filey, indent=4)


# validating isbn
def isbnvalid():
    global isbn
    while True:
        isbn = input("Enter ISBN: ")
        if len(isbn) == 10 and isbn.isnumeric():
            return isbn
        elif "-" in isbn and len(isbn) == 14:
            isbnlst = isbn.split("-")
            if (
                len(isbnlst[0]) == 3
                and len(isbnlst[1]) == 10
                and isbnlst[0].isnumeric()
                and isbnlst[1].isnumeric()
            ):
                return isbn
            else:
                print(
                    "Invalid ISBN! ISBN should be either 10 digits or in the format 'XXX-XXXXXXXXXX'."
                )
        else:
            print(
                "Invalid ISBN! ISBN should be either 10 digits or in the format 'XXX-XXXXXXXXXX'."
            )


# validating book type
def booktypevalid():
    global booktype
    booktype = input(
        """
Enter booktype
1. eBook
2. Hard Cover
3. Paper Back
Choice: """
    )
    while booktype not in ["1", "2", "3"]:
        booktype = input("Invalid choice! Please select 1, 2, or 3: ")
    if booktype == "1":
        booktype = "eBook"
    elif booktype == "2":
        booktype = "Hard Cover"
    else:
        booktype = "Paper Back"


# validating book quantity
def quantityvalid():
    global quantity
    quantity = input("Enter quantity: ")
    while not quantity.isnumeric():
        quantity = input("Invalid quantity! Please enter a numerical value: ")


# adding of books
def addbook():
    clearscreen()
    print("Going to add book...")
    time.sleep(1)
    print(
        """
+================+
|    ADD BOOK    |
+================+"""
    )
    while True:
        newbook = []
        isbn = isbnvalid()
        if isbninside(isbn):
            retry = input(
                "ISBN already exists! Do you want to re-enter details? (y/n): "
            )
            if retry.lower() != "y":
                print("Returning to main menu...")
                time.sleep(1.5)
                return
        else:
            newbook.append(isbn)
            bookname = input("Enter book name: ")
            if nameinside(bookname):
                retry = input(
                    "Book name already exists! Do you want to re-enter details? (y/n): "
                )
                if retry.lower() != "y":
                    print("Returning to main menu...")
                    time.sleep(1.5)
                    return
            else:
                newbook.append(bookname)
                booktypevalid()
                newbook.append(booktype)
                quantityvalid()
                newbook.append(int(quantity))
                print(tabulate([newbook], headers=head, tablefmt="grid"))
                confirm = input("Confirm adding this book? (y/n): ")
                if confirm.lower() == "y":
                    filedata.append(newbook)
                    savebooks()
                    print("Book successfully added...")
                else:
                    print("Book addition cancelled...")
                time.sleep(0.5)
                print("Returning to main menu...")
                time.sleep(1.5)
                return


# check if isbn currently exists
def isbninside(isbn):
    for i in filedata:
        if isbn in i:
            return True
    return False


# check if name currently exists
def nameinside(bookname):
    for i in filedata:
        if bookname in i:
            return True
    return False


# viewing of books
def viewbooks():
    clearscreen()
    print("Going to view books...")
    time.sleep(1)
    print(
        """
+=================+
|    VIEW BOOKS   |
+=================+"""
    )
    print(tabulate(filedata, headers=head, tablefmt="grid"))
    totalbooks(filedata)
    time.sleep(2)
    viewing = input(
        """
Sort or filter books?
1. Sort Books
2. Filter books (by book type)
0. Go back
Choice: """
    )
    while viewing not in ["1", "2", "0"]:
        viewing = input("Invalid choice! Please select 1, 2 or 0.")
    if viewing == "1":
        sortbooks()
        return
    elif viewing == "2":
        filterbooks()
    else:
        print("Returning to main menu...")
        time.sleep(1.5)
        return


# display filtered booklists
def filterbooks():
    filtering = input(
        """
Which book type would you like to filter the booklist by?
1. eBook
2. Hard Cover
3. Paper Back
Choice: """
    )
    while filtering not in ["1", "2", "3"]:
        filtering = input("Invalid choice! Please select 1, 2 or 3.")
    if filtering == "1":
        clearscreen()
        print("Viewing all eBook books...")
        time.sleep(1)
        print(tabulate(ebook_books, headers=head, tablefmt="grid"))  # filtered by ebook
        totalbooks(ebook_books)
        print("Press 'Enter' to go back to main menu...")
        wait()
    elif filtering == "2":
        clearscreen()
        print("Viewing all Hard Cover books...")
        time.sleep(1)
        print(
            tabulate(Hard_Cover_books, headers=head, tablefmt="grid")
        )  # filtered by hard cover
        totalbooks(Hard_Cover_books)
        print("Press 'Enter' to go back to main menu...")
        wait()
    else:
        clearscreen()
        print("Viewing all Paper Back books...")
        time.sleep(1)
        print(
            tabulate(Paper_Back_books, headers=head, tablefmt="grid")
        )  # filtered by paper back
        totalbooks(Paper_Back_books)
        print("Press 'Enter' to go back to main menu...")
        wait()


# display sorted booklists
def sortbooks():
    sorting = input(
        f"""
How would you like to sort the books by?
1. ISBN
2. Book name
3. Quantity (descending order)
4. Quantity (ascending order)
Choice: """
    )
    while sorting not in ["1", "2", "3", "4"]:
        sorting = input("Invalid choice! Please select 1, 2, 3 or 4.")
    if sorting == "1":
        clearscreen()
        print("Viewing books sorted by ISBN...")
        time.sleep(1)
        print(
            tabulate(sorted_books_by_isbn, headers=head, tablefmt="grid")
        )  # sorted by isbn (ascending order)
        totalbooks(sorted_books_by_isbn)
        print("Press 'Enter' to go back to main menu...")
        wait()
    elif sorting == "2":
        clearscreen()
        print("Viewing books sorted by name...")
        time.sleep(1)
        print(
            tabulate(sorted_books_by_name, headers=head, tablefmt="grid")
        )  # sorted by alphabetical order
        totalbooks(sorted_books_by_name)
        print("Press 'Enter' to go back to main menu...")
        wait()
    elif sorting == "3":
        clearscreen()
        print("Viewing books sorted by quantity (descending order)...")
        time.sleep(1)
        print(
            tabulate(sorted_books_by_quantityd, headers=head, tablefmt="grid")
        )  # sorted quantity (descending order)
        totalbooks(sorted_books_by_quantityd)
        print("Press 'Enter' to go back to main menu...")
        wait()
    else:
        clearscreen()
        print("Viewing books sorted by quantity (ascending order)...")
        time.sleep(1)
        print(
            tabulate(sorted_books_by_quantitya, headers=head, tablefmt="grid")
        )  # sorted quantity (ascending order)
        totalbooks(sorted_books_by_quantitya)
        print("Press 'Enter' to go back to main menu...")
        wait()


# sum of books
def totalbooks(booklst):
    total = sum(item[-1] for item in booklst)
    print("TOTAL BOOKS:", total)


# updating of books
def updatebook():
    clearscreen()
    print("Going to update book...")
    time.sleep(1)
    print(
        """
+===================+
|    UPDATE BOOK    |
+===================+"""
    )
    print("Select a book to update:")
    print(tabulate(filedata, headers=head, tablefmt="grid"))
    isbn_to_update = isbnvalid()
    matching_books = [book for book in filedata if book[0] == isbn_to_update]

    if not matching_books:
        print("No book with the provided ISBN found.")
        print("Returning to main menu...")
        time.sleep(1.5)
        return

    book_to_update = matching_books[0]

    print("Current details of the book:")
    print(tabulate([book_to_update], headers=head, tablefmt="grid"))

    while True:
        update_choice = input(
            """
What would you like to update?
1. Book Name
2. ISBN
3. Book Type
4. Quantity
0. Go back
Choice: """
        )

        if update_choice == "1":
            new_name = input("Enter the new name for the book: ")
            if nameinside(new_name):
                print("Book name already exists for another book.")
            else:
                book_to_update[1] = new_name
                print("Book name updated...")
                time.sleep(0.5)
        elif update_choice == "2":
            new_isbn = isbnvalid()
            if isbninside(new_isbn):
                print("ISBN already exists for another book.")
            else:
                book_to_update[0] = new_isbn
                print("ISBN updated...")
                time.sleep(0.5)
        elif update_choice == "3":
            booktypevalid()
            book_to_update[2] = booktype
            print("Book type updated...")
            time.sleep(0.5)
        elif update_choice == "4":
            quantityvalid()
            book_to_update[3] = int(quantity)
            print("Quantity updated...")
            time.sleep(0.5)
        elif update_choice == "0":
            break
        else:
            print("Invalid choice! Please select a valid option.")

    savebooks()
    print("Book details updated successfully...")
    time.sleep(0.5)
    print("Returning to main menu...")
    time.sleep(1.5)


# searching for book
def searchbook():
    clearscreen()
    print("Going to search book...")
    time.sleep(1)
    print(
        """
+===================+
|    SEARCH BOOK    |
+===================+"""
    )
    search_term = input("Enter ISBN or book title to search for book: ")

    matching_books = []

    for book in filedata:
        if book[0] == search_term or book[1].lower() == search_term.lower():
            matching_books.append(book)

    if not matching_books:
        print("No book with the provided ISBN or title found.")
        print("Returning to main menu...")
        time.sleep(1.5)
        return
    print(tabulate(matching_books, headers=head, tablefmt="grid"))
    print("Press 'Enter' to go back to main menu...")
    wait()


# delete book
def deletebook():
    clearscreen()
    print("Going to delete book...")
    time.sleep(1)
    print(
        """
+===================+
|    DELETE BOOK    |
+===================+"""
    )
    print("Select a book to delete:")
    print(tabulate(filedata, headers=head, tablefmt="grid"))

    isbn_to_delete = isbnvalid()
    matching_books = [book for book in filedata if book[0] == isbn_to_delete]

    if not matching_books:
        print("No book with the provided ISBN found.")
        print("Returning to main menu...")
        time.sleep(1.5)
        return

    book_to_delete = matching_books[0]
    print("Are you sure you want to delete the following book?")
    print(tabulate([book_to_delete], headers=head, tablefmt="grid"))

    confirm_delete = input("Confirm deletion (y/n): ")
    if confirm_delete.lower() == "y":
        filedata.remove(book_to_delete)
        savebooks()
        print("Book deleted successfully...")
        time.sleep(0.5)
        print("Returning to main menu...")
        time.sleep(1.5)
    else:
        print("Deletion cancelled...")
        time.sleep(0.5)
        print("Returning to main menu...")
        time.sleep(1.5)


# main menu
def mainy():
    clearscreen()
    global login
    global main
    action = input(
        f"""
+=================+
|    MAIN MENU    |
+=================+
Choose what action you want to do?
{keys[0]}. Add new book
{keys[1]}. Update existing book
{keys[2]}. View books
{keys[3]}. Search for a book
{keys[4]}. Delete a book
{keys[5]}. Log out
{keys[6]}. Settings
Choice: """
    )
    while action not in keys:
        action = input(
            f"Invalid choice! Please select {keys[0]}, {keys[1]}, {keys[2]}, {keys[3]}, {keys[4]}, {keys[5]} or {keys[6]}: "
        )
    if action == keys[0]:
        addbook()
    elif action == keys[1]:
        if not filedata:
            print("No books found. You can add a book.")
            return
        updatebook()
    elif action == keys[2]:
        global sorted_books_by_isbn
        global sorted_books_by_name
        global sorted_books_by_quantitya
        global sorted_books_by_quantityd
        global ebook_books
        global Hard_Cover_books
        global Paper_Back_books
        # sorting and filtering of the booklist
        sorted_books_by_isbn = sorted(filedata, key=lambda x: x[0])
        sorted_books_by_name = sorted(filedata, key=lambda x: x[1])
        sorted_books_by_quantityd = sorted(filedata, key=lambda x: x[3], reverse=True)
        sorted_books_by_quantitya = sorted(filedata, key=lambda x: x[3])
        ebook_books = [book for book in filedata if book[2] == "eBook"]
        Hard_Cover_books = [book for book in filedata if book[2] == "Hard Cover"]
        Paper_Back_books = [book for book in filedata if book[2] == "Paper Back"]
        if not filedata:
            print("No books found. You can add a book.")
            time.sleep(1)
            return
        viewbooks()
    elif action == keys[3]:
        if not filedata:
            print("No books found. You can add a book.")
            time.sleep(1)
            return
        searchbook()
    elif action == keys[4]:
        if not filedata:
            print("No books found. You can add a book.")
            time.sleep(1)
            return
        deletebook()
    elif action == keys[5]:
        print("Logging out...")
        time.sleep(1.5)
        savebooks()
        saveaccs()
        savesettings()
        login = False
        main = False
    elif action == keys[6]:
        editsettings()


# login page
def loginpage():
    global passw
    global user
    global login
    global main
    attempts_left = 5

    while not login:
        if not accounts:
            clearscreen()
            noaccs = input(
                """
+==================+
|    LOGIN PAGE    |
+==================+
There are currently no accounts registered! (Enter '#' to create an account) """
            )
            if noaccs == "#":
                createaccount()
            else:
                print("Closing program...")
                time.sleep(1.5)
                print(
                    """
+==================================+
|    THANK YOU FOR USING THE       |
|      MINI LIBRARY PROGRAM!       |
+==================================+"""
                )
                sys.exit(0)
        else:
            clearscreen()
            user = input(
                """
+==================+
|    LOGIN PAGE    |
+==================+
Enter "#" to create an account.
Enter "$" to reset password.
Enter "end" to exit the program.
ENTER USERNAME OR COMMAND: """
            )
            if user.lower() == "end":
                saveaccs()
                savebooks()
                savesettings()
                print("Closing program...")
                time.sleep(1.5)
                clearscreen()
                print(
                    """
+==================================+
|    THANK YOU FOR USING THE       |
|      MINI LIBRARY PROGRAM!       |
+==================================+"""
                )
                sys.exit(0)
            elif user.lower() == "#":
                createaccount()
            elif user == "$":
                resetpass()
            else:
                while not passwordy and attempts_left > 0:
                    passw = input("ENTER PASSWORD: ")
                    if not loginval(user, passw):
                        attempts_left -= 1
                        print(
                            f"Username and password do not match! {attempts_left} attempts remaining."
                        )
                        if attempts_left == 0:
                            print("Out of attempts. Closing program...")
                            time.sleep(1.5)
                            clearscreen()
                            print(
                                """
+==================================+
|    THANK YOU FOR USING THE       |
|      MINI LIBRARY PROGRAM!       |
+==================================+"""
                            )
                            sys.exit(0)
                        retry = input("Do you want to login try again? (y/n): ")
                        if retry.lower() != "y":
                            print("Closing program...")
                            time.sleep(1.5)
                            clearscreen()
                            print(
                                """
+==================================+
|    THANK YOU FOR USING THE       |
|      MINI LIBRARY PROGRAM!       |
+==================================+"""
                            )
                            sys.exit(0)
                        break
                    else:
                        print("Logging in...")
                        time.sleep(1.5)
                        global user1
                        global pass1
                        user1 = user
                        pass1 = passw
                        return


# create account
def createaccount():
    newaccount = []
    keypass = input("Enter admin key: ")
    if keypass == "admin123!":
        while True:
            newuser = input("Enter new username: ")
            if any(account[0] == newuser for account in accounts):
                print("Username already exists. Please choose a different username.")
                continue
            newuser2 = input("Confirm new username: ")
            if newuser == newuser2:
                newaccount.append(newuser)
                newpass = input("Enter new password: ")
                newpass2 = input("Confirm new password: ")
                if newpass == newpass2:
                    newaccount.append(newpass)
                    print("New account saved...")
                    time.sleep(1.5)
                    accounts.append(newaccount)
                    saveaccs()
                    return
                else:
                    print("passwords do not match!")
            else:
                print("Usernames do not match!")
            retry = input("Do you want to try again? (y/n): ")
            if retry.lower() != "y":
                return
    else:
        print("Incorrect admin key!")
        time.sleep(1.5)


# validate login
def loginval(username, password):
    global acc_user
    global acc_pass
    for acc_user, acc_pass in accounts:
        if username == acc_user and password == acc_pass:
            return True
    return False


# settings
def editsettings():
    clearscreen()
    print("Going to settings...")
    time.sleep(1)
    print(
        """
+================+
|    SETTINGS    |
+================+"""
    )
    opt = input(
        """
Choose what action you want to do?
1. View keybinds for main menu
2. Edit keybinds for main menu
3. View my account
4. Delete my account
5. Change password
6. Change username
7. Reset keybinds to default
0. Go back
Choice: """
    )
    while opt not in ["1", "2", "3", "4", "5", "6", "7", "0"]:
        opt = input("Invalid choice! Please select 1, 2, 3, 4, 5, 6, 7 or 0: ")
    if opt == "1":
        print(tabulate(keys, headers=sethead, showindex=keyheads, tablefmt="grid"))
        print("Press 'Enter' to go back to main menu...")
        wait()
    elif opt == "2":
        editkeys()
    elif opt == "3":
        acc = [user1, pass1]
        print(tabulate(acc, showindex=acchead, tablefmt="grid"))
        print("Press 'Enter' to go back to main menu...")
        wait()
    elif opt == "4":
        cfming = input("Confirm deletion of account? (y/n): ")
        while cfming not in ["y", "n"]:
            cfming = input("Invalid choice! Please type 'y' or 'n': ")
        if cfming == "y":
            for q in accounts:
                if user in q:
                    accounts.remove(q)
                    saveaccs()
            print("Account deleted successfully...")
            time.sleep(1)
            print("Logging out...")
            time.sleep(1.5)
            savebooks()
            savesettings()
            global login
            global main
            login = False
            main = False
        else:
            return
    elif opt == "5":
        updatepass()
    elif opt == "6":
        updateuser()
    elif opt == "0":
        print("Returning to main menu...")
        time.sleep(1.5)
    else:
        resetkeys()


# reset keybinds
def resetkeys():
    global keys
    try:
        filez = open("defaultkeys.json", "r+")
        dkeys = json.load(filez)
        filez.close()
    except:
        dkeys = []
    cfming = input("Confirm reset keys? (y/n): ")
    while cfming not in ["y", "n"]:
        cfming = input("Invalid choice! Please type 'y' or 'n': ")
    if cfming == "y":
        keys = dkeys
        print("Keys successfully reseted...")
        time.sleep(0.5)
        print("Returning to main menu...")
        time.sleep(1.5)
        savesettings()
    else:
        print("Reset keys cancelled...")
        time.sleep(0.5)
        print("Returning to main menu...")
        time.sleep(1.5)


# update username
def updateuser():
    global pass1
    passy = input("Enter your current password: ")
    if passy != pass1:
        print("Incorrect password!")
        time.sleep(0.5)
        print("Returning to the main menu...")
        time.sleep(1.5)
        return

    while True:
        newuser = input("Enter new username: ")
        if any(account[0] == newuser for account in accounts):
            print("Username already exists! Please choose a different username.")
            continue
        newuser2 = input("Confirm new username: ")
        if newuser == newuser2:
            cfmuser = input(f"Confirm change username to '{newuser}'? (y/n): ")
            if cfmuser.lower() == "y":
                for r in accounts:
                    if passy in r:
                        r[0] = newuser
                        user1 = newuser
                        saveaccs()
                        print("New username saved...")
                        time.sleep(1.5)
                        return
                else:
                    print("Username change cancelled...")
                    time.sleep(1.5)
                    return
            elif cfmuser.lower() == "n":
                print("Username change cancelled...")
                time.sleep(1.5)
                return
        else:
            print("Usernames do not match!")


# update password
def updatepass():
    global pass1
    passy = input("Enter your current password: ")
    if passy != pass1:
        print("Incorrect password!")
        time.sleep(0.5)
        print("Returning to the main menu...")
        time.sleep(1.5)
        return

    while True:
        newpass = input("Enter new password: ")
        newpass2 = input("Confirm new password: ")

        if newpass == newpass2:
            cfmpass = input("Confirm change password? (y/n): ")

            while cfmpass.lower() not in ["y", "n"]:
                cfmpass = input("Invalid choice! Please type 'y' or 'n': ")

            if cfmpass.lower() == "y":
                for r in accounts:
                    if passy in r:
                        r[1] = newpass
                        pass1 = newpass
                        saveaccs()
                        print("New password saved...")
                        time.sleep(1.5)
                        return
                else:
                    print("Password change cancelled...")
                    time.sleep(1.5)
                    return
            elif cfmpass.lower() == "n":
                print("Password change cancelled...")
                time.sleep(1.5)
                return
        else:
            print("Passwords do not match!")


# reset password
def resetpass():
    entered_key = input("Enter the admin key: ")

    if entered_key == "admin123!":
        user_to_reset = input("Enter the username of the account to reset: ")
        for account in accounts:
            if account[0] == user_to_reset:
                new_pass = input("Enter the new password: ")
                new_pass_confirm = input("Confirm the new password: ")

                if new_pass == new_pass_confirm:
                    account[1] = new_pass
                    saveaccs()
                    print("Password reset successful...")
                    time.sleep(1.5)
                    return
                else:
                    print("Passwords do not match! Password reset cancelled...")
                    time.sleep(1.5)
                    return
            else:
                continue
        print("Username not found...")
        time.sleep(1.5)
    else:
        print("Incorrect admin key...")
        time.sleep(1.5)


# change keybinds
def editkeys():
    inp = input(
        """
Which key would you like to edit:
1. Add book button
2. Update book button
3. View books button
4. Search book button
5. Delete book button
6. Log out button
7. Settings button
Choice: """
    )
    while inp not in ["1", "2", "3", "4", "5", "6", "7"]:
        inp = input("Invalid choice! Please select 1, 2, 3, 4, 5, 6 or 7: ")

    action_mapping = {
        "1": ("add book", 0),
        "2": ("update book button", 1),
        "3": ("view books button", 2),
        "4": ("search book button", 3),
        "5": ("delete book button", 4),
        "6": ("log out button", 5),
        "7": ("settings button", 6),
    }

    if inp in action_mapping:
        global oldkey
        acty, ind = action_mapping[inp]
        current_key = keys[ind]
        oldkey = current_key
        new_keybind = input(
            f"Enter new key bind for {acty} (Current key: '{current_key}'): "
        )

        while keyval(new_keybind):
            retrying = input(
                "Keybind already in use! Do you want to re-enter it? (y/n): "
            )
            if retrying.lower() != "y":
                print("Keybind change cancelled...")
                time.sleep(1.5)
                return
            new_keybind = input(
                f"Enter new key bind for {acty} (current key: '{current_key}'): "
            )

        conkey(new_keybind, acty, ind)


# confirm chaneg keybind
def conkey(key, act, index):
    conkey = input(f"New key for {act} is {key}! Confirm? (y/n): ")
    while conkey.lower() not in ["y", "n"]:
        conkey = input("Invalid choice! Please type 'y' or 'n': ")
    if conkey.lower() == "y":
        print(f"New key successfully changed from {oldkey} to {key}...")
        time.sleep(1.5)
        keys[index] = key
        savesettings()
    else:
        print("Keybind change cancelled...")
        time.sleep(1.5)
        return


# check if keybind currenty in use
def keyval(key):
    for p in keys:
        if key.lower() == p.lower():
            return True
    return False


# welcome print
print(
    """
+==================================+     
|   WELCOME TO THE MINI LIBRARY!   | 
+==================================+"""
)

# main loop
while True:
    loginpage()
    main = True
    login = False
    passwordy = False

    while main == True:
        mainy()
