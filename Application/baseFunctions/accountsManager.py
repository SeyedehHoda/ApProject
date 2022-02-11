from Application.commonFunctions import wrong_input, get_account_id
from Application.menuFunctions import menu_user, commonMenuWithBack
from DataBaseEngine.SQLHandler import handle_query


def list_all_user_accounts(user_id):
    accounts = handle_query(f'SELECT FROM bank_account WHERE user_id=={user_id} AND is_active==true')[1]
    print('This is all of your bank accounts,'
          ' enter each account number to manage it or enter .. to get back to the menu')
    for index, account in enumerate(accounts):
        account_id = account['id']
        alias = handle_query(f'SELECT FROM bank_account_common_used_aliases WHERE'
                             f' account_id=={account_id} AND alias_user_id=={user_id}')[1]
        if len(alias):
            alias = alias[0]
        else:
            alias = None
        account_number = account['account_number']
        print(f'{index + 1}. account number {account_number}', end='')
        if alias:
            alias_name = alias['alias']
            print(f' with alias {alias_name}')
        else:
            print()
    while True:
        order = input()
        if order == '..':
            print("***\nBack To Menu\n***")
            menu_user()
            return
        try:
            index = int(order) - 1
            return manage_account(accounts[index])
        except:
            wrong_input()


def menu_account():
    print("1. view all account transactions")
    print("2. close the account")
    commonMenuWithBack()


def list_all_account_transactions(account_id):
    transactions = handle_query(f'SELECT FROM transactions WHERE '
                                f'from_account_id=={account_id} OR to_account_id=={account_id}')[1]
    for transaction in transactions:
        amount = transaction['money']
        if transaction['bill_id'] == 'null':
            if int(transaction['from_account_id']) == int(account_id):
                other_person_account_id = transaction['to_account_id']
                account = handle_query(f'SELECT FROM bank_account WHERE id=={other_person_account_id} AND is_active=true')[1][0]
                account_number = account['account_number']
                print(f'Move {amount} Toman to account number {account_number}')
            elif int(transaction['to_account_id']) == int(account_id):
                other_person_account_id = transaction['from_account_id']
                account = handle_query(f'SELECT FROM bank_account WHERE id=={other_person_account_id} AND is_active==true')[1][0]
                account_number = account['account_number']
                print(f'Get {amount} Toman from account number {account_number}')
        else:
            print(f'Payed {amount} Toman for paying the bill')


def close_the_account(account):
    destination_account = None
    if int(account['money']) != 0:
        print("You Have to move your money to another account")
        account_id = get_account_id(account['user_id'], 'moneyDestination')
        if account_id == 'back_code':
            return
        destination_account = handle_query(f'SELECT FROM bank_account WHERE id=={account_id} AND is_active==true')[1][0]
    my_account_id = account['id']
    if destination_account:
        money = int(account['money'])
        destination_account_id = destination_account['id']
        values1 = str(account['id']) + ',' + str(destination_account_id) + ',null,' + str(money)
        handle_query(f'INSERT INTO transactions VALUES ({values1})')
        values3 = destination_account['user_id'] + ',' + destination_account['password'] \
                  + ',' + destination_account['account_number'] + ',' \
                  + str(int(destination_account['money']) + money) + ',true'
        handle_query(f'UPDATE bank_account where id=={destination_account_id} VALUES ({values3})')
    values2 = account['user_id'] + ',' + account['password'] \
              + ',' + account['account_number'] + ',0,false'
    res2 = handle_query(f'UPDATE bank_account where id=={my_account_id} VALUES ({values2})')
    if res2[0]:
        print('account has been closed successfully')
        menu_user()
        return


def manage_account(account):
    while True:
        menu_account()
        order = input()
        if order == '*':
            menu_account()
        elif order == '..':
            print('***\nBack To Menu\n***')
            menu_user()
            break
        elif order == '1':
            return list_all_account_transactions(account['id'])
        elif order == '2':
            return close_the_account(account)
        else:
            wrong_input()





