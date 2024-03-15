from PIL import Image, ImageDraw, ImageFont
import textwrap
import os
from datetime import datetime, timedelta

# Размещает текущее время с округлением в большую сторону на изображении

FONT = 'app/fonts/Geist-UltraBlack.otf'
FONT_SIZE = 80
INPUT_IMAGE = 'source/images/masa_stream.png'
TIMEZONE = 3

def place_text_center(image_path, output_path, text, font_path=None, font_size=40):
    """
    Размещает текст по центру изображения.
    
    :param image_path: Путь к исходному изображению.
    :param output_path: Путь для сохранения результата.
    :param text: Текст для размещения на изображении.
    :param font_path: Путь к файлу шрифта. Если None, используется шрифт по умолчанию.
    :param font_size: Размер шрифта.
    """
    # Загрузка изображения
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    # Задание шрифта
    if font_path:
        font = ImageFont.truetype(font_path, font_size)
    else:
        font = ImageFont.load_default()

    # Вычисление размера текста
    text_width, text_height = draw.textsize(text, font=font)

    # Получение размера изображения
    image_width, image_height = image.size

    # Вычисление позиции для текста
    x = (image_width - text_width) / 2
    y = (image_height - text_height) / 2 - 200

    # Размещение текста
    draw.text((x, y), text, font=font, fill="white")

    # Сохранение изображения
    output_path += '/out_' + os.path.basename(image_path)
    image.save(output_path)

def get_current_time(timezone):
    
    utc_now = datetime.utcnow()

    # Создайте объект timedelta для задания разницы в часах
    target_offset = timedelta(hours=timezone)

    # Примените разницу к текущей дате и времени
    current_datetime = utc_now + target_offset
    return current_datetime

def get_news_time(format=None, round=True):
    # Примените разницу к текущей дате и времени
    current_datetime = get_current_time(TIMEZONE)
    # Вычислить разницу в минутах до следующего часа
    minutes_to_next_hour = 60 - current_datetime.minute

    if round:
        # Если текущее время не в конце часа, округлить вверх
        if minutes_to_next_hour < 60:
            result_datetime = current_datetime + timedelta(minutes=minutes_to_next_hour)
            result_datetime = result_datetime.replace(second=0, microsecond=0)
        else:
            # Если уже конец часа, просто обнулить минуты
            result_datetime = current_datetime.replace(minute=0, second=0, microsecond=0)
    else:
        result_datetime = current_datetime

    if format == 'usa':
        return result_datetime.strftime("%m/%d/%y %I:%M %p")
    else:
        return result_datetime.strftime("%d.%m.%y %H:%M")


# Пример использования функции
text = get_news_time(format=None, round=False)
place_text_center(INPUT_IMAGE, "out", text, FONT, FONT_SIZE)