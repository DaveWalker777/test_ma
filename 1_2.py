import random
import string
import uvicorn
import json
from urllib.parse import parse_qs
from time import time

# Инициализация файлов и переменных
URL_STORE_FILE = "url_store.json"  # Файл для хранения ссылок
url_store = {}  # Словарь, хранящий короткие и оригинальные ссылки
request_counts = {}  # Словарь для учета количества запросов от каждого IP
REQUEST_LIMIT = 10  # Максимум 10 запросов в минуту от одного IP
BLOCK_TIME = 60     # Время ограничения (в секундах)

# Функция генерации уникального кода
def generate_short_code(length=6):
    # Генерируем короткий код из случайных букв и цифр
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Функция для загрузки ссылок из файла
def load_url_store():
    global url_store
    try:
        with open(URL_STORE_FILE, "r") as f:
            url_store = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        url_store = {}

# Функция для сохранения ссылок в файл
def save_url_store():
    with open(URL_STORE_FILE, "w") as f:
        json.dump(url_store, f)

# Функция проверки лимитов запросов от одного IP
def is_request_allowed(client_ip):
    current_time = time()
    # Получаем запросы от текущего IP
    request_log = request_counts.get(client_ip, [])
    # Удаляем запросы, которые старше BLOCK_TIME секунд
    request_log = [req_time for req_time in request_log if current_time - req_time < BLOCK_TIME]
    if len(request_log) >= REQUEST_LIMIT:
        return False
    # Запоминаем новый запрос
    request_log.append(current_time)
    request_counts[client_ip] = request_log
    return True

# Основное ASGI-приложение для обработки запросов
async def app(scope, receive, send):
    if scope["type"] == "http":
        path = scope["path"]
        method = scope["method"]
        client_ip = scope["client"][0]

        # Проверка лимита запросов
        if not is_request_allowed(client_ip):
            await send({
                "type": "http.response.start",
                "status": 429,
                "headers": [(b"content-type", b"text/plain")],
            })
            await send({"type": "http.response.body", "body": b"Error: Too many requests. Please try again later."})
            return

        if method == "POST" and path == "/shorten":
            body = await receive()
            query_data = parse_qs(body['body'].decode())
            original_url = query_data.get("original_url", [None])[0]

            if original_url:
                # Генерация уникального короткого кода
                short_code = generate_short_code()
                while short_code in url_store:
                    short_code = generate_short_code()
                # Сохраняем код и оригинальный URL
                url_store[short_code] = original_url
                save_url_store()  # Обновляем файл

                response_body = f"Shortened URL: http://localhost:8000/{short_code}"
                await send({
                    "type": "http.response.start",
                    "status": 200,
                    "headers": [(b"content-type", b"text/plain")],
                })
                await send({"type": "http.response.body", "body": response_body.encode()})
            else:
                await send({
                    "type": "http.response.start",
                    "status": 400,
                    "headers": [(b"content-type", b"text/plain")],
                })
                await send({"type": "http.response.body", "body": b"Error: 'original_url' parameter is required."})

        elif method == "GET":
            # Переход по короткому коду
            short_code = path.lstrip("/")
            if short_code in url_store:
                original_url = url_store[short_code]
                await send({
                    "type": "http.response.start",
                    "status": 302,
                    "headers": [(b"location", original_url.encode())],
                })
                await send({"type": "http.response.body", "body": b""})
            else:
                await send({
                    "type": "http.response.start",
                    "status": 404,
                    "headers": [(b"content-type", b"text/plain")],
                })
                await send({"type": "http.response.body", "body": b"Error: URL not found."})

# Загрузка данных при запуске сервера
if __name__ == "__main__":
    load_url_store()
    uvicorn.run(app, host="127.0.0.1", port=8000)
