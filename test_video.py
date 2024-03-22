import requests
import json

def load_news(file_path):
    # Открыть файл для чтения
    with open(file_path, 'r', encoding='utf-8') as file:
        # Прочитать строки из файла и сохранить их в список
        lines = [line.strip() for line in file.readlines()]
    return lines

#news_file = "news.txt"
news_file = "/Users/outsider/Source/Docker/airflow/data/news/masa_live_short/masa_live_short.240321154622.txt"
data = load_news(news_file)
conf = {
    "base_file": "./source/pieces_masa_live/",
    "audio_file": './source/sound/clock5sec/',
    "output_dir": "./out/",
    "logo_text": '\ 7news          |',
    "logo_font": "./fonts/azoft-sans/Azoft Sans-Bold.otf",
    "basic_font_color": 'white',
    "basic_font": "./fonts/inglobal/inglobal.ttf",
    "basic_font_size": 25,
    "max_str_length": 46,
    "max_text_length": 1300,
    "blur_strength": 0,
    "box_color": "#313131@0.8",
    "box_border": 200
}

# Замените URL на свой адрес сервера Flask
#url = 'http://172.17.0.2:5000/video'
url = 'http://127.0.0.1:5000/video'
#url = 'http://81.200.154.127:5000/video'

# Пример данных в формате JSON
data_to_send = {
    "sample": "short_news",
    "data": data,
    "config": conf
    }

# Отправляем POST-запрос с данными JSON
response = requests.post(url, json=data_to_send)

#escaped_string = '\u0414\u0430\u043d\u043d\u044b\u0435 \u0443\u0441\u043f\u0435\u0448\u043d\u043e \u043f\u043e\u043b\u0443\u0447\u0435\u043d\u044b'
decoded_string = bytes(response.text, 'utf-8').decode('unicode-escape')
print(decoded_string)
# Печать ответа от сервера
#print("Ответ сервера:", response.text)
