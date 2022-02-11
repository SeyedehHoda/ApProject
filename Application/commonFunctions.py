from DataBaseEngine.SQLHandler import handle_query
from Application.menuFunctions import commonMenuWithBack, menu_user


def wrong_input():
    print('***')
    print('Wrong input, Please try again')
    print('Enter * to watch menu again')
    print('***')


def print_accounts(accounts_dic):
    print('This is your aliases list:')
    for alias, account in accounts_dic.items():
        user_id = account['user_id']
        user = handle_query(f'SELECT FROM users WHERE id=={user_id}')[1][0]
        user_name = user['name']
        account_number = account['account_number']
        printed_value = f'{alias} with number = {account_number} for user {user_name}'
        print(printed_value)


def convert_aliases_list_to_accounts_dic(aliases):
    accounts_dic = {}
    for alias_dic in aliases:
        account_id = alias_dic['account_id']
        account = handle_query(f'SELECT FROM bank_account WHERE id=={account_id} AND is_active==true')[1][0]
        accounts_dic[alias_dic['alias']] = account
    return accounts_dic


def choose_from_aliases_menu(alias_user_id, owner_user_id):
    if owner_user_id:
        aliases = handle_query(
            f'SELECT FROM bank_account_common_used_aliases'
            f' WHERE alias_user_id=={alias_user_id} AND owner_user_id=={owner_user_id}'
        )[1]
    else:
        aliases = handle_query(
            f'SELECT FROM bank_account_common_used_aliases'
            f' WHERE alias_user_id=={alias_user_id}'
        )[1]
    accounts_dic = convert_aliases_list_to_accounts_dic(aliases)
    print_accounts(accounts_dic)
    while True:
        print('** open alias name or .. for getting back')
        order = input()
        if order == '..':
            return None
        account = accounts_dic.get(order, None)
        if account:
            return account['id']
        else:
            print('wrong alias name')


def add_new_bank_number_handler(user_id):
    while True:
        bank_number = input('please enter the bank number: ')
        bank_account = handle_query(f'SELECT FROM bank_account WHERE account_number=={bank_number} AND is_active==true')[1]
        if len(bank_account):
            bank_account = bank_account[0]
            order = input(
                'Do You want to add this number to common used numbers, if yes enter alias and if no enter NO: '
            )
            while True:
                if order == 'NO':
                    return bank_account['id']
                owner_user_id = bank_account['user_id']
                values = str(user_id) + ',' + str(owner_user_id) + ',' + str(bank_account['id']) + ',' + order
                res = handle_query(f'INSERT INTO bank_account_common_used_aliases VALUES ({values})')
                if res[0]:
                    return bank_account['id']
                else:
                    order = input('enter new alias or NO for getting back')
        else:
            print('wrong bank number')


def account_number_menu(where):
    print(f'Please choose your {where} account from your common used list or enter your {where} account number')
    print("1. choose from aliases")
    print("2. Enter new account number")
    commonMenuWithBack()


def get_account_id(user_id, where):
    account_number_menu(where)
    while True:
        order = input()
        account_id = None
        if order == '1':
            account_id = choose_from_aliases_menu(
                user_id,
                user_id if 'origin' else None
            )
        elif order == '2':
            account_id = add_new_bank_number_handler(user_id)
        elif order == '..':
            print("***\nBack To Menu\n***")
            menu_user()
            return 'back_code'
        elif order == '*':
            account_number_menu(where)
        if account_id:
            return account_id
        else:
            account_number_menu(where)
