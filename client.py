# xmlrpc_client.ipynb

import xmlrpc.client

server = xmlrpc.client.ServerProxy("http://localhost:8008", allow_none=True)
stats_server = xmlrpc.client.ServerProxy("http://localhost:8009", allow_none=True)

#print(server.system.listMethods())

# print ('Ping:', server.ping())
# print ('Server datetime:', server.now())
# print ('View, type, value:', server.type(2))
# print ('View, type, value:', server.type(2.))
# print ('View, type, value:', server.type('My string'))
# print ('View, type, value:', server.type("My string"))
# print ('View, type, value:', server.type([1,2,3]))
# print ('View, type, value:', server.type(["one", "two", "three"]))
# print ('View, type, value:', server.type((1,2,"3")))
# print ('Sum 2 + 3 :', server.sum(2, 3))
# print ('Pow 2^3: ', server.pow(2, 3))

print("\n --- Все Лог файлы ---\n")
print(stats_server.find_csv_files_recursive())
# print("\n--- Filtered Log: Event Type 'sum' ---")
# print(stats_server.filter_log('sum'))

print("\n--- Filtered Log: Time Range ---")
start_time = '2024-11-29 21:52:04'
end_time = '2024-11-29 21:52:04'
print(stats_server.filter_log(None, '2024-12-02 16:57:21', '2024-12-02 16:58:25'))