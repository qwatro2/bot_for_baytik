import os
from aiogram import Bot, Dispatcher, executor, types
import TikTokApi
import random
import logging
import funcs

TOKEN = ''

itembtn1 = types.KeyboardButton('Трендовый хэштег')
itembtn2 = types.KeyboardButton('Трендовый звук')
keyboard = types.ReplyKeyboardMarkup(True, False)
keyboard.row(itembtn1, itembtn2)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.DEBUG)


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await bot.send_message(
        message.chat.id,
        "Привет!\nТы попал к боту, которые будет радовать тебя тиктоками\n"
        "Для того, чтоб узнать, как работает бот, пиши /help", reply_markup=keyboard)


@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    await bot.send_message(message.chat.id, 'Кнопка "Трендовый хэштег" - ТикТок с трендовым хэштегом\n'
                                            'Кнопка "Трендовый звук" - ТикТок с трендовым звуком\n'
                                            'Если вы введете любой хэштег, с котором есть ролики, '
                                            'бот отправит вам случайный с этим хэштегом')


@dp.message_handler(text='Трендовый хэштег')
async def send_video_by_trending_hashtag(message: types.Message):
    await bot.send_message(message.chat.id, '<strong>Мы подбираем'
                                            ' Вам ТикТок с трендовым хэштегом</strong>',
                           parse_mode='HTML')
    try:
        filename, author_name, music_author, music_name = funcs.find_trending_hashtags()
        with open(filename, 'rb') as f:
            await bot.send_video(message.chat.id, f)
        await bot.send_message(message.chat.id, f'<strong>Автор</strong>: {author_name}\n'
                                                f'<strong>Звук</strong>: {music_author} - {music_name}',
                               parse_mode='HTML')
    except Exception as e:
        await bot.send_message(message.chat.id, '<i>Упс... Произошла ошибка</i>', parse_mode='HTML')
        print(e)


@dp.message_handler(text='Трендовый звук')
async def send_video_by_trending_music(message: types.Message):
    await bot.send_message(message.chat.id, '<strong>Мы подбираем'
                                            ' Вам ТикТок с трендовым звуком</strong>',
                           parse_mode='HTML')
    try:
        filename, author_name, music_author, music_name = funcs.find_trending_music()
        with open(filename, 'rb') as f:
            await bot.send_video(message.chat.id, f)
        await bot.send_message(message.chat.id, f'<strong>Автор</strong>: {author_name}\n'
                                                f'<strong>Звук</strong>: {music_author} - {music_name}',
                               parse_mode='HTML')
    except Exception as e:
        await bot.send_message(message.chat.id, '<i>Упс... Произошла ошибка</i>', parse_mode='HTML')
        print(e)


@dp.message_handler(content_types=['text'])
async def send_video_by_chosen_tiktok(message: types.Message):
    if len(str(message.text).split()) > 1:
        await bot.send_message(message.chat.id, '<i>Хэштег должен состоять из одного слова</i>', parse_mode='HTML')
        return
    elif str(message.text).count('#') > 1:
        await bot.send_message(message.chat.id, '<i>Введите один хэштег</i>', parse_mode='HTML')
        return

    await bot.send_message(message.chat.id, '<strong>Мы подбираем Вам '
                                            'ТикТок с выбранным хэштегом</strong>',
                           parse_mode='HTML')
    try:
        tag = str(message.text).lower()
        filename, author_name, music_author, music_name = funcs.find_hashtag_video(tag)
        try:
            with open(filename, "rb") as f:
                await bot.send_video(message.chat.id, f)
            await bot.send_message(message.chat.id,
                                   f'<strong>Автор</strong>: {author_name}\n'
                                   f'<strong>Звук</strong>: {music_author} - {music_name}',
                                   parse_mode='HTML')

        except Exception as e:
            await bot.send_message(message.chat.id, '<i>Упс... Произошла ошибка</i>', parse_mode='HTML')
            print(e)

    except KeyError as e:
        await bot.send_message(message.chat.id, '<i>Видео с таким хэштегом'
                                                ' еще не получили распространение</i>', parse_mode='HTML')
        print(e)


@dp.message_handler(content_types=['video'])
async def user_sent_video(message: types.Message):
    with open('funny.txt', 'w') as FILE:
        FILE.write(message['video']['file_id'] + '\n')
    await bot.send_video(message.chat.id, message['video']['file_id'])


@dp.message_handler(content_types=types.ContentTypes.ANY)
async def unknown_message(message: types.Message):
    await bot.send_message(message.chat.id, '<i>Ух ты... Качественный контент!</i>', parse_mode='HTML')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
    FILE.close()
