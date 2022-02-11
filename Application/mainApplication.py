from Application.menuFunctions import *
from Application.baseFunctions.register import register
from Application.baseFunctions.login import login
from Application.baseFunctions.createNewBankAccount import create_new_bank_account
from Application.commonFunctions import wrong_input

menu_guest()
login_user_id = None

while True:
    order = input()
    if not login_user_id:
        if order == '1':
            register()
        elif order == '2':
            login_user_id = login()
            menu_user()
        elif order == '3':
            exit(0)
        elif order == '*':
            menu_guest()
        else:
            wrong_input()
    else:
        if order == '*':
            menu_user()
        elif order == '1':
            create_new_bank_account(login_user_id)
        elif order == '2':
            accounts_manager()
        elif order == '3':
            make_transaction()
        elif order == '4':
            pay_bill()
        elif order == '5':
            get_loan_from_bank()
        elif order == '6':
            close_the_bank_account()
        elif order == '7':
            login_user_id = None
            print('***\nSuccessfully logged out from bank\n***')
            menu_guest()
        else:
            wrong_input()
