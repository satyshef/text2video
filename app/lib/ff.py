import os
import random

import ffmpeg
import lib.helper as helper


def cut_video(input_file, output_dir, output_file_prefix, duration=10):
    """
    Разрезает видеофайл на кусочки заданной длительности.

    Параметры:
    - input_file: Путь к входному видеофайлу.
    - output_file_prefix: Префикс для имен выходных файлов.
    - duration: Длительность каждого куска в секундах (по умолчанию 10 секунд).

    Пример:
    cut_video("input_video.mp4", "output_chunk", duration=15)
    """
    #file_name = helper.get_file_name(input_file)
    
    try:
        # Получаем общую информацию о видео
        probe = ffmpeg.probe(input_file)
        # Определение общей длительности видео
        total_duration = float(probe['format']['duration'])

        # Определяем количество частей
        num_segments = int(total_duration / duration)
        if num_segments == 0:
            return
        # Отрезаем видео на кусочки
        for i in range(num_segments):
            start_time = i * duration
            file_name = helper.generate_filename(input_file)
            output_file = f"{output_dir}/{output_file_prefix}_{file_name}"
            #output_file = f"'{output_dir}/{output_file_prefix}_{file_name}_{i+1}.mp4'"
            #ffmpeg.input(input_file, ss=start_time, t=duration).output(output_file).run()
            #work
            #ffmpeg.input(input_file, ss=start_time, t=duration).output(output_file, **{'b:v': '1100k'}, r=30, c='libx264', an=None, map_metadata=-1).run()
            #test
            #yuv420p10le 720x1280
            #
            #vf = 'scale=1080:1920,format=yuv420p'
            vf = 'scale=720:1280,format=yuv420p'
            ffmpeg.input(input_file, ss=start_time, t=duration).output(output_file, **{'pix_fmt': 'yuv420p'}, r=30, vf=vf, c='libx264', an=None, map_metadata=-1).run()

        # Проверяем, остался ли необработанный фрагмент
        #remaining_duration = total_duration - num_segments * duration
        #if remaining_duration >= duration:
        #    start_time = num_segments * duration
        #    output_file = f"{output_file_prefix}_{num_segments+1}.mp4"
        #    ffmpeg.input(input_file, ss=start_time, t=duration).output(output_file).run()

        # Проверяем длинну последнего куска
        probe = ffmpeg.probe(output_file)
        # Определение общей длительности видео
        part_duration = float(probe['format']['duration'])
        if part_duration < duration:
            os.remove(output_file)

        print("Видео успешно разрезано на кусочки.")
    except ffmpeg.Error as e:
        print(f"Произошла ошибка при разрезании видео: {e.stderr}")


# Склеиваем список файлов
def concatenate_videos(input_files, output_file, duration):
    concat_file = 'concat.txt'
    open(concat_file, 'w').writelines([('file %s\n' % input_path) for input_path in input_files])
    ffmpeg.input(concat_file, format='concat', safe=0).output(output_file, c='copy', t=duration).run(overwrite_output=True)
    os.remove(concat_file)

# Меняем разрешение и соотношение сторон, удаляет звук и метаданные
def change_resolution(input_file, output_file):
    #if os.path.exists(output_file):
    #video_bitrate='1000k', frame_rate=30
    try:
        input_stream = ffmpeg.input(input_file)
        #output_stream = ffmpeg.output(input_stream, output_file, vf='scale=1280:-1', **{'b:v': '1000k'}, r=30, c='libx264', aspect='9:16', an=None, map_metadata=-1)
        output_stream = ffmpeg.output(input_stream, output_file, an=None, map_metadata=-1)
        ffmpeg.run(output_stream, overwrite_output=True)
        print(f"Файл {input_file} успешно преобразован и сохранен в {output_file}")
    except ffmpeg.Error as e:
        print(f"Произошла ошибка при обработке файла: {e.stderr}")


# Получаем список видеофайлов в заданной директории
def get_videofiles_list(input_dir):
    video_files = [f for f in os.listdir(input_dir) if f.endswith(('.mp4', '.avi', '.mkv'))]
    result = []
    for video_file in video_files:
        result.append(os.path.join(input_dir, video_file))

    random.shuffle(result)
    return result


