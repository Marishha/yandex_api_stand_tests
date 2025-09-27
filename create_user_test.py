# Импортируем модуль sender_stand_request, содержащий функции для отправки HTTP-запросов к API.
import sender_stand_request
import data

# Цвета для красивого вывода (работает в большинстве терминалов)
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

# эта функция меняет значения в параметре firstName
def get_user_body(first_name):
    current_body = data.user_body.copy()
    current_body["firstName"] = first_name
    return current_body

def print_test_header(test_number, description):
    """Печатает заголовок теста"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}┌{'─' * 70}┐{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}│ ТЕСТ {test_number:2d}: {description:<55} │{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}└{'─' * 70}┘{Colors.END}")

def print_success(message):
    """Печатает успешное сообщение"""
    print(f"{Colors.GREEN}✅ {message}{Colors.END}")

def print_error(message):
    """Печатает сообщение об ошибке"""
    print(f"{Colors.RED}❌ {message}{Colors.END}")

def print_info(message):
    """Печатает информационное сообщение"""
    print(f"{Colors.BLUE}ℹ️  {message}{Colors.END}")

def print_warning(message):
    """Печатает предупреждение"""
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.END}")

# Функция для позитивных проверок
def positive_assert(first_name, test_number):
    print_test_header(test_number, f"Успешное создание: '{first_name}'")
    print_info(f"Тело запроса: {get_user_body(first_name)}")
    
    user_response = sender_stand_request.post_new_user(get_user_body(first_name))
    
    print_info(f"Статус код: {user_response.status_code}")
    print_info(f"Ответ: {user_response.text}")
    
    if user_response.status_code == 201:
        print_success(f"Пользователь создан! AuthToken: ...{user_response.json()['authToken'][-8:]}")
        return True
    else:
        print_error(f"Ожидался статус 201, получен {user_response.status_code}")
        return False

# Функция для негативных проверок (неправильные символы)
def negative_assert_symbol(first_name, test_number):
    print_test_header(test_number, f"Ожидаема ошибка: '{first_name}'")
    print_info(f"Тело запроса: {get_user_body(first_name)}")
    
    response = sender_stand_request.post_new_user(get_user_body(first_name))
    
    print_info(f"Статус код: {response.status_code}")
    
    if response.status_code == 400:
        print_success(f"Ошибка обработана корректно: {response.json().get('message', 'Нет сообщения об ошибке')}")
        return True
    else:
        print_error(f"Ожидался статус 400, получен {response.status_code}")
        return False

# Функция для негативных проверок (отсутствует firstName)
def negative_assert_no_firstname(user_body, test_number):
    print_test_header(test_number, "Ошибка: отсутствует firstName")
    print_info(f"Тело запроса: {user_body}")
    
    response = sender_stand_request.post_new_user(user_body)
    
    print_info(f"Статус код: {response.status_code}")
    
    if response.status_code == 400:
        print_success("Ошибка обработана корректно")
        return True
    else:
        print_error(f"Ожидался статус 400, получен {response.status_code}")
        return False

# Тесты
def test_create_user_2_letter_in_first_name_get_success_response():
    return positive_assert("Аа", 1)

def test_create_user_15_letter_in_first_name_get_success_response():
    return positive_assert("Ааааааааааааааа", 2)

def test_create_user_1_letter_in_first_name_get_error_response():
    return negative_assert_symbol("A", 3)

def test_create_user_16_letter_in_first_name_get_error_response():
    return negative_assert_symbol("Аааааааааааааааa", 4)

def test_create_user_english_letter_in_first_name_get_success_response():
    return positive_assert("QWErty", 5)

def test_create_user_russian_letter_in_first_name_get_success_response():
    return positive_assert("Мария", 6)

def test_create_user_has_space_in_first_name_get_error_response():
    # ТЕСТ 7: ДОЛЖЕН ЗАВЕРШИТЬСЯ ОШИБКОЙ
    return negative_assert_symbol("Человек и КО", 7)

def test_create_user_has_special_symbol_in_first_name_get_error_response():
    return negative_assert_symbol("\"№%@\",", 8)

def test_create_user_has_number_in_first_name_get_error_response():
    return negative_assert_symbol("123", 9)

def test_create_user_no_first_name_get_error_response():
    user_body = data.user_body.copy()
    user_body.pop("firstName")
    return negative_assert_no_firstname(user_body, 10)

def test_create_user_empty_first_name_get_error_response():
    user_body = get_user_body("")
    return negative_assert_no_firstname(user_body, 11)

def test_create_user_number_type_first_name_get_error_response():
    # ТЕСТ 12: ДОЛЖЕН ЗАВЕРШИТЬСЯ ОШИБКОЙ
    print_test_header(12, "Ошибка: число вместо строки")
    print_info("Тело запроса с числом вместо firstName")
    
    user_body = data.user_body.copy()
    user_body["firstName"] = 12
    
    response = sender_stand_request.post_new_user(user_body)
    print_info(f"Статус код: {response.status_code}")
    
    if response.status_code == 400:
        print_success("Ошибка типа данных обработана корректно")
        return True
    else:
        print_error(f"Ожидался статус 400, получен {response.status_code}")
        return False

# Запуск всех тестов
if __name__ == "__main__":
    print(f"\n{Colors.BOLD}{Colors.PURPLE}🚀 ЗАПУСК ТЕСТОВ СОЗДАНИЯ ПОЛЬЗОВАТЕЛЯ{Colors.END}")
    print(f"{Colors.CYAN}{'=' * 72}{Colors.END}")
    
    # Список всех тестовых функций
    test_functions = [
        test_create_user_2_letter_in_first_name_get_success_response,
        test_create_user_15_letter_in_first_name_get_success_response,
        test_create_user_1_letter_in_first_name_get_error_response,
        test_create_user_16_letter_in_first_name_get_error_response,
        test_create_user_english_letter_in_first_name_get_success_response,
        test_create_user_russian_letter_in_first_name_get_success_response,
        test_create_user_has_space_in_first_name_get_error_response,
        test_create_user_has_special_symbol_in_first_name_get_error_response,
        test_create_user_has_number_in_first_name_get_error_response,
        test_create_user_no_first_name_get_error_response,
        test_create_user_empty_first_name_get_error_response,
        test_create_user_number_type_first_name_get_error_response
    ]
    
    passed_tests = 0
    failed_tests = 0
    
    # Запускаем тесты по порядку
    for i, test_func in enumerate(test_functions, 1):
        try:
            if test_func():
                passed_tests += 1
            else:
                failed_tests += 1
        except Exception as e:
            print_error(f"Тест завершился исключением: {e}")
            failed_tests += 1
    
    # Итоги
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'=' * 72}{Colors.END}")
    print(f"{Colors.BOLD}📊 ИТОГИ ТЕСТИРОВАНИЯ:{Colors.END}")
    print(f"{Colors.GREEN}✅ Пройдено тестов: {passed_tests}{Colors.END}")
    print(f"{Colors.RED}❌ Провалено тестов: {failed_tests}{Colors.END}")
    print(f"{Colors.BLUE}📈 Общее количество: {passed_tests + failed_tests}{Colors.END}")
    
    # Ожидаем, что тесты 7 и 12 должны провалиться
    expected_failures = 2  # тесты 7 и 12
    
    if failed_tests == expected_failures:
        print(f"\n{Colors.BOLD}{Colors.GREEN}🎉 ТЕСТИРОВАНИЕ ЗАВЕРШЕНО УСПЕШНО!{Colors.END}")
        print(f"{Colors.GREEN}Ожидаемые провалы (тесты 7 и 12) подтверждены{Colors.END}")
    else:
        print(f"\n{Colors.BOLD}{Colors.YELLOW}⚠️  РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ{Colors.END}")
        print(f"{Colors.YELLOW}Ожидалось проваленных тестов: {expected_failures}{Colors.END}")
        print(f"{Colors.YELLOW}Фактически проваленных: {failed_tests}{Colors.END}")