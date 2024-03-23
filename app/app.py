import sys
import os
import importlib
from flask import Flask, request, jsonify, send_file

host = '0.0.0.0'
#host = '172.17.0.2'
port = '5000'
media_directory = './out/'
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
        if 'data' not in news or 'sample' not in news:
                return jsonify({"success": False, "error": "Empty parametrs"})
        
        if isinstance(news.get('sample'), str):
            sample_name = news['sample']
        else:
            if 'name' not in news['sample']:
                return jsonify({"success": False, "error": "Sample name in config not set"})     
            sample_name = news['sample']['name']

       
        library_name = 'sample.' + sample_name

        sample = importlib.import_module(library_name)
        file_path, e = sample.run(news)
        #print("Полученные данные:", data['sample'])
        #sys.stdout.write("Полученные данные: {}\n".format(json_data))
        sys.stdout.flush()  # Принудительно сбрасываем буфер вывода
        # Возвращаем ответ в формате JSON
        if e == None:
            # генерируем url для видеофайла
            #video_url =request.base_url + "/" + os.path.basename(file_path)
            # Может работать не корректно если формат записи media_directory отличается от записи в sample(./out/ out/)
            video_url =request.base_url + "/" + file_path.replace(media_directory, '')
            return jsonify({"success": True, "message": "Video created", "url":video_url})
        else:
            return jsonify({"success": False, "error": e})    
    except Exception as e:
        print(e)
        return jsonify({"success": False, "error": str(e)})


@app.route('/video/<path:video_path>', methods=['GET'])
def get_video(video_path):
    
    try:
        # Формируем путь к медиафайлу на основе file_id
        media_file_path = f'{media_directory}{video_path}'

        # Возвращаем медиафайл в ответе
        return send_file(media_file_path, as_attachment=True)
    except Exception as e:
        return f"Ошибка: {str(e)}"
    

if __name__ == '__main__':
    app.run(debug=False, host=host, port=port)
    

