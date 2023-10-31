import vk_api
from functools import cache

from gpt_vk_api_example.secrets import APP_ID, PHONE, PWD


def captcha_handler(captcha):
    """ При возникновении капчи вызывается эта функция и ей передается объект
        капчи. Через метод get_url можно получить ссылку на изображение.
        Через метод try_again можно попытаться отправить запрос с кодом капчи
    """

    key = input("Enter captcha code {0}: ".format(captcha.get_url())).strip()

    # Пробуем снова отправить запрос с капчей
    return captcha.try_again(key)


def auth_handler():
    """ При двухфакторной аутентификации вызывается эта функция.
    """

    # Код двухфакторной аутентификации
    key = input("Enter authentication code: ")
    # Если: True - сохранить, False - не сохранять.
    remember_device = True

    return key, remember_device


@cache
def get_vk_session() -> vk_api.VkApi:
    # Авторизация в Вконтакте
    vk_session = vk_api.VkApi(
        PHONE,
        PWD,
        captcha_handler=captcha_handler,
        auth_handler=auth_handler,
        app_id=APP_ID
    )
    vk_session.auth()
    # Создание экземпляра API
    return vk_session.get_api()
