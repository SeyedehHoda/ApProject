from DataBaseEngine.SQLHandler import handle_query
from Application.commonFunctions import wrong_input, get_account_id
from Application.menuFunctions import menu_user, commonMenuWithBack


def bill_help():
    print("Please Enter your bill details in following order")
    print("bill_id bill_payment_id bill_amount")
    commonMenuWithBack()


successful_message = '***\nYour bill have been successfully paid\n***'


def payBill(user_id):
    account_id = get_account_id(user_id, 'payBill')
    if account_id == 'back_code':
        return
    account = handle_query(f'SELECT FROM bank_account WHERE id=={account_id} AND is_active==true')[1][0]
    bill_help()
    while True:
        order = input().split()
        if order[0] == '*':
            bill_help()
        elif order[0] == '..':
            print("***\nBack To Menu\n***")
            menu_user()
            break
        else:
            if len(order) != 3:
                wrong_input()
                continue
            try:
                bill_id = order[0]
                bill_amount = int(order[2])
                if bill_amount > int(account['money']):
                    print('Error: Bill amount is more than your account money')
                    return payBill(user_id)
                valuesTransaction = str(account_id) + ',null,' + str(bill_id) + ',' + str(bill_amount)
                resTransaction = handle_query(f'INSERT INTO transactions VALUES ({valuesTransaction})')
                valuesAccount = account['user_id'] + ',' + account['password'] \
                          + ',' + account['account_number'] + ',' + str(int(account['money']) - bill_amount) + ',true'
                resAccount = handle_query(f'UPDATE bank_account where id=={account_id} VALUES ({valuesAccount})')
                if not resAccount[0] or not resTransaction[0]:
                    wrong_input()
                else:
                    print(successful_message)
                    menu_user()
                    break
            except:
                wrong_input()
