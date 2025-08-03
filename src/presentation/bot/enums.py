from enum import StrEnum


class MainKeyboardButton(StrEnum):
    CONNECT_WIFI = "Подключение к Wi-Fi 🛜"
    ENTER_CLOUD = "Войти в облако ☁️"
    GET_WEATHER = "Узнать текущую погоду 🌤️"
    

class EnterCloudKeyboardButton(StrEnum):
    NEXTCLOUD = 'Kirovs Nextcloud'


class WriteAdminButton(StrEnum):
    WRITE_ADMIN = 'Написать администратору'


class Caption(StrEnum):
    START_MSG = "Добро пожаловать! Это бот-помощник нашей семьи." \
                "С моей помощью вы можете узнать любую полезную информацию о паролях, сервисах и т.п." \
                "Используйте /login, чтобы подтвердить личность и получить доступ к функционалу."
    
    CONNECT_WIFI = "Отсканируй данный QR-код или используй следующие данные: \n\n" \
        "<b>SSID:</b> <code>Kirovs Wi-Fi</code>\n" \
        "<b>Пароль:</b> <code>v_kirov0318</code>"
    
    SUCCESS_AUTH = "Аутентификация успешна. Вам доступны команды бота."

    SUPPORT_INFO = "Вы авторизованы. По всем вопросам писать админу."

    SUCCESS_LOGOUT = "Вы сделали логаут. Для дальнейшего использования нужно снова авторизоваться через /login."

    UNUQUE_ERROR = "Такие учетные данные уже используются. \nПожалуйста, используйте /login с другими данными."

    
class ResourcePath(StrEnum):
    WIFI_QR_CODE = "resources/qr_wifi.png"
    CLOUD = 'https://nextcloud.kirovs.online'
    ADMIN_TG = "t.me/evan_kirk"


class HeadsOrTails(StrEnum):
    HEAD='Орёл'
    TAIL='Решка'
