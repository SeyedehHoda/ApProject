from DataBaseEngine.SQLHandler import handle_query
from Application.commonFunctions import wrong_input
from Application.menuFunctions import menu_user, commonMenuWithBack
from DataBaseEngine.Table import Table
import random


def create_bank_account_help():
    password = input('please enter a password for your new account or .. for getting back: ')
    if password == '..':
        return None, None
    alias = input('You can use an alias for your new account, input the alias or NO for skipping this part: ')
    if alias == 'NO':
        alias = None
    return password, alias


successful_message = '***\nYour bank account successfully created, you can manage it in user menu\n***'


def generate_new_account_number():
    table = Table('bank_account')
    new_id = len(table.rowsList) + 1
    account_number = str(new_id)
    rest_number_len = 10 - len(str(new_id))
    for _ in range(rest_number_len):
        account_number += str(random.randint(0, 9))
    return new_id, account_number


def create_new_bank_account(user_id):
    while True:
        password, alias = create_bank_account_help()
        if not password:
            print("***\nBack To Menu\n***")
            menu_user()
            break
        try:
            new_id, account_number = generate_new_account_number()
            values = str(user_id) + ',' + password + ',' + account_number + ',0'
            res = handle_query(f'INSERT INTO bank_account VALUES ({values})')
            if res[0]:
                if not alias:
                    print(successful_message)
                    print(f'This is your new account number: {account_number}')
                    menu_user()
                    break
                values = str(user_id) + ',' + str(user_id) + ',' + str(new_id) + ',' + alias
                res = handle_query(f'INSERT INTO bank_account_common_used_aliases VALUES ({values})')
                if res[0]:
                    print(successful_message)
                    print(f'This is your new account number: {account_number}')
                    menu_user()
                    break
        except:
            wrong_input()
