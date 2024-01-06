from datetime import datetime, timedelta


TIMEZONE = 3

def load_news():
    file_path = 'source/news.txt'
    # Открыть файл для чтения
    with open(file_path, 'r', encoding='utf-8') as file:
        # Прочитать строки из файла и сохранить их в список
        lines = [line.strip() for line in file.readlines()]
    return lines


def get_current_time(timezone):
    
    utc_now = datetime.utcnow()

    # Создайте объект timedelta для задания разницы в часах
    target_offset = timedelta(hours=timezone)

    # Примените разницу к текущей дате и времени
    current_datetime = utc_now + target_offset
    return current_datetime

def get_news_time():
    # Примените разницу к текущей дате и времени
    current_datetime = get_current_time(TIMEZONE)
    # Вычислить разницу в минутах до следующего часа
    minutes_to_next_hour = 60 - current_datetime.minute

    # Если текущее время не в конце часа, округлить вверх
    if minutes_to_next_hour < 60:
        rounded_datetime = current_datetime + timedelta(minutes=minutes_to_next_hour)
        rounded_datetime = rounded_datetime.replace(second=0, microsecond=0)
    else:
        # Если уже конец часа, просто обнулить минуты
        rounded_datetime = current_datetime.replace(minute=0, second=0, microsecond=0)

    return rounded_datetime.strftime("%d.%m.%y %H:%M")

# Нарезаем строку на подстроки. max_string - максимальная длинна входной строки
def split_text(text, max_length=25, max_string=400):
    
    text = text.strip()
    if len(text) > max_string:
        return ""

    text = text.replace("\n", r" ")
    # Разбиваем текст на слова
    words = text.split()

    # Инициализируем список для хранения строк
    result = []
    current_line = ''

    # Обрабатываем каждое слово
    for word in words:
        # Проверяем, помещается ли текущее слово в текущую строку
        if len(current_line) + len(word) <= max_length:
            # Добавляем слово к текущей строке
            if current_line:
                current_line += ' '
            current_line += word
        else:
            # Добавляем текущую строку к результату
            result.append(current_line)
            # Начинаем новую строку с текущим словом
            current_line = word

    # Добавляем последнюю строку к результату
    if current_line:
        result.append(current_line)

    # Объединяем строки символом новой строки
    return '\n'.join(result)


def generate_filename(base, ext):
    current_datetime = get_current_time(TIMEZONE)
    result = base + '_' + current_datetime.strftime("%y%m%d%H%M%S") + "." + ext
    return result
    