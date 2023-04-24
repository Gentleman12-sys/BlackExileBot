from aiogram.dispatcher import Dispatcher
from aiogram import Bot, types
from aiogram.utils import executor
import json
from math import ceil

import phonenumbers
from phonenumbers import carrier
from phonenumbers.phonenumberutil import number_type

token = 'BotAPI'
bot = Bot(token=token)
dp = Dispatcher(bot)



def user_debug(user):
    if user[0] == '8':
        user = list(user)
        del user[0]
        user.insert(0, '7')
        user.insert(0, '+')
        user = ''.join(user)
    return user

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply('Привет\nЯ бот который поможет вам найти неприятного клиента в списках бд\nfind - позволяет найти того или иного пользователя в базе find номер\nadd_grade - позволяет поставить оценку тому или иному пользователю add_grade номер оценка (от 1 до 5)')

@dp.message_handler(commands=['find'])
async def start(message: types.Message):
    with open('users.json', 'r') as file:
        users = json.load(file)
    user = message.text.split()[-1]
    user = user_debug(user)
    if users.get(user):
        text = f"""
                <em>Пользователь {user} найден</em>
                Общай оценка: {ceil(sum(users[user])/len(users[user]))*'⭐'}/⭐⭐⭐⭐⭐
                """
        for i in set(users[user]):
            text += f'\nКол-во {i*"⭐"}: {users[user].count(i)}'
        await bot.send_message(message.chat.id, text.replace('  ', ''), parse_mode='HTML')
    else:
        await bot.send_message(message.chat.id, '<em>Данного пользователя не найдено</em>', parse_mode='HTML')

@dp.message_handler(commands=['add_grade'])
async def add_grade(message: types.Message):
    with open('users.json', 'r') as file:
        users = json.load(file)
    user = message.text.split()[-2]
    user = user_debug(user)
    grade = int(message.text.split()[-1])
    grade = max(min(5, grade), 1)
    try:
        if not carrier._is_mobile(number_type(phonenumbers.parse(user))):
            await message.reply('<em>Данного номера не существует</em>', parse_mode='HTML')
            return False
    except:
        await message.reply('<em>Данного номера не существует</em>', parse_mode='HTML')
        return False
    if users.get(user):
        users[user].append(grade)
        print(grade)
        await message.reply(f'<em>Оценка  {grade*"⭐"} успешно добавлена</em>', parse_mode='HTML')
    else:
        users[user] = [grade]
        await message.reply(f'<em>Пользователь добавлен в базу данных\nОценка {grade*"⭐"} успешно добавлена</em>', parse_mode='HTML')
    with open('users.json', 'w') as file:
        json.dump(users, file)

if __name__ == '__main__':
    executor.start_polling(dp)