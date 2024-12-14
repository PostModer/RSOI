import datetime
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import sqlite3
import os
import time

# Имя файла базы данных
DB_FILENAME = "log.db"

# Создание базы данных и таблицы для логов
def init_db():
    """Инициализация базы данных, создание таблицы при необходимости."""
    connection = sqlite3.connect(DB_FILENAME)
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time TEXT NOT NULL,
            event_type TEXT NOT NULL,
            execution_time REAL NOT NULL
        )
    """)
    connection.commit()
    connection.close()

    # Инициализация БД
init_db()


def log_event(event):
    """
    Записывает событие в базу данных.
    Ожидается словарь с ключами: time, event_type, execution_time.
    """
    try:
        connection = sqlite3.connect(DB_FILENAME)
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO events (time, event_type, execution_time)
            VALUES (?, ?, ?)
        """, (event["time"], event["event_type"], event["execution_time"]))
        connection.commit()
        connection.close()
        print("Событие записано в базу данных:", event)
        return True
    except Exception as e:
        print("Ошибка записи в базу данных:", e)
        return False


def get_logs():
    """
    Извлекает все записи из базы данных и возвращает их как список словарей.
    """
    try:
        connection = sqlite3.connect(DB_FILENAME)
        cursor = connection.cursor()
        cursor.execute("SELECT time, event_type, execution_time FROM events")
        rows = cursor.fetchall()
        connection.close()

        # Форматирование записей в список словарей
        logs = [{"time": row[0], "event_type": row[1], "execution_time": row[2]} for row in rows]
        return logs
    except Exception as e:
        print("Ошибка при чтении из базы данных:", e)
        return []

# Обработчик запросов
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

# Запуск сервера
server = SimpleXMLRPCServer(("localhost", 8010), requestHandler=RequestHandler, allow_none=True)

# Регистрация функций
server.register_function(log_event, "log_event")
server.register_function(get_logs, "get_logs")

print("Сервер статистики запущен на порту 8010...")
server.serve_forever()