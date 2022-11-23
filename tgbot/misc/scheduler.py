""" Functions for sending scheduled weather data """

from os import remove

from aiogram import Dispatcher
from aiogram.types import InputFile, Message
from aiogram.utils.exceptions import BotBlocked, MessageToDeleteNotFound

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from tgbot.models.database import database, Users
from tgbot.services.weather_api import weather


async def update_weather_data(dp: Dispatcher) -> None:
    """ Updates weather data for all users """
    users: list[Users] = await database.get_all_users()
    for user in users:
        image_path: str = await weather.get_weather_forecast(user_id=user.id)
        try:
            reply: Message = await dp.bot.send_photo(chat_id=user.id, photo=InputFile(image_path),
                                                     caption=await weather.get_current_weather(user_id=user.id),
                                                     disable_notification=True)
            await dp.bot.delete_message(chat_id=user.id, message_id=user.dialog_message_id)
            await database.save_dialog_message_id(user_id=user.id, dialog_message_id=reply.message_id)
        except BotBlocked:
            await database.delete_user(user_id=user.id)
        except MessageToDeleteNotFound:
            pass
        remove(image_path)


async def schedule(dp) -> None:
    scheduler: AsyncIOScheduler = AsyncIOScheduler()
    scheduler.add_job(
        func=update_weather_data,
        trigger='cron',
        hour='0, 3, 6, 9, 12, 15, 18, 21',
        args=(dp,),
        timezone='UTC'
    )
    scheduler.start()