# Удалить метаданные. Если входной и выходной файл совподают тогда произойдет замена
def remove_metadata(input_file, output_file):
    # Если заменяем файл
    if input_file == output_file:
        output_file_path = output_file + ".tmp"
    else:
        output_file_path = output_file
    try:
        input_stream = ffmpeg.input(input_file)
        output_stream = ffmpeg.output(input_stream, output_file_path, map_metadata=-1)
        ffmpeg.run(output_stream, overwrite_output=True)
        if input_file == output_file:
            os.rename(output_file_path, output_file)
        print(f"Метаданные из файла {input_file} успешно удалены, и результат сохранен в {output_file}")
        

    except ffmpeg.Error as e:
        print(f"Произошла ошибка при обработке файла: {e.stderr}")


def add_effect(input_file, output_file, vf, duration):
    # Если заменяем файл
    if input_file == output_file:
        #output_file_path = "tmp.mp4"
        output_file_path = get_temp_filename(output_file)
    else:
        output_file_path = output_file
    try:
        input_stream = ffmpeg.input(input_file)
        output_stream = ffmpeg.output(input_stream, output_file_path, vf=vf, t=duration, map_metadata=-1)
        ffmpeg.run(output_stream, overwrite_output=True)
        if input_file == output_file:
            os.rename(output_file_path, output_file)
        print(f"Эффекты успешно применены к файлу  {output_file}")
        

    except ffmpeg.Error as e:
        print(f"Произошла ошибка при обработке файла: {e.stderr}")


def overlay_audio(input_video, input_audio, output_file):
    """
    Налагивает аудио на видео.

    Параметры:
    - input_video: Путь к входному видеофайлу.
    - input_audio: Путь к входному аудиофайлу.
    - output_video: Путь к выходному видеофайлу.

    Пример:
    overlay_audio("input_video.mp4", "input_audio.mp3", "output_video.mp4")
    """
    # Если заменяем файл
    if input_video == '':
        return
    
    if input_video == output_file:
        #output_file_path = "tmp.mp4"
       output_file_path = get_temp_filename(output_file)
    else:
        output_file_path = output_file

    try:
        probe = ffmpeg.probe(input_video)
        # Определение длительности видео
        duration = float(probe['format']['duration'])
        video_stream = ffmpeg.input(input_video)
        audio_stream = ffmpeg.input(input_audio)
        ffmpeg.concat(video_stream, audio_stream, v=1, a=1).output(output_file_path, t=duration).run(overwrite_output=True)
        
        #output(output_file_path, acodec='aac', vcodec='copy', shortest=None).run(overwrite_output=True)
        if input_video == output_file:
            os.rename(output_file_path, output_file)

        print("Аудио успешно наложено на видео.")
    except ffmpeg.Error as e:
        print(f"Произошла ошибка при наложении аудио на видео: {e.stderr}")


def get_video_duration(file):
    try:
        # Определение длительности видео
        probe = ffmpeg.probe(file)
        return float(probe['format']['duration'])
    except ffmpeg.Error as e:
        print(f"Произошла ошибка при получении длительности видео: {e.stderr}")
        return 0

def blur_video(input_file, output_file, blur_strength=5):
    """
    Размывает видео с использованием фильтра boxblur.

    Параметры:
    - input_file: Путь к входному видеофайлу.
    - output_file: Путь к выходному видеофайлу.
    - blur_strength: Степень размытия (по умолчанию 5).

    Пример:
    blur_video("input_video.mp4", "output_blurred.mp4", blur_strength=10)
    """
    if blur_strength == 0:
        return
    # Если заменяем файл
    if input_file == output_file:
        #output_file_path = "tmp.mp4"
        output_file_path = get_temp_filename(output_file)
    else:
        output_file_path = output_file
    try:
        ffmpeg.input(input_file).output(output_file_path, vf=f'boxblur=luma_radius={blur_strength}:luma_power={blur_strength}').run(overwrite_output=True)
        if input_file == output_file:
            os.rename(output_file_path, output_file)

        print("Видео успешно размыто.")
    except ffmpeg.Error as e:
        print(f"Произошла ошибка при размытии видео: {e.stderr}")



def prepare_text(text):
    text = text.replace(':', r'\:')
    text = text.replace("%", r'\\%')
    text = text.replace('"', '\"')
    text = text.replace("'", "\"")
    text = text.replace("`", "\"")
    text = text.replace("«", "\"")
    text = text.replace("»", "\"")
    return text


def get_temp_filename(path):
    
    ext = "." + helper.get_file_extension(path)
    path = path.replace(ext, '.tmp' + ext)
    return path