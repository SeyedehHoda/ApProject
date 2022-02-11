def commonMenuWithBack():
    print('Enter * to see this menu again, Enter .. to get back to last menu')


def commonMenuWithoutBack():
    print('Enter * to see this menu again')


def menu_guest():
    print("1. Register user")
    print('2. login')
    print("3. exit from application")
    commonMenuWithoutBack()


def menu_user():
    print("1. create new bank account")
    print("2. manage all of my accounts")
    print("3. make transaction")
    print("4. pay bill")
    print("5. get loan")
    print("6. close the bank account")
    print("7. logout user from the system")
    commonMenuWithoutBack()


def menu_account():
    print("1. take money from account")
    print("2. put money in account")
    print("3. view all account transactions")
    print("4. change account alias")
    print("5. make account common used")
    commonMenuWithBack()
