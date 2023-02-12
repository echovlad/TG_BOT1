import telebot
from telebot import types

client = telebot.TeleBot('6074955327:AAHImOUfUf2KmwRi0kLWpcEncEVKRhIxbh8')


@client.message_handler(commands=['start'])
def start(message):
    mess = (f'Здравствуйте, <b>{message.from_user.first_name}! </b>' 
            f'Скажите, пожалуйста, что именно Вас интересует?')
    markup_inline = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text = '\U0001F60D Хочу оставить отзыв и получить бонус!', callback_data = 'first')
    btn2 = types.InlineKeyboardButton(text = '\U0001F612 Проблема с товаром', callback_data = 'second')
    btn3 = types.InlineKeyboardButton(text = '\N{smiling face with sunglasses} Другое', callback_data ='third')

    markup_inline.add(btn1, btn2, btn3)
    client.send_message(message.chat.id, mess, parse_mode = 'html', reply_markup= markup_inline )

@client.callback_query_handler(func = lambda call: True)
def answer(call):
    if call.data == 'first':
        markup_inline = types.InlineKeyboardMarkup(row_width=1)
        text_btn = types.InlineKeyboardButton('Текстовый отзыв с бонусом 100 рублей', callback_data='text')
        photo_btn = types.InlineKeyboardButton('Фото отзыв с бонусом 150 рублей', callback_data='photo')

        markup_inline.add(text_btn, photo_btn)
        client.send_message(call.message.chat.id, 'Мы очень рады, что товар Вам понравился \U0001F60D ' 
        'Выберите, какой отзыв Вы хотите оставить.', parse_mode='html', reply_markup=markup_inline)

        if call.data == 'text':
            mess = (f'Инструкция:\n'
                    f'1. Нажмите на кнопку ниже и пройдите по ссылке на страницу купленного товара\n'
                    f'2. Оставьте текстовый отзыв\n'
                    f'3. После того, как отзыв будет опубликован - пришлите фото подтверждение (или скриншот отзыва) в этот чат.\n'
                    f'4. Напишите номер телефона в этот чат, куда можно будет перевести 100 рублей'
                    )
            markup_inline = types.InlineKeyboardMarkup()
            markup_inline.add(types.InlineKeyboardButton('Wildberries', url='http://www.wildberries.ru/'))
            client.send_message(call.message.chat.id, mess, reply_markup=markup_inline)

        elif call.data == 'photo':
            mess = (f'Инструкция:\n'
                    f'1. Нажмите на кнопку ниже и пройдите по ссылке на страницу купленного товара\n'
                    f'2. Оставьте текстовый отзыв\n'
                    f'3. После того, как отзыв будет опубликован - пришлите фото подтверждение (или скриншот отзыва) в этот чат.\n'
                    f'4. Напишите номер телефона в этот чат, куда можно будет перевести 100 рублей'
                    )
            markup_inline = types.InlineKeyboardMarkup()
            markup_inline.add(types.InlineKeyboardButton('Wildberries', url='http://www.wildberries.ru/'))
            client.send_message(call.message.chat.id, mess, reply_markup=markup_inline)

    elif call.data == 'second':
        markup_inline = types.InlineKeyboardMarkup(row_width=1)
        btn_1 = types.InlineKeyboardButton('Товар поврежден', callback_data = 'broken')
        btn_2 = types.InlineKeyboardButton('Товар не соответсвует описанию', callback_data = 'another')

        markup_inline.add(btn_1, btn_2)
        client.send_message(call.message.chat.id, 'Давайте разбираться в чем проблема.', parse_mode = 'html', reply_markup = markup_inline)

    elif call.data == 'third':
        mess = ('Напишите, пожалуйста, что Вас интересует,'
              ' и наш заботливый менеджер свяжется с Вами,'
              ' как только освободится')
        client.send_message(call.message.chat.id, mess, parse_mode='html')




client.polling(none_stop=True)
