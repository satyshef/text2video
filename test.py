import requests
import json

# Замените URL на свой адрес сервера Flask
url = 'http://172.17.0.2:5000/video'
#url = 'http://81.200.154.127:5000/video'

# Пример данных в формате JSON
data_to_send = {
    "sample": "masa_live",
    "data": [
        'Hello "elastic"'
        ],
    }

# Отправляем POST-запрос с данными JSON
response = requests.post(url, json=data_to_send)

#escaped_string = '\u0414\u0430\u043d\u043d\u044b\u0435 \u0443\u0441\u043f\u0435\u0448\u043d\u043e \u043f\u043e\u043b\u0443\u0447\u0435\u043d\u044b'
decoded_string = bytes(response.text, 'utf-8').decode('unicode-escape')
print(decoded_string)
# Печать ответа от сервера
#print("Ответ сервера:", response.text)
