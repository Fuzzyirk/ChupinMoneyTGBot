from config import TOKEN
import telebot
import logic

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['help'])
def command_help(message):
    bot.reply_to(message, "<Сумма> <Тэг/Категория> - Добавить расходы (200 такси)\n"
                          "+<Сумма> <Категория>  - Добавить поступление(+5000 ЗП)\n"
                          "+<Категория> - Добавить категорию (+Продкуты)\n"
                          "-<Категория> - Удалить категорию (+Продкуты)\n"
                          "#<Тэг> <Категория> - Добавить тэг к категории (#памперсы дети)\n"
                          "-#<Тэг> <Категория> - Удалить тэг из категории (-#памперсы дети)")


@bot.message_handler(commands=['start'])
def command_start(message):
    bot.reply_to(message, "Просмотр категорий /category\n"
                          "Поиск тэга /findTag\n"
                          "Удаление операций /deltoday\n")


@bot.message_handler(commands=['category'])
def command_start(message):
    bot.reply_to(message, logic.show_categorys())


@bot.message_handler(commands=['deltoday'])
def show_today_operations(message):
    bot.reply_to(message, logic.find_last_operations())


@bot.message_handler(commands=['del1'])
def del_operation(message):
    print('удаляю!')


def listener(messages):
    for m in messages:
        chatid = m.chat.id
        if m.content_type == 'text':
            text = m.text
            answear = logic.parsing_message(text)
            bot.send_message(chatid, answear, parse_mode="Markdown")


if __name__ == '__main__':
    bot.set_update_listener(listener)  # register listener
    bot.polling(none_stop=True)
    while True:  # Don't let the main Thread end.
        pass

