from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import xmlrpc.client
import datetime
import time

MAIN_SERVER_URL = "http://localhost:8008"
STAT_SERVER_URL = "http://localhost:8010"
ALLOW_NONE = True

# Подключение к основному серверу
main_server = xmlrpc.client.ServerProxy(MAIN_SERVER_URL, allow_none=ALLOW_NONE)
stats_server = xmlrpc.client.ServerProxy(STAT_SERVER_URL, allow_none=ALLOW_NONE)


def call_method(method_name, *args):

    # Вызов метода на основном сервере
    try:
        start_time = time.time()
        method = getattr(main_server, method_name)  # Получение метода по имени
        result = method(*args)  # Вызов метода
        exec_time = time.time() - start_time
        event = {
            "time": time.strftime("%d-%m-%Y %H:%M:%S", time.localtime(start_time)),
            "event_type": method_name,
            "execution_time": exec_time
        }
        #Попытка отправки данных на сервер статистики
        try:
            stats_server.log_event(event)
        except Exception as e:
            print('Сервер статистики недоступен: ', e)
        return result
    except Exception as e:
        return f"Ошибка при вызове метода '{method_name}': {e}"


# Создание сервера
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

server = SimpleXMLRPCServer(("localhost", 8009), requestHandler=RequestHandler, allow_none=ALLOW_NONE)

# Регистрация методов для прокси
server.register_function(call_method, "call_method")

print("Proxy server listening on port 8009...")
server.serve_forever()