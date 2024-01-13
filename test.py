import requests
import json

# Замените URL на свой адрес сервера Flask
url = 'http://172.17.0.2:5000/video'
#url = 'http://81.200.154.127:5000/video'

# Пример данных в формате JSON
data_to_send = {
    "sample": "breaking_news",
    "data": [
        'Министерство государственной безопасности КНР объявило о задержании иностранного консультанта, который, по данным следствия, собирал секретные сведения для британской внешней разведки MI6, сообщает South China Morning Post. В ведомстве не указали гражданство, возраст и точное имя задержанного. По информации министерства, он действовал в интересах MI6 с 2015 года, и британская разведка тренировала!'
        ],
    }

# Отправляем POST-запрос с данными JSON
response = requests.post(url, json=data_to_send)

#escaped_string = '\u0414\u0430\u043d\u043d\u044b\u0435 \u0443\u0441\u043f\u0435\u0448\u043d\u043e \u043f\u043e\u043b\u0443\u0447\u0435\u043d\u044b'
decoded_string = bytes(response.text, 'utf-8').decode('unicode-escape')
print(decoded_string)
# Печать ответа от сервера
#print("Ответ сервера:", response.text)
