import requests

# URL сервера
base_url = "http://localhost:8000"


# 1. Создание короткой ссылки
def create_short_url(original_url):
    # Отправляем POST-запрос для сокращения ссылки
    response = requests.post(f"{base_url}/shorten", data={"original_url": original_url})
    if response.status_code == 200:
        print("Короткая ссылка создана:", response.text)
    else:
        print("Ошибка при создании короткой ссылки:", response.text)


# 2. Переход по короткой ссылке
def visit_short_url(short_code):
    # Отправляем GET-запрос по короткой ссылке
    response = requests.get(f"{base_url}/{short_code}", allow_redirects=False)
    if response.status_code == 302:
        print("Перенаправлено на оригинальный URL:", response.headers["Location"])
    else:
        print("Неизвестный ответ от сервера.")

# Пример выполнения запросов
if __name__ == "__main__":
    # Оригинальный URL для сокращения
    original_url = "https://yandex.ru"
    # Создаем короткую ссылку
    create_short_url(original_url)
