from DataBaseEngine.SQLHandler import handle_query
from Application.commonFunctions import wrong_input
from Application.menuFunctions import menu_guest, commonMenuWithBack


def register_help():
    print("Please Enter your information in following order")
    print("name personal_code password phone_number email")
    commonMenuWithBack()


successful_message = '***\nYou have been registered successfully\n***'


def register():
    register_help()
    while True:
        order = input().split()
        if order[0] == '*':
            register_help()
        elif order[0] == '..':
            print("***\nBack To Menu\n***")
            menu_guest()
            break
        else:
            if len(order) != 5:
                wrong_input()
                continue
            try:
                values = ','.join(order)
                res = handle_query(f'INSERT INTO users VALUES ({values})')
                if res[0]:
                    print(successful_message)
                    menu_guest()
                    break
                if not res[0]:
                    wrong_input()
            except:
                wrong_input()
