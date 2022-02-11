from DataBaseEngine.SQLHandler import handle_query
from Application.commonFunctions import wrong_input
from Application.menuFunctions import menu_guest, commonMenuWithBack


def login_help():
    print("Please Enter your user details in following order")
    print("personal_code password")
    commonMenuWithBack()


successful_message = '***\nYoh have been logged in successfully\n***'


def login():
    login_help()
    while True:
        order = input().split()
        if order[0] == '*':
            login_help()
        elif order[0] == '..':
            print("***\nBack To Menu\n***")
            menu_guest()
            break
        else:
            if len(order) != 2:
                wrong_input()
                continue
            try:
                personal_code = order[0]
                password = order[1]
                res = handle_query(f'SELECT FROM users WHERE personal_code=={personal_code} AND password=={password}')
                if res[0] and len(res[1]) == 1:
                    user_id = res[1][0]['id']
                    print(successful_message)
                    return user_id
                if res[0] and len(res[1]) == 0:
                    print('No users with this login details have been found')
                    print('Please try again')
                    continue
                if not[res[0]]:
                    wrong_input()
            except:
                wrong_input()
