from telebot.async_telebot import AsyncTeleBot
from telebot import types
import asyncio
import config
import random

TG_TOKEN = config.TG_TOKEN
bot = AsyncTeleBot(TG_TOKEN)

def isint(func):
    try:
        int(func)
        return True
    except:
        return False

@bot.message_handler(content_types=['text'])
async def message_handler(message):
    msgsplit = message.text.split(' ')
    if msgsplit[0] == '/start':
        text = '''Привет, это Починатор, поздравь любого с починами\n'''
        text += '''Бот работает только в режиме инлайн, просто напишите в строку сообщений @pochinatorbot и введите имя или юз тому кого хотите поздравить с починами и свое послание по желанию. Пример: @pochinator Разраб с починами\n'''
        text += '''Также бот умеет считать процент почина, просто впишите любое число. Пример: @pochinator 3\n'''
        text += '''/info для информации о боте'''
        await bot.reply_to(message, text)
    elif msgsplit[0] in ['/about', '/info']:
        text = '''разраб: @xbox202\nканал разраба: @XboxOsu'''
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton('Github', 'https://github.com/XboXoffc/pochinator_bot')
        button2 = types.InlineKeyboardButton('DonationAlerts', 'https://www.donationalerts.com/r/xbox202')
        markup.add(button1, button2, row_width=1)
        await bot.reply_to(message, text, reply_markup=markup)

@bot.inline_handler(lambda query: isint(query.query))
async def procent_pochin(inline_query):
    querysplit = inline_query.query.split(' ')
    haircutday = int(querysplit[0])
    procent_pochin=(9)/(haircutday+12)*150-13
    procent_pochin = round(procent_pochin, 3)
    if procent_pochin < 0:
        procent_pochin = 0
    textr1 = f'''@{inline_query.from_user.username} не стригся ровно {haircutday} дней. Процент поздравления почин равняется {str(procent_pochin)}%\n\n'''
    if procent_pochin > 20:
        textr1 += f'''Будьте осторожны, всегда успейте отбить почины!'''
    else:
        textr1 += f'''Вы можете расслабиться, вас не смогут поздравить с починами, кайф!'''
    r1 = types.InlineQueryResultArticle('1', 'Какой у вас процент почин?', types.InputTextMessageContent(textr1), description='Напишите сколько дней вы не стриглись')
    await bot.answer_inline_query(inline_query.id, [r1])

@bot.inline_handler(lambda query: len(query.query) >= 0)
async def pozdravit_s_pochinami(inline_query):
    querysplit = inline_query.query.split(' ')
    textr = ''
    if len(inline_query.query) > 1:
        textr += f'''{querysplit[0]}, '''

    chance = random.randint(0, 100)
    if chance > 35:
        textr += f'''@{inline_query.from_user.username} треснул вам по ушам, с Починами!\n'''
    elif chance <= 35:
        textr += f'''@{inline_query.from_user.username} хотел треснуть вам по ушам, но к счатью вы среагировали и отбили удар!\n'''

    if len(querysplit) >= 2:
        querysplit.pop(0)
        textr += f'''\nЕго послание перед ударом: {' '.join(querysplit)}'''
    r = types.InlineQueryResultArticle('1', 'Поздравить друга с починами', types.InputTextMessageContent(textr), description='Напиши имя или юзернейм друга, а потом свое послание')
    await bot.answer_inline_query(inline_query.id, [r], cache_time=0)

print('БОТ ЗАПУЩЕН')
asyncio.run(bot.polling(True))

