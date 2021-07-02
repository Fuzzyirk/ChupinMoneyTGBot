from dbmethods import write_to_db, search_today

category_dict = {'unknown': []}


def parsing_message(message):
    message_parts = message.strip().split(' ')
    if len(message_parts) == 1:
        if '+' in message_parts[0]:
            return add_category(message_parts[0][1:].lower())
        elif '-' in message_parts[0]:
            if '#' in message_parts[0]:
                return del_tag(message_parts[0][2:].lower())
            else:
                return del_category(message_parts[0][1:].lower())
    elif len(message_parts) == 2:
        if message_parts[0].isdigit():
            return add_expense(int(message_parts[0]), message_parts[1].lower(), message)
        elif '+' in message_parts[0]:
            return add_income(int(message_parts[0]), message_parts[1].lower(), message)
        elif '#' in message_parts[0]:
            return add_tag_to_category(message_parts[0][1:].lower(), message_parts[1].lower())
        elif '-' in message_parts[0]:
            return del_expense(message_parts[0], message_parts[1])
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
        keys = keys + str(k) + ':\n' + values + '\n'
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
    return f"""Ктегория *{category}* добавлена"""


def del_category(category):
    if category != 'unknown':
        try:
            category_dict.pop(category)
        except KeyError:
            return f"""Ктегория *{category}* не найдена"""
        return f"""Ктегория *{category}* удалена"""
    else:
        return """Категория *Unknown* не может быть удалена"""


def del_tag(tag):
    category = _find_category(tag)
    if category != 'No category':
        if tag != category:
            category_dict[category].remove(tag)
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
                category_dict[category].append(tag)
                return f"""Тэг *{tag}* добавлен к категории *{category}*"""
    return f"""Категория *{category}* не найдена"""


def _find_category(tag):
    for k, v in category_dict.items():
        for t in v:
            if t == tag:
                return k
    return 'No category'


def add_income(income, tag, message):
    category = _find_category(tag)
    if category == 'No category':
        add_tag_to_category(tag, 'unknown')
        category = 'unknown'
    write_to_db(amount=income, message=message, category=category, tag=tag)
    return f"""Доход - *{income}*, тэг - *{tag}*, категория - *{category}*"""


def add_expense(expense, tag, message):
    category = _find_category(tag)
    if category == 'No category':
        add_tag_to_category(tag, 'unknown')
        category = 'unknown'
    write_to_db(amount=expense, message=message, category=category, tag=tag)
    return f"""Расход - *{expense}*, тэг - *{tag}*, категория - *{category}*"""


def find_last_operations():
    operations = search_today()
    text = ''
    if len(operations) > 0:
        for i in range(1, len(operations)+1):
            text = text + str(operations[i]['sum']) + ', ' + operations[i]['tag'] + ', ' + \
                   operations[i]['category'] + f' /del{i}\n'
    else:
        text = 'Операций за сегодня не найдено'
    return text


def del_expense(expense, tag):
    # del_from_db(expense, tag)
    return 'Удалено'
