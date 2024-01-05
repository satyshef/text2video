import sys
import os
import importlib
from flask import Flask, request, jsonify, send_file

host = '0.0.0.0'
#host = '172.17.0.2'
port = '5000'
media_directory = 'out/'
app = Flask(__name__)

@app.route('/')
def ok():
    print(request.host)
    sys.stdout.flush()
    return 'OK'

@app.route('/video', methods=['POST'])
def create_video():
    try:
        # Получаем данные JSON из запроса
        news = request.json
        library_name = 'sample.' + news['sample']
        sample = importlib.import_module(library_name)
        file_path, e = sample.run(news)
        #print("Полученные данные:", data['sample'])
        #sys.stdout.write("Полученные данные: {}\n".format(json_data))
        sys.stdout.flush()  # Принудительно сбрасываем буфер вывода
        # Возвращаем ответ в формате JSON
        if e == None:
            # генерируем url для видеофайла
            video_url =request.base_url + "/" + os.path.basename(file_path)
            return jsonify({"success": True, "message": "Video created", "url":video_url})
        else:
            return jsonify({"success": False, "error": e})    
    except Exception as e:
        print(e)
        return jsonify({"success": False, "error": str(e)})


@app.route('/video/<file_id>', methods=['GET'])
def get_video(file_id):
    try:
        # Формируем путь к медиафайлу на основе file_id
        media_file_path = f'{media_directory}{file_id}'

        # Возвращаем медиафайл в ответе
        return send_file(media_file_path, as_attachment=True)
    except Exception as e:
        return f"Ошибка: {str(e)}"
    

if __name__ == '__main__':
    app.run(debug=False, host=host, port=port)
    

