import xmlrpc.client


# Подключение к серверу статистики
# server = xmlrpc.client.ServerProxy("http://localhost:8008", allow_none=True)
stats_server = xmlrpc.client.ServerProxy("http://localhost:8010", allow_none=True)
proxy_server = xmlrpc.client.ServerProxy("http://localhost:8009", allow_none=True)

# Функции сервера
print ('Ping:', proxy_server.call_method('ping'))
print ('Server datetime:', proxy_server.call_method('now'))
print ('View, type, value:', proxy_server.call_method('type', 2))
print ('View, type, value:', proxy_server.call_method('type', 2.))
# # print ('View, type, value:', proxy_server.call_method('My string'))
# # print ('View, type, value:', server.type([1,2,3]))
# # print ('View, type, value:', server.type(["one", "two", "three"]))
# # print ('View, type, value:', server.type((1,2,"3")))
print ('Sum 2 + 3 :', proxy_server.call_method('sum', 2, 3))
print ('Pow 2^3: ', proxy_server.call_method('pow', 2, 3))



# Получение логов
# logs = stats_server.get_logs()
# #
# # # Вывод логов в терминал
# print("=== Логи событий из базы данных ===")
# for log in logs:
#     print(
#         f"Время: {log['time']}, Тип события: {log['event_type']}, Время выполнения: {log['execution_time']:.4f} сек")
