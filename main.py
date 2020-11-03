from datetime import datetime

import telebot
from telebot import *
from keyboards import *
from peewee import *
import models
from excel_tests import *

import requests

session = requests.Session()
session.verify = False

test1_number_of_questions = 30

#PROXY = 'http://t.me/proxy?server=www.mtproxygo.xyz&port=80&secret=dddd321456789012345678901234567921'
#apihelper.proxy = {'http': PROXY}
bot = telebot.AsyncTeleBot('1043528881:AAHaUG08xz8KAQjC4X1mr_epHD8r-QkgIAo')


@bot.message_handler(content_types=['text'])
def text_handler(message):
    if message.text == "/start":
        start_handler(message)
    if message.text == "Начать тест":
        start_test_handler(message)
    if message.text == "Предыдущий результат":
        prev_result_handler(message)
    if message.text == "/getAdmin -p t1c341522R":
        getAdmin(message)
    if message.text == "Наличие незавершонного теста":
        not_completed_test(message)
    if message.text in ['1', '2', '3', '4', '5']:
        question(message)


def not_completed_test(message):
    user = models.getUserById(message.from_user.id)
    if 1 <= user.current_question < test1_number_of_questions:
        keyboard = types.InlineKeyboardMarkup()
        key_yes = types.InlineKeyboardButton(text='Продолжить', callback_data='/continue_current_test')
        keyboard.add(key_yes)
        bot.send_message(user.id, text="Имеется не завершенный тест.", reply_markup=keyboard)
    else:
        bot.send_message(user.id, text="Не завершеннных тестов не имеется.")


def start_handler(message):
    try:
        user = models.getUserById(message.from_user.id)
    except Exception:
        user = models.User(id=message.from_user.id, current_question=0, rigth_answer_count=0)
        user.save(True)
    keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
    key_yes = types.InlineKeyboardButton(text='Начать тест', callback_data='/start_test')  # кнопка «Да»
    keyboard.add(key_yes)  # добавляем кнопку в клавиатуру
    bot.send_message(message.from_user.id, text="Привет! Начнем?",
                     reply_markup=getmenukeyboard())


def start_test_handler(message):
    user = models.getUserById(message.from_user.id)
    if 1 <= user.current_question < test1_number_of_questions:
        keyboard = types.InlineKeyboardMarkup()
        key_yes = types.InlineKeyboardButton(text='Продолжить', callback_data='/continue_current_test')
        key_no = types.InlineKeyboardButton(text='Начать сначала', callback_data='/restart_test')
        keyboard.add(key_yes)
        keyboard.add(key_no)
        bot.send_message(user.id, text="Имеется не завершенный тест.", reply_markup=keyboard)
    else:
        user.current_question = 0
        user.rigth_answer_count = 0
        res_message = get_question(user.current_question)
        bot.send_message(user.id, text=res_message, reply_markup=getanswerkeyboard(3))
        user.current_question += 1
        user.save()
        bot.register_next_step_handler(message, question)





def question(message):
    user = models.getUserById(message.from_user.id)
    if message.text == getAnswer(user.current_question):
        user.rigth_answer_count += 1
        user.save()

    if user.current_question == test1_number_of_questions:
        result = models.TestResult()
        result.user = user
        result.result = user.rigth_answer_count
        result.date = datetime.now()
        result.save()
        bot.send_message(message.from_user.id, text="Ваш результат " + str(user.rigth_answer_count) + " из " + str(test1_number_of_questions),
                         reply_markup=getmenukeyboard())
        send_result_to_admin(message.from_user, user.rigth_answer_count)
    else:
        res_message = get_question(user.current_question)
        bot.send_message(user.id, text=res_message, reply_markup=getanswerkeyboard(3))
        bot.register_next_step_handler(message, question)
        user.current_question += 1
        user.save()

def continue_test(call):
    user = models.getUserById(call.from_user.id)

    if user.current_question == test1_number_of_questions:
        result = models.TestResult()
        result.user = user
        result.result = user.rigth_answer_count
        result.date = datetime.now()
        result.save()
        bot.send_message(call.from_user.id, text="Ваш результат " + str(user.rigth_answer_count) + " из " + str(test1_number_of_questions),
                         reply_markup=getmenukeyboard())
        send_result_to_admin(call.from_user, user.rigth_answer_count)

    else:
        res_message = get_question(user.current_question)
        bot.send_message(user.id, text=res_message, reply_markup=getanswerkeyboard(3))
        user.current_question += 1
        user.save()


def prev_result_handler(message):
    tr = models.getLastUserResult(message.from_user.id)
    if tr == -1:
        bot.send_message(message.from_user.id, text="Вы еще не проходили тест",
                         reply_markup=getmenukeyboard())
    else:
        bot.send_message(message.from_user.id, text="Ваш предыдущий результат " + str(tr) + " из " + str(test1_number_of_questions),
                         reply_markup=getmenukeyboard())


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "/continue_current_test":
        continue_test(call)
    if call.data == "/restart_test":
        user = models.getUserById(call.from_user.id)
        user.current_question = 0
        user.save()
        continue_test(call)


def getAdmin(message):
    user = models.getUserById(message.from_user.id)
    user.is_admin = True
    user.save()


def send_result_to_admin(user_, result):
    admin_list = models.getAdminList()
    for admin in admin_list:
        bot.send_message(admin.id, text="Пользователь " + user_.first_name + " сдал тест на " + str(result) + " из " + str(test1_number_of_questions),
                         reply_markup=getmenukeyboard())


dbhandle = SqliteDatabase("postgres://ykjfzkpfewpdxw:6bafd3cb6ba66f44891774c739bc7076b3b9ad1d902d3da29c1c18e30d894085@ec2-34-235-108-68.compute-1.amazonaws.com:5432/de85etgjvkelqr")  # или :memory: чтобы сохранить в RAM


bot.polling(none_stop=True, interval=0)
