from state import State
from input import Input
from storage import Storage
from pyrogram.enums import ParseMode
from pyrogram.types import (InlineKeyboardMarkup,InlineKeyboardButton)

state = State()
storage = Storage()
input = Input(storage)


async def add(client, message):
    date = message.command[1] if len(message.command) > 1 else None
    await message.reply(
        "Запишите название и сумму в формате `-100 название`. Валюту указывать не надо",
        parse_mode=ParseMode.MARKDOWN
    )
    state.readInput('add', date)



async def today_sum(client, message):    
    sum = storage.get_today_sum(message.from_user.id)
    await message.reply(
        "Ваш итог за сегодня %+d руб." % sum,
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "Подробнее",
                    callback_data="today.list"
                ),
            ]
        ])
    )

async def week_sum(client, message):
    sum = storage.get_week_sum(message.from_user.id)
    await message.reply(
        "Ваш итог за неделю %+d руб." % sum,
    )

async def month_sum(client, message):
    sum = storage.get_month_sum(message.from_user.id)
    await message.reply(
        "Ваш итог за месяц %+d руб." % sum,
    )

async def read_input(client, message):
    lastCommand = state.handleCommand()

    # по умолчанию записывает новый расход
    if not lastCommand:
        input.add(message)
        await message.reply(
            "Ок"
        )
        return
    
    handler =  handlers[lastCommand]
    handler(message, state.get_parameters())
    await message.reply(
        "Ок"
    )

async def button_handler(client, callback_query):
    # todo считать последюю команду, для которой должен быть обработчик
    await callback_query.message.reply(
        '\n'.join(storage.get_today_list(callback_query.from_user.id))
    )

handlers = {
    "add": input.add
}