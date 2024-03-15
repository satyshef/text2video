from PIL import Image, ImageDraw, ImageFont
#import textwrap
import os
import time

# Размещает текущее время с округлением в большую сторону на изображении
def place_text_center(input_path, output_path, text, font_path=None, font_size=40):
    """
    Размещает текст по центру изображения.
    
    :param image_path: Путь к исходному изображению.
    :param output_path: Путь для сохранения результата.
    :param text: Текст для размещения на изображении.
    :param font_path: Путь к файлу шрифта. Если None, используется шрифт по умолчанию.
    :param font_size: Размер шрифта.
    """
    # Загрузка изображения
    image = Image.open(input_path)
    draw = ImageDraw.Draw(image)
    
    # Задание шрифта
    if font_path:
        font = ImageFont.truetype(font_path, font_size)
    else:
        font = ImageFont.load_default()
    
    # Вычисление размера текста
    #text_width, text_height = draw.textlength(text, font=font)
    _, _, text_width, text_height = draw.textbbox((0, 0), text=text, font=font)
    #text_width = draw.textlength(text, font=font)
    #text_height = 0
    # Получение размера изображения
    image_width, image_height = image.size
    
    # Вычисление позиции для текста
    x = (image_width - text_width) / 2
    y = (image_height - text_height) / 2

    # Размещение текста
    draw.text((x, y), text, font=font, fill="white", align="center")

    
    # Сохранение изображения
    image.save(output_path)
    return True
