from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import xmlrpc.client
import datetime

# Подключение к серверу статистики
# proxy_server = xmlrpc.client.ServerProxy("http://localhost:8009")
stats_server = xmlrpc.client.ServerProxy("http://localhost:8010")
# Создание основного сервера
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

server = SimpleXMLRPCServer(("localhost", 8008), allow_none=True,
                            requestHandler=RequestHandler)

# Тест
def ping():
    # stats_server.log_event('ping')
    # proxy_server.call_method('ping')
    return True
server.register_function(ping, 'ping')

# Время сервера
def now():
    # stats_server.log_event('now')
    # proxy_server.call_method('now')
    return datetime.datetime.now()
server.register_function(now, 'now')

# Отображение строкового вида, типа и значений
def show_type(arg):
    # stats_server.log_event('type')
    # proxy_server.call_method('type')
    return (str(arg), str(type(arg)), arg)
server.register_function(show_type, 'type')

# Сумма
def test_sum(a, b):
    # stats_server.log_event('sum')
    # proxy_server.call_method('sum')
    return a + b
server.register_function(test_sum, 'sum')

# Степень
def test_pow(a, b):
    # stats_server.log_event('pow')
    # proxy_server.call_method('pow')
    return a**b
server.register_function(test_pow, 'pow')


print("Listening on port 8008...")
server.serve_forever()