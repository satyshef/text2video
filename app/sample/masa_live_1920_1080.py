# МАСА Лайв с автогенерацией базы из 5с нарезок
import lib.news as News
import lib.ff as ff

DEFAULT_NEWS_DURATION = 6

def get_config():
    conf = {
        "base_file": "./source/1920_1080",
        #"base_file": "./source/1920_1080/ff_1708969273_160425.mp4",
        #"audio_file": "./source/music/collection1/funkyelement.mp3",
        "audio_file": '',
        "output_dir": "./out/",
        #"clip_duration": 7,
        "logo_text": '\ МАСА Лайв         |',
        "logo_font": "./fonts/azoft-sans/Azoft Sans-Bold.otf",
        "basic_font": "./fonts/azoft-sans/Azoft Sans.otf",
        "max_str_length": 70,
        "max_text_length": 800,
        "blur_strength": 0,
    }

    return conf


def get_drawtext_logo(start, duration, text, font):
    text = ff.prepare_text(text)
    end = start + duration
    fontsize = 25
    fontcolor = 'white'
    #font = './fonts/Geist-SemiBold.otf'
    #boxcolor = '#0080FF@0.9'
    boxcolor = '#CC0000@0.9'
    pos_x = '(w-text_w)+10'
    pos_y = '(h-text_h)-50'
    enable = f"between(t,{start},{end})"
    drawtext=f"fontfile={font}:text='{text}':fontsize={fontsize}:fontcolor={fontcolor}:box=1:boxcolor={boxcolor}:boxborderw=20:x={pos_x}:y={pos_y}:enable='{enable}'"
    return drawtext



def get_drawtext_time(start, duration, text, font):
    text = ff.prepare_text(text)
    end = start + duration
    fontsize = 25
    fontcolor = 'white@0.9'
    #font = './fonts/Geist-SemiBold.otf'
    pos_x = 70
    pos_y = '(h-text_h)-50'
    enable = f"between(t,{start},{end})"
    drawtext=f"fontfile={font}:text='{text}':fontsize={fontsize}:fontcolor={fontcolor}:x={pos_x}:y={pos_y}:enable='{enable}'"
    return drawtext

def get_drawtext_news(start, duration, text, font):
    text = str(text)
    if str(text) == "":
        return ""
    text = ff.prepare_text(text)
    end = start + duration
    #font = '' 
    fontsize = 30
    fontcolor = 'white'
    #boxcolor = '#404040@0.9'
    boxcolor = '004C99'
    #boxcolor = '#0080FF@0.9'
    pos_x = '(w-text_w)/2'
    pos_y = '((h-text_h)/2)-50'
    enable = f"between(t,{start},{end})"
    delta = 2
    #alpha = f"'if(lt(t,{start}),0,if(lt(t,{end}),(t-{start})/2,if(lt(t,2),1,if(lt(t,{start}0),(0-(t-2))/0,0))))'"
    alpha = f"'if(lt(t,{start}),0,if(lt(t,0),(t-0)/0,if(lt(t,({end}-{delta})),1,if(lt(t,{end}),(2-(t-({end}-{delta})))/2,0))))'"
    drawtext = f"fontfile={font}:text='{text}':fontsize={fontsize}:fontcolor={fontcolor}:box=1:boxcolor={boxcolor}:boxborderw=20:x=(w-text_w)/2:y=((h-text_h)/2)-20:enable='{enable}':alpha={alpha}"
    #drawtext = f"fontfile={font}:text='{text}':fontsize={fontsize}:fontcolor={fontcolor}:box=1:boxcolor={boxcolor}:boxborderw=40:x={pos_x}:y={pos_y}"
    return drawtext


def run(news):
    conf = get_config()
    news_time = News.get_news_time()
    input_file = ff.get_videofile(conf["base_file"])
    
    file_name = News.generate_filename(news['sample'], 'mp4')
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
        text = News.split_text(line, conf['max_str_length'], conf['max_text_length'])
        if text == "":
            continue
        temptext = drawtext + '\n\n' + text
        if len(temptext) > conf['max_text_length']:
            break
        drawtext = temptext

    # определяем длинну клипа
    if "clip_duration" in conf:
        clip_duration = conf["clip_duration"]
    else:
        clip_duration = ff.get_video_duration(input_file)

    # получаем элемент drawtext
    dt_news = get_drawtext_news(0, clip_duration, drawtext, conf['basic_font'])
    if dt_news == "":
            return '', 'Empty draw text'
    
    draws.append(dt_news)
    dt_logo = get_drawtext_logo(0, clip_duration, conf['logo_text'], conf['logo_font'])
    draws.append(dt_logo)
    dt_date = get_drawtext_time(0, clip_duration, news_time, conf['logo_font'])
    draws.append(dt_date)
    #run(output_file, output_file, draws, clip_duration)
    #ff.remove_metadata(result_path, result_path)
    vf = ''
    for d in draws:
        if d == "" or d == None:
            continue
        vf = vf + 'drawtext=' + d + ','
    vf = vf.rstrip(',')
    ff.add_effect(input_file, output_file, vf, clip_duration)
    #ffmpeg.input(input_file).output(output_file, vf=params, t=duration).run()

    return output_file, None
    