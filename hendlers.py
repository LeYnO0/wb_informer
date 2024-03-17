import asyncio
import requests

from datetime import datetime
from sqlalchemy import select
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from config import GETITEM_URL
from database import async_session
from models import RequestInfo
import app.keyboards as keyboards

router = Router()

# Создаем машину состояния


class GetArticle(StatesGroup):
    article = State()


# Приветствуем нового пользователя и показываем reply-калвиатуру
@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f'Привет, {message.from_user.first_name}. Я помогу тебе в поиске информации по артикулам Wildberries 🍒', reply_markup=keyboards.main)


# Получаем и работаем с артикулом товара
@router.message(F.text == 'Получить информацию по товару ℹ️')
async def cmd_get_wb_data(message: Message, state: FSMContext):
    await state.set_state(GetArticle.article) # Устанавливаем машину состояния в ожидание артикула
    await message.answer(f'Введите артикул товара:') # Запрашиваем артикул


@router.message(GetArticle.article)
async def get_article(message: Message, state: FSMContext):
    await state.update_data(article=message.text) # Обновляем состояние машины
    data = RequestInfo(date_time=str(datetime.now())[:-4], # Записываем в переменную данные для добавления в БД
                       article=int(message.text),
                       telegram_id=int(message.from_user.id),)
    async with async_session() as session: # Открываем асинхронную сессию и добавляем в неё данные
        session.add(data)
        await session.commit() # После комита данные (о пользователе и запросе) отправляются в БД

    url = f'{GETITEM_URL}{message.text}' # Создаем запрос к API WB
    response_data = requests.get(url).json() # Преобразуем класс библиотеки requests к json

    name = response_data['data']['products'][0]['name'] # Собираем все данные из json в переменные с соответствующими именами
    article = message.text
    price = response_data['data']['products'][0]['salePriceU'] / 100
    raiting = response_data['data']['products'][0]['reviewRating']

    quantity = 0

    for i in range(len(response_data['data']['products'][0]['sizes'][0]['stocks'])): # Для получения количества товара на всех складах проходимся
        quantity += response_data['data']['products'][0]['sizes'][0]['stocks'][i]['qty'] # циклом по всем складам и записываем значения в переменную

    await message.answer(f'Название: {name}\n' # Формируем финальное сообщение для отправки пользователю
                         f'Артикул: {article}\n'
                         f'Цена: {price}\n'
                         f'Рейтинг: {raiting}\n'
                         f'Количество: {quantity}',
                         reply_markup=keyboards.subscribe,)

    await state.clear() # Очищаем машину состояния для дальнейшей работы


# Получаем информацию из БД
@router.message(F.text == 'Получить информацию из БД 📁')
async def cmd_get_db_data(message: Message):
    await message.answer(f'Последние 5 записей из базы данных:')
    async with async_session() as session:
        stmt = select(RequestInfo).order_by(RequestInfo.id.desc()).limit(5) # Выбираем из БД по столбцу id последние 5 записей при помощи команды desc()
        data = await session.execute(stmt)
        result = data.scalars().all() # Из моделей строк БД собираем финальные сообщения для отправки пользователю и
        for index, recording in enumerate(result): # отправляем их в цикле. enumerate служит только для удобной нумерации
            await message.answer(f'Запись №: {index + 1}\n\n'
                                 f'Дата и время: {recording.date_time}\n'
                                 f'Артикул: {recording.article}\n'
                                 f'user_id: {recording.telegram_id}\n')


# Создаём коллбэк для инлайн кнопки подписки
@router.callback_query(F.data == 'subscribe')
async def subscribe(callback: CallbackQuery, state: FSMContext):
    await callback.answer(f'Подписка оформлена ✅')
    index_ = callback.message.text.split().index('Артикул:') + 1 # Из сообщения над кнопкой вытаскиваем артикул чтобы
    article = callback.message.text.split()[index_] # не запрашивать его повторно и записываем в переменную

    await state.update_data({"parsing_continue": True}) # Устанавливаем значение для бесконечного цикла, которое будет изменяться
    while (await state.get_data()).get("parsing_continue"): # при нажатии на кнопку отписки

        url = f'{GETITEM_URL}{article}' # Снова парсим значения из API как и при получении по запросу артикула, только
        response_data = requests.get(url).json() # делаем это в бесконечном цикле каждые 300 секунд
        name = response_data['data']['products'][0]['name']
        article = article
        price = response_data['data']['products'][0]['salePriceU'] / 100
        raiting = response_data['data']['products'][0]['reviewRating']

        quantity = 0

        for i in range(len(response_data['data']['products'][0]['sizes'][0]['stocks'])):
            quantity += response_data['data']['products'][0]['sizes'][0]['stocks'][i]['qty']

        await callback.message.answer(f'Название: {name}\n'
                                      f'Артикул: {article}\n'
                                      f'Цена: {price}\n'
                                      f'Рейтинг: {raiting}\n'
                                      f'Количество: {quantity}',)

        await asyncio.sleep(300) # Время сна в секундах


# Останавливаем уведомления, меняя состояние parsing_continue на False
@router.message(F.text == 'Остановить уведомления 🚫')
async def cmd_stop_notification(message: Message, state: FSMContext):
    await message.answer(f'Уведомления остановлены ')
    await state.update_data({"parsing_continue": False}) # Меняем состояние. Цикл подписки прерывается
