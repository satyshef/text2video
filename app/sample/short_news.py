# МАСА Лайв генерация loop видео с новостями на одном экране
import lib.news as News
import lib.ff as ff
import lib.helper as helper


DEFAULT_NEWS_DURATION = 6

# default config
def get_config():
    conf = {
        "base_file": "./source/pieces_masa_live/",
        #"audio_file": "./source/music/collection1/funkyelement.mp3",
        "audio_file": './source/sound/clock5sec/',
        "output_dir": "./out/",
        #"clip_duration": 7,
        "logo_text": '\ Short news          |',
        "logo_font": "./fonts/azoft-sans/Azoft Sans-Bold.otf",
        "basic_font_color": 'white',
        "basic_font": "./fonts/inglobal/inglobal.ttf",
        "basic_font_size": 25,
        "max_str_length": 46,
        "max_text_length": 1300,
        "blur_strength": 0,
        "box_color": "#313131@0.8",
        "box_border": '40'
    }

    return conf

def get_drawtext_news(start, duration, text, font, fontcolor = 'white', fontsize = 30, boxcolor = '', boxborder = 20):
    text = str(text)
    if str(text) == "":
        return ""
    text = ff.prepare_text(text)
    end = start + duration
    #font = '' 
    #fontsize = 38
    #fontcolor = 'white'
    #boxcolor = '#404040@0.9'
    #boxcolor = '1C3866@0.9'
    #boxcolor = '#0080FF@0.9'
    pos_x = '(w-text_w)/2'
    pos_y = '((h-text_h)/2)'
    enable = f"between(t,{start},{end})"
    #alpha = f"'if(lt(t,{start}),0,if(lt(t,{end}),(t-{start})/2,if(lt(t,2),1,if(lt(t,{start}0),(0-(t-2))/0,0))))'"
    #drawtext = f"text='{text}':fontsize={fontsize}:fontcolor={fontcolor}:box=1:boxcolor={boxcolor}:boxborderw=20:x=(w-text_w)/2:y=((h-text_h)/2)-20:enable='{enable}':alpha={alpha}"
    if boxcolor == '':
        drawtext = f"fontfile={font}:text='{text}':fontsize={fontsize}:fontcolor={fontcolor}:box=0:boxcolor={boxcolor}:boxborderw={boxborder}:x={pos_x}:y={pos_y}"
    else:
        drawtext = f"fontfile={font}:text='{text}':fontsize={fontsize}:fontcolor={fontcolor}:box=1:boxcolor={boxcolor}:boxborderw={boxborder}:x={pos_x}:y={pos_y}"
    return drawtext



def run(news):
    if isinstance(news.get('sample'), str):
        conf = get_config()
        sample_name = news['sample']
    else:
        conf = news['sample']
        sample_name = news['sample']['name']
       
    
    news_time = News.get_news_time()
    input_file = ff.get_videofile(conf["base_file"])
    if input_file == None:
        return None, "Empty input video file"
    
    #return None, conf["base_file"]

    audio_file = ff.get_audiofile(conf["audio_file"])
    if audio_file == None:
        return None, "Empty input audio file"
    
    
    file_name = News.generate_filename(sample_name, 'mp4')
    output_file = conf['output_dir'] + file_name
    news_list = news['data']
    if len(news_list) == 0:
        return None, "Empty news list"
    draws = []
    drawtext = ''
    #drawtext = '- ' + news_list[0]
    #drawtext = "Главное на данный момент:"

    # Собираем текст
    for line in news_list:
        text = News.split_text(line, conf['max_str_length'])
        if text == "":
            continue
        
        temptext = drawtext + '\n\n- ' + text
        if len(temptext) > conf['max_text_length']:
            break
        drawtext = temptext

    # определяем длинну клипа
    if "clip_duration" in conf:
        clip_duration = conf["clip_duration"]
    else:
        clip_duration = ff.get_video_duration(input_file)
        
    box_color = helper.get_random_parametr(conf['box_color'])
    
    # получаем элемент drawtext
    dt_news = get_drawtext_news(0, clip_duration, drawtext, conf['basic_font'], conf['basic_font_color'], conf['basic_font_size'], box_color, conf['box_border'])
    if dt_news == "":
            return '', 'Empty draw text'
    
    draws.append(dt_news)
    vf = ''
    for d in draws:
        if d == "" or d == None:
            continue
        vf = vf + 'drawtext=' + d + ','
    vf = vf.rstrip(',')
    ff.add_effect(input_file, output_file, vf, clip_duration)

    # Накладываем картинку
    if "image" in conf and "file" in conf["image"]:
        image = conf["image"]
        file = image["file"]
        size = helper.get_random_parametr(image["size"])
        pos_x = helper.get_random_parametr(image["pos_x"])
        pos_y = helper.get_random_parametr(image["pos_y"])
        if size != None and pos_x != None and pos_y != None:
            ff.add_image(output_file, output_file, file, size, pos_x, pos_y)
            
    #ff.add_image(output_file, output_file, conf["image_file"], size=260, pos_x=180, pos_y=500)
    ff.overlay_audio(output_file, audio_file, output_file)
    return output_file, None