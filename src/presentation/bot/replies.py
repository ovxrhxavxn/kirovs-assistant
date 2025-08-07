from aiogram import F, Router, types
from aiogram.enums import ParseMode

from .enums import MainKeyboardButton, ResourcePath, Caption
from .keyboards import get_inline_cloud_keyboard
from ...business_logic.services import WeatherService
from ...data_access.shemas import WeatherDayHour, DailyForecast


router = Router(name='Replies Router')


def _get_weather_emoji(hour: WeatherDayHour) -> str:
    """A simple helper to select an emoji based on weather conditions."""
    if hour.chance_of_snow > 40:
        return "❄️"
    if hour.chance_of_rain > 40:
        return "🌧️"
    if hour.cloud > 75:
        return "☁️"
    if hour.cloud > 50:
        return "🌥️"
    if hour.cloud > 25:
        return "🌤️"
    return "☀️"


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
    await message.answer("Нажмите ниже, чтобы войти в облако:", reply_markup=get_inline_cloud_keyboard())


@router.message(F.text == MainKeyboardButton.GET_WEATHER)
async def send_weather_info(
    message: types.Message,
    weather_service: WeatherService):

    city = "Карабаш" # Hardcoding for now as it's the default in the service

    # New way: we expect a list of DailyForecast objects
    forecast_list: list[DailyForecast] = await weather_service.get_forecast_upon(days=7)

    # --- THIS IS THE MAIN FIX ---

    # 1. Safely check if the list is empty (API call failed)
    if not forecast_list:
        await message.answer("Не удалось получить прогноз погоды. Попробуйте позже.")
        return

    # 2. Get the first day's forecast from the list.
    #    Since we request 1 day, it will be the only item.
    today_forecast = forecast_list[0]

    # 3. Access the data through the new, clean attributes.
    day_summary = today_forecast.day_summary
    hourly_forecast = today_forecast.hourly_forecast

    summary_parts = [
        f"<b>Погода в г. {city} на сегодня:</b>\n",
        f"🌡️ Температура: <b>{day_summary.maxtemp_c}°C</b> / <b>{day_summary.mintemp_c}°C</b> (макс/мин)",
        f"💨 Ветер: до <b>{day_summary.maxwind_kph} км/ч</b>",
        f"💧 Вероятность дождя: <b>{day_summary.daily_chance_of_rain}%</b>",
        f"❄️ Вероятность снега: <b>{day_summary.daily_chance_of_snow}%</b>"
    ]

    # The rest of the logic is almost identical, just using the new variable names
    text_parts = ["\n".join(summary_parts)]
    text_parts.append("\n<b>Прогноз по часам:</b>")

    interesting_hours = [8, 12, 16, 20]

    for hour_data in hourly_forecast:
        if hour_data.time.hour in interesting_hours:
            emoji = _get_weather_emoji(hour_data)

            line = (
                f"  - <b>{hour_data.time.strftime('%H:%M')}</b>: {emoji} {hour_data.temp_c}°C "
                f"(ощущается как {hour_data.feelslike_c}°C)"
            )
            text_parts.append(line)

    final_text = "\n".join(text_parts)

    await message.answer(final_text, parse_mode=ParseMode.HTML)