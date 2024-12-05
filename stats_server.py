import glob
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import csv
import os
import datetime
import pandas as pd

# Максимальное количество записей в журнале
MAX_RECORDS = 50
LOG_FILENAME = 'event_log.csv'

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

# Создание сервера
server = SimpleXMLRPCServer(("localhost", 8009), allow_none=True, requestHandler=RequestHandler)

# Функция для проверки и ротации журнала
def rotate_log_file():
    if os.path.exists(LOG_FILENAME):
        with open(LOG_FILENAME) as file:
            record_count = sum(1 for line in file)
            # Проверка количества записей
            if record_count >= MAX_RECORDS:
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                new_log_filename = f'event_log_{timestamp}.csv'
                os.rename(LOG_FILENAME, new_log_filename)

# Функция для добавления записи в журнал
def log_event(event_type):
    rotate_log_file()
    event_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILENAME, mode='a', newline='') as file:
        writer = csv.writer(file)
        if os.path.getsize(LOG_FILENAME) == 0:
            writer.writerow(['Time', 'Event Type'])  # Заголовки
        writer.writerow([event_time, event_type])
    return True

# Функция для получения содержимого журнала
# def get_log_content():
#     if not os.path.isfile(LOG_FILENAME):
#         return []
#     df = pd.read_csv(LOG_FILENAME)
#     return df.to_dict(orient='records')

def filter_log(event_type=None, start_time=None, end_time=None):
    # if not os.path.isfile(LOG_FILENAME):
    #     return []

    filtered_records = []
    log_files = find_csv_files_recursive()
    # Чтение CSV-файла и фильтрация записей
    for log_file in log_files:
        # print(log_file)
        with open(log_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                record_time = row['Time']
                record_event = row['Event Type']

                # Применение фильтров
                if event_type is not None and record_event != event_type:
                    continue
                if start_time is not None and record_time < start_time:
                    continue
                if end_time is not None and record_time > end_time:
                    continue

                # Добавление записи в результат
                filtered_records.append({
                    'Time': row['Time'],
                    'Event Type': record_event
                })

    return filtered_records

def find_csv_files_recursive(directory="."):
    """Поиск всех файлов с расширением .csv, включая вложенные директории."""
    csv_files = []
    for root, dirs, files in os.walk(directory):  # Обходим папки и файлы
        for file in files:
            if file.endswith(".csv"):  # Проверяем расширение
                csv_files.append(file)  # Добавляем полный путь
    return csv_files

def filter_log_rpc(*args):
    # Обработка входных аргументов
    event_type = args[0] if len(args) > 0 and args[0] else None
    start_time = args[1] if len(args) > 1 and args[1] else None
    end_time = args[2] if len(args) > 2 and args[2] else None

    # Передача аргументов в основную функцию
    return filter_log(
        event_type=event_type,
        start_time=start_time,
        end_time=end_time
    )

# Регистрация функции логирования
server.register_function(log_event, 'log_event')
server.register_function(find_csv_files_recursive, 'find_csv_files_recursive')
# server.register_function(filter_log, 'filter_log')
# server.register_function(get_log_content, 'get_log_content')
server.register_function(filter_log_rpc, 'filter_log')

print("Statistics server listening on port 8009...")
server.serve_forever()