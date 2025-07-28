from aiogram import F, Router, types

from .constants import CONNECT_WIFI


router = Router(name='Replies Router')

@router.message(F.text == CONNECT_WIFI)
async def send_wifi_data(msg: types.Message):

    file_path = 'resources\\wifi_qrcode.png'

    photo_file = types.FSInputFile(file_path)

    # Send the photo
    await msg.answer_photo(
        photo=photo_file,
        caption="Отсканируй данный QR-код или используй следующие данные:" \
        "SSID: Kirovs Wi-Fi" \
        "Пароль: v_kirov0318"
    )