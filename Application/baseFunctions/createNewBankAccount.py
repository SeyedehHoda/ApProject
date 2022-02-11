from DataBaseEngine.SQLHandler import handle_query
from Application.commonFunctions import wrong_input
from Application.menuFunctions import menu_user, commonMenuWithBack
from DataBaseEngine.Table import Table
import random


def create_bank_account_help():
    print("Please enter your bank account information in following order")
    print("account_alias password")
    commonMenuWithBack()


successful_message = '***\nYour bank account successfully created, you can manage it in user menu\n***'


def generate_new_account_number():
    table = Table('bank_account')
    new_id = len(table.rowsList) + 1
    account_number = str(new_id)
    rest_number_len = 10 - len(str(new_id))
    for _ in range(rest_number_len):
        account_number += str(random.randint(0, 9))
    return account_number


def create_new_bank_account(user_id):
    create_bank_account_help()
    while True:
        order = input().split()
        if order[0] == '*':
            create_bank_account_help()
        elif order[0] == '..':
            print("***\nBack To Menu\n***")
            menu_user()
            break
        else:
            if len(order) != 2:
                wrong_input()
                continue
            try:
                values = str(user_id) + ',' + ','.join(order) + ',' + generate_new_account_number() + ',0,false'
                res = handle_query(f'INSERT INTO bank_account VALUES ({values})')
                if res[0]:
                    print(successful_message)
                    menu_user()
                    break
            except:
                wrong_input()
