from dbmethods import write_to_db, search_today, del_from_db, search_last
import pickle
import os.path
import datetime
import calendar

# TODO Сделать функцию поиска операций по имени/Дате


def cash_on_day():
    total = get_total()
    day_today = datetime.datetime.now().day
    if 0 < day_today < 15:
        zp_day = 15
        check_weekend = datetime.datetime.today().replace(day=zp_day).weekday()
        if check_weekend == 6:
            zp_day = 13
        elif check_weekend == 5:
            zp_day = 14
        day_to_zp = zp_day - day_today + 1
    elif 15 < day_today < 31:
        zp_day = calendar.monthrange(datetime.datetime.now().year, datetime.datetime.now().month)[1]
        check_weekend = datetime.datetime.today().replace(day=zp_day).weekday()
        if check_weekend == 6:
            zp_day = zp_day - 2
        elif check_weekend == 5:
            zp_day = zp_day - 1
        day_to_zp = zp_day - day_today + 1
    else:
        day_to_zp = 1
    return total / day_to_zp


def read_category_dict():
    if os.path.getsize('CatDict.txt') > 0:
        cat_dict = pickle.load(open('CatDict.txt', 'rb'))
    else:
        cat_dict = {'unknown': []}
        write_category_dict(cat_dict)
        cat_dict = pickle.load(open('CatDict.txt', 'rb'))
    return cat_dict


category_dict = read_category_dict()


def write_category_dict(cat_dict):
    pickle.dump(cat_dict, open('CatDict.txt', 'wb'))


def parsing_message(message, sender):
    message_parts = message.strip().split(' ')
    if len(message_parts) == 1:
        if '+' in message_parts[0]:
            return add_category(message_parts[0][1:].lower())
        elif '-' in message_parts[0]:
            if '#' in message_parts[0]:
                return del_tag(message_parts[0][2:].lower())
            else:
                return del_category(message_parts[0][1:].lower())
        elif '/' in message_parts[0]:
            return ''
        else:
            return 'Unknown command'
    elif len(message_parts) == 2:
        if message_parts[0].isdigit():
            return add_expense(int(message_parts[0]), message_parts[1].lower(), message, sender)
        elif '+' in message_parts[0]:
            return add_income(int(message_parts[0]), message_parts[1].lower(), message, sender)
        elif '#' in message_parts[0]:
            return add_tag_to_category(message_parts[0][1:].lower(), message_parts[1].lower())
        # elif '-' in message_parts[0]:
        #     return del_expense(message_parts[0], message_parts[1])
        else:
            return 'Unknown command'
    else:
        return 'Unknown command'


def show_categorys():
    keys = ''
    for k, v in category_dict.items():
        values = ''
        for t in v:
            values += str(t) + ','
        keys = keys + '*' + str(k) + '*' + ':\n' + values[:-1:] + '\n'
    return keys


def find_tag(tag):
    category = _find_category(tag)
    if category != 'No category':
        return f"""Тэг *{tag}* привязан к категории *{category}*"""
    else:
        return f"""Тэг *{tag}* не привязан к каким-либо категориям"""


def find_category(category):
    for k, v in category_dict.items():
        values = ''
        if k == category:
            for t in v:
                values += str(t) + ', '
            return f"""*{category}*:\n""" + values
        else:
            return f"""Категории *{category}* нету"""


def add_category(category):
    category_dict.setdefault(category, [category])
    if category in category_dict['unknown']:
        category_dict['unknown'].remove(category)
    write_category_dict(category_dict)
    return f"""Ктегория *{category}* добавлена"""


def del_category(category):
    if category != 'unknown':
        try:
            category_dict.pop(category)
        except KeyError:
            return f"""Ктегория *{category}* не найдена"""
        write_category_dict(category_dict)
        return f"""Ктегория *{category}* удалена"""
    else:
        return """Категория *Unknown* не может быть удалена"""


def del_tag(tag):
    category = _find_category(tag)
    if category != 'No category':
        if tag != category:
            category_dict[category].remove(tag)
            write_category_dict(category_dict)
            return f"""Тэг *{tag}* удален из категории *{category}*"""
        else:
            return f"""Тэг *{tag}* не может быть удален из одноименной категории *{category}*"""
    else:
        return f"""Тэга *{tag}* нету во всех категориях"""


def add_tag_to_category(tag, category):
    for k, v in category_dict.items():
        if category == k:
            if tag in v:
                return f"""Тэг *{tag}* уже есть!"""
            else:
                del_tag(tag)
                category_dict[category].append(tag)
                write_category_dict(category_dict)
                return f"""Тэг *{tag}* добавлен к категории *{category}*"""
    return f"""Категория *{category}* не найдена"""


def _find_category(tag):
    for k, v in category_dict.items():
        for t in v:
            if t == tag:
                return k
    return 'No category'


def add_income(income, tag, message, sender):
    category = _find_category(tag)
    if category == 'No category':
        add_tag_to_category(tag, 'unknown')
        category = 'unknown'
    total = get_total() + income
    write_to_db(amount=income,
                message=message,
                category=category,
                tag=tag,
                name=sender,
                operation='income',
                total=total)
    return f"""Доход - *{income}*, тэг - *{tag}*, категория - *{category}*, остаток - *{get_total()}*"""


def add_expense(expense, tag, message, sender):
    category = _find_category(tag)
    if category == 'No category':
        add_tag_to_category(tag, 'unknown')
        category = 'unknown'
    total = get_total() - expense
    write_to_db(amount=expense,
                message=message,
                category=category,
                tag=tag, name=sender,
                operation='expense',
                total=total)
    return f"""Расход - *{expense}*, тэг - *{tag}*, категория - *{category}*, остаток - *{get_total()}*"""


def find_last_operations():
    operations = search_today()
    text = ''
    if len(operations) > 0:
        for k, v in operations.items():
            text = text + str(operations[k]['sum']) + ', ' + operations[k]['tag'] + ', ' + \
                   operations[k]['category'] + ', ' + operations[k]['name'] + f' /del{k}\n'
    else:
        text = 'Операций за сегодня не найдено'
    return text


def del_expense(operation_id):
    del_operation = del_from_db(operation_id[4::])
    if del_operation:
        return f'Удалено. Остаток - {get_total()}"'
    else:
        return 'Операция не найена. Повторите поиск операций'


def get_total():
    total = search_last()['total']
    return total
