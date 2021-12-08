import telebot
from telebot import types
import logic
import os
from dotenv import load_dotenv

IDS = [216982492]
load_dotenv()
bot = telebot.TeleBot(os.getenv('TOKEN'))

# TODO сделать деплой
# TODO организовать код на вебхуках
# TODO сделать метод для коанды findtag


@bot.message_handler(commands=['help'])
def command_help(message):
    print(message)
    if message.chat.id in IDS:
        bot.reply_to(message, """*Добавить расходы:*\n"""
                              """<Сумма> <Тэг/Категория>  _200 такси_\n"""
                              """*Добавить поступление:*\n"""
                              """+<Сумма> <Категория>  _+5000 ЗП_\n"""
                              """*Добавить категорию:*\n"""
                              """+<Категория>  _+Продкуты_\n"""
                              """*Удалить категорию *\n"""
                              """-<Категория>  _-Продкуты_\n"""
                              """*Добавить тэг к категории:*\n"""
                              """#<Тэг> <Категория>  _#памперсы дети_\n"""
                              """*Удалить тэг из категории:*\n"""
                              """-#<Тэг> <Категория>  _-#памперсы дети_""", parse_mode="Markdown")
    else:
        bot.reply_to(message, "Access denied")


@bot.message_handler(commands=['start'])
def command_start(message):
    print(message)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    itembtn1 = types.KeyboardButton('/start')
    itembtn2 = types.KeyboardButton('/help')
    markup.add(itembtn1, itembtn2)
    if message.chat.id in IDS:
        bot.reply_to(message, "*Помощь по командам* /help\n"
                              "*Просмотр категорий* /category\n"
                              "*Поиск тэга* /findTag\n"
                              "*Показать остаток* /showTotal\n"
                              "*Показать остаток в день до ЗП* /showCashAtDay\n"
                              "*Удаление операций* /deltoday\n", reply_markup=markup, parse_mode="Markdown")
    else:
        bot.reply_to(message, "Access denied")


@bot.message_handler(commands=['showCashAtDay'])
def command_cash_at_day(message):
    if message.chat.id in IDS:
        text = f'Можно тратить в день до следущей ЗП: {logic.cash_on_day()}'
        bot.send_message(message.chat.id, text)
    else:
        bot.reply_to(message, "Access denied")

@bot.message_handler(commands=['showTotal'])
def command_total(message):
    if message.chat.id in IDS:
        text = f'Остаток: {logic.get_total()}'
        bot.send_message(message.chat.id, text)
    else:
        bot.reply_to(message, "Access denied")


@bot.message_handler(commands=['category'])
def command_start(message):
    print(message)
    if message.chat.id in IDS:
        bot.reply_to(message, logic.show_categorys(), parse_mode="Markdown")
    else:
        bot.reply_to(message, "Access denied")


@bot.message_handler(commands=['deltoday'])
def show_today_operations(message):
    if message.chat.id in IDS:
        bot.reply_to(message, logic.find_last_operations())
    else:
        bot.reply_to(message, "Access denied")


@bot.message_handler(regexp="/del+\d+")
def del_operation(message):
    del_markup = types.InlineKeyboardMarkup()
    btn_del = types.InlineKeyboardButton(text='Удалить', callback_data='del')
    btn_cancel = types.InlineKeyboardButton(text='Отмена', callback_data='cancel')
    del_markup.add(btn_del, btn_cancel)
    bot.send_message(message.chat.id, 'Удалить операцию?', parse_mode="Markdown", reply_markup=del_markup)
    global need_del
    need_del = message.text


@bot.callback_query_handler(func=lambda call: True)
def call_handler(call):
    if call.data == 'del':
        bot.send_message(call.message.chat.id, logic.del_expense(need_del))
    elif call.data == 'cancel':
        bot.send_message(call.message.chat.id, 'Отменено')


@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    if m.chat.id in IDS:
        answear = logic.parsing_message(m.text, m.from_user.first_name)
        if answear == 'Unknown command':
            answear = answear + ' /help'
        bot.send_message(m.chat.id, answear, parse_mode="Markdown")
    else:
        bot.reply_to(m, "Access denied")


if __name__ == '__main__':
    logic.read_category_dict()
    bot.polling(none_stop=True)
