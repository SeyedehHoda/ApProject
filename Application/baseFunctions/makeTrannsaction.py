from DataBaseEngine.SQLHandler import handle_query
from Application.commonFunctions import get_account_id
from Application.menuFunctions import menu_user


def make_transaction(user_id):
    origin_account_id = get_account_id(user_id, 'origin')
    if origin_account_id == 'back_code':
        return
    origin_account = handle_query(f'SELECT FROM bank_account WHERE id=={origin_account_id}')[1][0]
    if int(origin_account['user_id']) != int(user_id):
        print('Error: the origin account should be for the logged in user')
        return make_transaction(user_id)
    password = input('Please give me the password of this bank account: ')
    while True:
        if password == '..':
            menu_user()
            return
        if origin_account['password'] != password:
            print('Error: The entered password is wrong')
            password = input('Enter password again or enter .. to get back to the menu')
        else:
            break
    destination_account_id = get_account_id(user_id, 'destination')
    if destination_account_id == 'back_code':
        return
    destination_account = handle_query(f'SELECT FROM bank_account WHERE id=={destination_account_id}')[1][0]
    if origin_account_id == destination_account_id:
        print('Error: Origin and destination account can not be same')
        return make_transaction(user_id)
    money = int(input('Enter the amount of money you want to move: '))
    if money > int(origin_account['money']):
        print('Error: You DO NOT have enough money to make this transaction')
        menu_user()
        return
    values1 = str(origin_account_id) + ',' + str(destination_account_id) + ',null,null,' + str(money)
    res1 = handle_query(f'INSERT INTO transactions VALUES ({values1})')
    values2 = origin_account['user_id'] + ',' + origin_account['password'] \
              + ',' + origin_account['account_number'] + ',' + str(int(origin_account['money']) - money)
    res2 = handle_query(f'UPDATE bank_account where id=={origin_account_id} VALUES ({values2})')
    values3 = destination_account['user_id'] + ',' + destination_account['password'] \
              + ',' + destination_account['account_number'] + ',' \
              + str(int(destination_account['money']) + money)
    res3 = handle_query(f'UPDATE bank_account where id=={destination_account_id} VALUES ({values3})')
    if res1[0] and res2[0] and res3[0]:
        print('transaction done successfully')
        menu_user()
        return
