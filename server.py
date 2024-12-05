from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import xmlrpc.client
import datetime

# Подключение к серверу статистики
try:
    stats_server = xmlrpc.client.ServerProxy("http://localhost:8009")
    stats_enabled = True
except ConnectionRefusedError:
    print("Statistics server is not available.")
    stats_enabled = False

# Функция для отправки события на сервер статистики
def log_event(event_type):
    if stats_enabled:
        try:
            stats_server.log_event(event_type)
        except Exception as e:
            print(f"Failed to log event: {e}. Continuing without statistics.")
            pass

# Создание основного сервера
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

server = SimpleXMLRPCServer(("localhost", 8008), allow_none=True,
                            requestHandler=RequestHandler)

# Тест
def ping():
    log_event('ping')
    return True
server.register_function(ping, 'ping')

# Время сервера
def now():
    log_event('now')
    return datetime.datetime.now()
server.register_function(now, 'now')

# Отображение строкового вида, типа и значений
def show_type(arg):
    log_event('type')
    return (str(arg), str(type(arg)), arg)
server.register_function(show_type, 'type')

# Сумма
def test_sum(a, b):
    log_event('sum')
    return a + b
server.register_function(test_sum, 'sum')

# Степень
def test_pow(a, b):
    log_event('pow')
    return a**b
server.register_function(test_pow, 'pow')


print("Listening on port 8008...")
server.serve_forever()