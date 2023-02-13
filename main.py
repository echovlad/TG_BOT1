#!/usr/bin/env python3.9

import os
import telebot
from telebot import types
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
GROUP_ID = os.getenv('GROUP_ID')

client = telebot.TeleBot('BOT_TOKEN')

@client.message_handler(commands=['start'])
def start(message):
    mess = (f'Здравствуйте, <b>{message.from_user.first_name}! </b>' 
            f'Скажите, пожалуйста, что именно Вас интересует?')
    markup_inline = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text = '\U0001F60D Хочу оставить отзыв и получить бонус!', callback_data = 'first')
    btn2 = types.InlineKeyboardButton(text = '\U0001F612 Проблема с товаром', callback_data = 'second')
    btn3 = types.InlineKeyboardButton(text = '\N{smiling face with sunglasses} Другое', callback_data ='third')
    markup_inline.add(btn1, btn2, btn3)
    try:
        client.send_message(message.chat.id, mess, parse_mode = 'html', reply_markup= markup_inline )
    except Exception as e:
        print(e)

@client.callback_query_handler(func = lambda call: True)
def answer(call):
    if call.data == 'first':
        markup_inline = types.InlineKeyboardMarkup(row_width=1)
        text_btn = types.InlineKeyboardButton('Текстовый отзыв с бонусом 100 рублей', callback_data='text')
        photo_btn = types.InlineKeyboardButton('Фото отзыв с бонусом 150 рублей', callback_data='photo')
        markup_inline.add(text_btn, photo_btn)
        client.send_message(call.message.chat.id, 'Мы очень рады, что товар Вам понравился \U0001F60D ' 
        'Выберите, какой отзыв Вы хотите оставить.', parse_mode='html', reply_markup=markup_inline)

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

    elif call.data == 'text':
        mess = (f'Инструкция:\n'
                f'1. Нажмите на кнопку ниже и пройдите по ссылке на страницу купленного товара\n'
                f'2. Оставьте текстовый отзыв\n'
                f'3. После того, как отзыв будет опубликован - пришлите фото подтверждение (или скриншот отзыва) в этот чат.\n'
                f'4. Напишите номер телефона в этот чат, куда можно будет перевести 100 рублей'
                )
        markup_inline = types.InlineKeyboardMarkup()
        markup_inline.add(types.InlineKeyboardButton('Wildberries', url='http://www.wildberries.ru/seller/73371'))
        client.send_message(call.message.chat.id, mess, reply_markup=markup_inline)

    elif call.data == 'photo':
        mess = (f'Инструкция:\n'
                f'1. Нажмите на кнопку ниже и пройдите по ссылке на страницу купленного товара\n'
                f'2. Оставьте фотоотзыв\n'
                f'3. После того, как отзыв будет опубликован - пришлите фото подтверждение (или скриншот отзыва) в этот чат.\n'
                f'4. Напишите номер телефона в этот чат, куда можно будет перевести 150 рублей'
                )
        markup_inline = types.InlineKeyboardMarkup()
        markup_inline.add(types.InlineKeyboardButton('Wildberries', url='http://www.wildberries.ru/seller/73371'))
        client.send_message(call.message.chat.id, mess, reply_markup=markup_inline)

    elif call.data == 'broken':
        mess = (f'Нам очень жаль! Нужно понять, повреждение произошло в момент транспортировки или это заводской брак')
        markup_inline = types.InlineKeyboardMarkup(row_width=1)
        text_btn = types.InlineKeyboardButton('Коробка и товар повреждены', callback_data='broken1')
        photo_btn = types.InlineKeyboardButton('Коробка цела но товар поврежден', callback_data='broken1')
        markup_inline.add(text_btn, photo_btn)
        client.send_message(call.message.chat.id, mess, reply_markup=markup_inline)

    elif call.data == 'broken1':
        mess = (f'Нам очень жаль! Пришлите, пожалуйста, фото коробки и товара')
        client.send_message(call.message.chat.id, mess, parse_mode='html')

    elif call.data == 'another':
        mess = (f'Нам очень жаль! Пришлите, пожалуйста, фото несоответствия')
        client.send_message(call.message.chat.id, mess, parse_mode='html')

@client.message_handler(content_types=["text"])
def phone(message):
    mess = (f'Текст от пользователя -> @{message.from_user.username} \n')
    client.send_message("GROUP_ID", mess+message.text)
    client.reply_to(message, 'Ваше сообщение отправлено менеджеру, он свяжется с Вами в ближайшее время!')

@client.message_handler(content_types=["photo", "text"])
def photo(message):
    mess = (f'Фото от пользователя -> @{message.from_user.username} \ntext: {message.caption}')
    idphoto = message.photo[0].file_id
    client.send_photo("GROUP_ID", idphoto , caption=mess)
    client.send_message(message.chat.id, "Фото успешно загружено")

client.infinity_polling(timeout=10, long_polling_timeout = 5)
