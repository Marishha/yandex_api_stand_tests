# Импорт необходимых модулей и данных для запроса
import requests
import configuration
import data

def post_new_user(user_body):
    """
    Функция для отправки POST-запроса на создание нового пользователя
    """
    # Отправка POST-запроса на создание пользователя
    return requests.post(configuration.URL_SERVICE + configuration.CREATE_USER_PATH,
                         json=user_body,  # Тело запроса содержит данные пользователя
                         headers=data.headers)  # Заголовки запроса

# Определение функции для отправки POST-запроса на поиск наборов по продуктам
def post_products_kits(products_ids):
    # Отправка POST-запроса с использованием URL из конфигурации, данных о продуктах и заголовков
    # Возвращается объект ответа, полученный от сервера
    return requests.post(configuration.URL_SERVICE + configuration.PRODUCTS_KITS_PATH,
                         json=products_ids)  # Тело запроса содержит ID продуктов в формате JSON