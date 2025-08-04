from aiogram import F, Router, types
from aiogram.enums import ParseMode

from .enums import MainKeyboardButton, ResourcePath, Caption
from .keyboards import get_inline_cloud_keybord
from ...business_logic.services import WeatherService


router = Router(name='Replies Router')


@router.message(F.text == MainKeyboardButton.CONNECT_WIFI)
async def send_wifi_data(message: types.Message):

    photo_file = types.FSInputFile(ResourcePath.WIFI_QR_CODE)
    # Send the photo
    await message.answer_photo(
        photo=photo_file,
        caption=Caption.CONNECT_WIFI,
        parse_mode=ParseMode.HTML
    )


@router.message(F.text == MainKeyboardButton.ENTER_CLOUD)
async def send_cloud_link(message: types.Message):
    await message.answer("Нажмите ниже, чтобы войти в облако:", reply_markup=get_inline_cloud_keybord())


@router.message(F.text == MainKeyboardButton.GET_WEATHER)
async def send_weather_info(
    message: types.Message,
    weather_service: WeatherService):
    weather = await weather_service.get_current()

    text = f"Текущая погода днем: \n \
             \nТемпература 🌡️ {weather.temp_c}°C, ощущается, как {weather.feelslike_c}°C. \
             \n\nСкорость ветра 💨 {weather.wind_kph} км/ч." if weather.is_day else f"Текущая погода ночью: \n \
             \nТемпература 🌡️ {weather.temp_c}°C, ощущается, как {weather.feelslike_c}°C. \
             \n\nСкорость ветра 💨 {weather.wind_kph} км/ч."

    await message.answer(text)