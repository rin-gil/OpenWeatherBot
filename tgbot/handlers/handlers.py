""" Handling messages from bot users """
from asyncio import sleep

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.exceptions import MessageToDeleteNotFound, MessageIdentifierNotSpecified

from tgbot.keyboards.inline import generate_cities_keyboard, generate_temperature_units_keyboard
from tgbot.misc.locale import get_dialog_message_answer
from tgbot.misc.states import TextInput
from tgbot.models.db import get_dialog_message_id, save_dialog_message_id, delete_user_from_db
from tgbot.services.weather_api import get_list_cities, get_weather


async def _del_old_dialog_message_and_send_new(message: Message, old_dialog_message_id: int, message_text: str) -> int:
    """
    Implement the dialog logic in a single message:
        Deletes the old dialog message and sends a new one. Returns the id of the new message.

    :param message: message from the user
    :param old_dialog_message_id: old message id
    :param message_text: the text to be sent to the user
    :return: old message id or new message id
    """
    try:
        await message.bot.delete_message(chat_id=message.from_user.id, message_id=old_dialog_message_id)
    except MessageToDeleteNotFound:
        pass
    except MessageIdentifierNotSpecified:
        pass
    new_dialog_message: Message = await message.answer(text=message_text)
    return new_dialog_message.message_id


async def dialog_command_start(message: Message, state: FSMContext) -> None:
    """
    Handles command /start from the user

    :param message: message from the user
    :param state: state from Final State Machine
    :return: None
    """
    await message.delete()
    await state.reset_state()
    async with state.proxy() as data:
        data['user_id']: int = message.from_user.id
        data['user_language']: str = message.from_user.language_code
        data['dialog_message_id']: int = await _del_old_dialog_message_and_send_new(
            message=message,
            old_dialog_message_id=await get_dialog_message_id(user_id=data['user_id']),
            message_text=await get_dialog_message_answer(user_language_code=data['user_language'],
                                                         dialog_message_name='dialog_command_start')
        )
    await TextInput.EnterCityName.set()  # Allow user input of text
    await save_dialog_message_id(user_id=data['user_id'], dialog_message_id=data['dialog_message_id'])


async def dialog_command_stop(message: Message, state: FSMContext) -> None:
    """
    Handles command /stop from the user

    :param message: message from the user
    :param state: state from Final State Machine
    :return: None
    """
    await message.delete()
    await state.reset_state()
    dialog_message_id: int = await _del_old_dialog_message_and_send_new(
        message=message,
        old_dialog_message_id=await get_dialog_message_id(user_id=message.from_user.id),
        message_text=await get_dialog_message_answer(user_language_code=message.from_user.language_code,
                                                     dialog_message_name='dialog_command_stop'))
    await delete_user_from_db(user_id=message.from_user.id)
    await sleep(5)
    await message.bot.delete_message(chat_id=message.from_user.id, message_id=dialog_message_id)


async def dialog_message_select_city(message: types.Message, state: FSMContext) -> None:
    """
    Processing the result of the search of the city entered by the user

    :param message: message from the user
    :param state: state from Final State Machine
    :return: None
    """
    await message.delete()
    await TextInput.previous()  # Deny user input (prevents repeated city search if OpenWeatherMap API service
    #                             takes a long time to process the request)
    async with state.proxy() as data:
        await message.bot.edit_message_text(
            text=await get_dialog_message_answer(user_language_code=data['user_language'],
                                                 dialog_message_name='dialog_message_select_city'),
            chat_id=data['user_id'],
            message_id=data['dialog_message_id']
        )
        cities_found: list = await get_list_cities(city_name=message.text)
        if len(cities_found) == 0:
            await message.bot.edit_message_text(
                text=await get_dialog_message_answer(user_language_code=data['user_language'],
                                                     dialog_message_name='dialog_message_select_city_error'),
                chat_id=data['user_id'],
                message_id=data['dialog_message_id']
            )
            await TextInput.EnterCityName.set()  # Allow user input of text
        else:
            await message.bot.edit_message_text(
                text=await get_dialog_message_answer(user_language_code=data['user_language'],
                                                     dialog_message_name='dialog_message_select_city_success'),
                chat_id=data['user_id'],
                message_id=data['dialog_message_id'],
                reply_markup=await generate_cities_keyboard(cities=cities_found,
                                                            user_language_code=data['user_language'])
            )


async def back_to_input_city_name(call: CallbackQuery) -> None:
    """
    Returns to the input of the city name

    :param call: CallbackQuery
    :return: None
    """
    await call.answer(cache_time=1)
    await call.bot.edit_message_text(
        text=await get_dialog_message_answer(user_language_code=call.from_user.language_code,
                                             dialog_message_name='dialog_command_start'),
        chat_id=call.message.chat.id,
        message_id=call.message.message_id
    )
    await TextInput.EnterCityName.set()  # Allow user input of text


async def dialog_choice_of_temperature_units(call: CallbackQuery, state: FSMContext) -> None:
    """
    Processes the coordinates of the selected user city and displays a dialog to select the temperature units

    :param call: CallbackQuery
    :param state: state from Final State Machine
    :return: None
    """
    await call.answer(cache_time=1)
    async with state.proxy() as data:
        coordinates: str = call.data.removeprefix('coordinates_of_the_city=')
        data['city_latitude']: str = coordinates.partition('&')[0]
        data['city_longitude']: str = coordinates.partition('&')[2]
        await call.bot.edit_message_text(
            text=await get_dialog_message_answer(user_language_code=call.from_user.language_code,
                                                 dialog_message_name='dialog_choice_of_temperature_units'),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=await generate_temperature_units_keyboard()
        )


async def dialog_save_weather_settings(call: CallbackQuery, state: FSMContext) -> None:
    """
    Saves the user's weather settings in the database

    :param call: CallbackQuery
    :param state: state from Final State Machine
    :return: None
    """
    await call.answer(text=await get_dialog_message_answer(user_language_code=call.from_user.language_code,
                                                           dialog_message_name='dialog_save_weather_settings'),
                      show_alert=True,
                      cache_time=1)
    async with state.proxy() as data:
        print(data)

        # TODO сделать сохранение пользователя в БД

        await call.bot.edit_message_text(text=await get_weather(),
                                         chat_id=call.message.chat.id,
                                         message_id=call.message.message_id)
        data.clear()


async def dialog_unprocessed(message: Message) -> None:
    """
    Deletes unprocessed messages or commands from the user

    :param message: message from the user
    :return: None
    """
    await message.delete()


def register_handlers(dp: Dispatcher) -> None:
    """
    Registers the handling of commands from the user in the Dispatcher.

    :param dp: Dispatcher
    :return: None
    """
    dp.register_message_handler(dialog_command_start, commands='start', state='*')
    dp.register_message_handler(dialog_command_stop, commands='stop', state='*')
    dp.register_message_handler(dialog_message_select_city, state=TextInput.EnterCityName)
    dp.register_callback_query_handler(back_to_input_city_name, text='input_another_city')
    dp.register_callback_query_handler(dialog_choice_of_temperature_units, text_contains='coordinates_of_the_city=')
    dp.register_callback_query_handler(dialog_save_weather_settings, text_contains='temperature_units=')
    dp.register_message_handler(dialog_unprocessed, state='*', content_types=types.ContentTypes.ANY)
