import os
from aiogram import Bot, Dispatcher, executor, types
import TikTokApi
from TikTokApi.browser import set_async
import random

TOKEN = '1305765980:AAEF2l7lyATX7sHHLuv2HVZPOMDKqfVnNak'

itembtn1 = types.KeyboardButton('Режим поиска по тегу')
itembtn2 = types.KeyboardButton('Трендовый хэштег')
itembtn3 = types.KeyboardButton('Трендовый звук')
keyboard = types.ReplyKeyboardMarkup(True, False)
keyboard.row(itembtn1, itembtn2, itembtn3)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
api = TikTokApi.TikTokApi()

set_async()


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await bot.send_message(
        message.chat.id,
        "Привет!\nТы попал к боту, которые будет радовать тебя тиктоками\n"
        "Для того, чтоб узнать список команд, пиши /help", reply_markup=keyboard)


@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    await bot.send_message(message.chat.id, 'Кнопка "Режим поиска по тегу" - '
                                            'напишите любой хэштег и получите ТикТок\n'
                                            'Кнопка "Трендовый хэштег" - ТикТок с трендовым хэштегом\n'
                                            'Кнопка "Трендовый звук" - ТикТок с трендовым звуком')


@dp.message_handler(text='Трендовый хэштег')
async def send_video_by_trending_hashtag(message: types.Message):
    await bot.send_message(message.chat.id, '<strong>Мы подбираем'
                                            ' Вам ТикТок с трендовым хэштегом</strong>',
                           parse_mode='HTML')
    hashtag = random.choice(api.discoverHashtags())["cardItem"]["title"]
    videos = api.byHashtag(hashtag, language="ru", count=100)
    hashtag = random.choice(videos)
    url = hashtag["itemInfos"]["video"]["urls"][0]
    video = api.get_Video_By_DownloadURL(url, language="ru")
    name = hashtag['itemInfos']['id'] + '.mp4'
    try:
        with open(name, "wb") as f:
            f.write(video)
        with open(name, "rb") as f:
            await bot.send_video(message.chat.id, f)
        os.remove(name)
        await bot.send_message(message.chat.id,
                               '<strong>Автор</strong>: {}\n'
                               '<strong>Звук</strong>: {} - {}'.format(hashtag['authorInfos']['nickName'],
                                                                       hashtag['musicInfos']['authorName'],
                                                                       hashtag['musicInfos']['musicName']),
                               parse_mode='HTML')
    except Exception as e:
        await bot.send_message(message.chat.id, '<i>Упс... Произошла ошибка</i>', parse_mode='HTML')
        print(e)


@dp.message_handler(text='Трендовый звук')
async def send_video_by_trending_music(message: types.Message):
    await bot.send_message(message.chat.id, '<strong>Мы подбираем'
                                            ' Вам ТикТок с трендовым звуком</strong>',
                           parse_mode='HTML')
    music = random.choice(api.discoverMusic())['cardItem']['id']
    videos = api.bySound(music, language='ru', count=100)
    music = random.choice(videos)
    url = music['itemInfos']['video']['urls'][0]
    video = api.get_Video_By_DownloadURL(url, language="ru")
    name = music['itemInfos']['id'] + '.mp4'
    try:
        with open(name, "wb") as f:
            f.write(video)
        with open(name, "rb") as f:
            await bot.send_video(message.chat.id, f)
        os.remove(name)
        await bot.send_message(message.chat.id,
                               '<strong>Автор</strong>: {}\n'
                               '<strong>Звук</strong>: {} - {}'.format(music['authorInfos']['nickName'],
                                                                       music['musicInfos']['authorName'],
                                                                       music['musicInfos']['musicName']),
                               parse_mode='HTML')
    except Exception as e:
        await bot.send_message(message.chat.id, '<i>Упс... Произошла ошибка</i>', parse_mode='HTML')
        print(e)


@dp.message_handler(text=['Режим поиска по тегу'])
async def send_video_by_chosen_hashtag(message: types.Message):
    await bot.send_message(message.chat.id, "<strong>Режим поиска по тегу включен</strong>", parse_mode='HTML')

    @dp.message_handler(content_types=types.ContentTypes.ANY)
    async def func(message: types.Message):
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
            text = str(message.text).lower()
            hashtag = text[1 if text[0] == '#' else 0:]
            videos = api.byHashtag(hashtag, count=100)
            hashtag = random.choice(videos)
            url = hashtag['itemInfos']['video']['urls'][0]
            video = api.get_Video_By_DownloadURL(url, language="ru")
            name = hashtag['itemInfos']['id'] + '.mp4'
            try:
                with open(name, "wb") as f:
                    f.write(video)
                with open(name, "rb") as f:
                    await bot.send_video(message.chat.id, f)
                os.remove(name)
                await bot.send_message(message.chat.id,
                                       '<strong>Автор</strong>: {}\n'
                                       '<strong>Звук</strong>: {} - {}'.format(hashtag['authorInfos']['nickName'],
                                                                               hashtag['musicInfos']['authorName'],
                                                                               hashtag['musicInfos']['musicName']),
                                       parse_mode='HTML')
            except Exception as e:
                await bot.send_message(message.chat.id, '<i>Упс... Произошла ошибка</i>', parse_mode='HTML')
                print(e)

        except KeyError:
            await bot.send_message(message.chat.id, '<i>Видео с таким хэштегом'
                                                    ' еще не получили распространение</i>', parse_mode='HTML')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
