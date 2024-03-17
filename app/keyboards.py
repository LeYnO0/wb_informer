from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Получить информацию по товару ℹ️')],
    [KeyboardButton(text='Остановить уведомления 🚫')],
    [KeyboardButton(text='Получить информацию из БД 📁')],
], resize_keyboard=True)

subscribe = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Подписаться', callback_data='subscribe')]
])
