from classes import MY_BOOK, Record, FILE_NAME


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return 'This contact doesnt exist, please try again.'
        except ValueError as exception:
            return exception.args[0]
        except IndexError:
            return 'This contact cannot be added, it exists already'
        except TypeError:
            return 'Unknown command or parametrs, please try again.'
    return inner


@input_error
def add_user(args):
    name, phone = args
    if name not in MY_BOOK:
        MY_BOOK.add_record(Record(name, phone))
        return f'User {name} added with phone {phone}'
    MY_BOOK[name].add_phone(phone)
    return f'Adding a new tel {phone} for {name}'


def avaliable_comands(_):
    return '''
    Use "add" *name* *phone* to add new user.
    Use "change" *name* *phone* to change user\'s number.
    Use "show" or "show all" to see all adress book. 
    Use "exit" or "q" to exit from bot.
    Use "del" *user* or "delete" to delete user.
    Use "birthday" *user* *birthday* to add birthday to contact in format "DD-MM-YYY".
    Use "next" *user* if you want to know how mane days before birthday.
    Use "save" to save your contacts.
    Use "search" *name* to find user's info.
    '''


@input_error
def birthday_func(args):
    name, date = args[0], args[1]
    record = MY_BOOK[name]
    record.add_birthday(date)
    return f'For {name} you added Birthday {date}'


@input_error
def change_phone(args):
    name, new_phone, old_phone = args
    old_phone = MY_BOOK.get(name)
    print(old_phone)
    MY_BOOK[name].edit_phone(old_phone, new_phone)
    return f'User {name} have a new phone number. Old number was {old_phone}'


@input_error
def delete_user(args):
    name = args[0]
    MY_BOOK.remove_record(name)
    return f"User with name {name} was deleted"


def exit(_):
    print("Good Bye!!!")
    return 'exit'


def hello(_):
    return "Can I help you? Write something to me:) You can see the avaliable commands by 'help' command"


@input_error
def next_birthday_func(name):
    record = MY_BOOK[name[0]]
    return f"Days to next {name[0]}'s birthday will be in {record.get_days_to_next_birthday()} days."


def save_func(_):
    MY_BOOK.save_contacts(FILE_NAME)
    print("Contacts saved")


@input_error
def search_record(args):
    records = MY_BOOK.search(args[0].capitalize())
    search_records = " "
    for record in records:
        search_records += f'{record.get_info()}\n'
    return search_records


def show_all(_):
    MY_BOOK.look_book()
    return ""


@input_error
def show_number(args):
    user = args[0]
    phone = MY_BOOK[user]
    return f'{user} : {[tel.value for tel in phone.phones]}'


HANDLERS = {
    "hello": hello,
    'good bye': exit,
    'close': exit,
    'exit': exit,
    'q': exit,
    'add': add_user,
    'change': change_phone,
    'show': show_all,
    'show all': show_all,
    'phone': show_number,
    'help': avaliable_comands,
    'del': delete_user,
    'delete': delete_user,
    'search': search_record,
    'birthday': birthday_func,
    'next': next_birthday_func,
    'save': save_func
}


def parser_input(user_input):
    cmd, *args = user_input.split()
    try:
        handler = HANDLERS[cmd.lower()]
    except KeyError:
        if args:
            cmd = f'{cmd} {args[0]}'
            args = args[1:]
        else:
            def handler(_): return "Unknown command"
    return handler, args
