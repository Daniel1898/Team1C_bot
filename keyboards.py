from telebot.types import ReplyKeyboardMarkup, KeyboardButton

### Клавиатура для ответов ###

def getanswerkeyboard(num_of_variants):

    answer_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    answer_kb.row(KeyboardButton(str(1)),KeyboardButton(str(2)),KeyboardButton(str(3)))
    #for i in range(1,num_of_variants+1):
     #   answer_kb.add(KeyboardButton(str(i)))
    return answer_kb

def getmenukeyboard():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(KeyboardButton(str('Начать тест')),
    KeyboardButton(str('Предыдущий результат')),
    KeyboardButton(str('Наличие незавершонного теста')))
    return kb



