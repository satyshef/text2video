import lib.news as News
import ffmpeg
import lib.ff as ff


DEFAULT_NEWS_DURATION = 6

def get_config():
    conf = {
        "input_file": "./source/bases/trk_base.mp4",
        "output_dir": "./out/",
        "intro_duration": 2,
        "news_duration": 7,
        "max_str_length": 25,
        "logo_text": '\     МАСА Лайв',
    }

    return conf

def get_drawtext_introtime(start, duration, text):
    text = ff.prepare_text(text)
    end = start + duration
    fontsize = 80
    fontcolor = 'white'
    font = './fonts/Uni Sans Heavy.otf'
    pos_x = '(w-text_w)/2'
    pos_y = '(h-text_h)/2'
    
    enable = f"between(t,{start},{end})"
    drawtext=f"fontfile={font}:text='{text}':fontsize={fontsize}:fontcolor={fontcolor}:x={pos_x}:y={pos_y}:enable='{enable}'"
    return drawtext


def get_drawtext_time(start, duration, text):
    text = ff.prepare_text(text)
    end = start + duration
    fontsize = 45
    fontcolor = 'white'
    font = './fonts/Uni Sans Heavy.otf'
    pos_x = 670
    pos_y = 1670
    enable = f"between(t,{start},{end})"
    drawtext=f"fontfile={font}:text='{text}':fontsize={fontsize}:fontcolor={fontcolor}:x={pos_x}:y={pos_y}:enable='{enable}'"
    return drawtext

def get_drawtext_news(start, duration, text):
    text = str(text)
    if str(text) == "":
        return ""
    text = ff.prepare_text(text)
    end = start + duration
    font = './fonts/Uni Sans Heavy.otf'
    fontsize = 50
    fontcolor = 'white'
    pos_x = '(w-text_w)/2'
    pos_y = '((h-text_h)/2)+70'
    boxcolor = 'black@0.2'
    enable = f"between(t,{start},{end})"
    alpha = f"'if(lt(t,{start}),0,if(lt(t,{end}),(t-{start})/2,if(lt(t,2),1,if(lt(t,{start}0),(0-(t-2))/0,0))))'"
    drawtext = f"fontfile={font}:text='{text}':fontsize={fontsize}:fontcolor={fontcolor}:box=1:boxcolor={boxcolor}:boxborderw=40:x={pos_x}:y={pos_y}:enable='{enable}':alpha={alpha}"
    return drawtext



def run(news):
    conf = get_config()
    news_time = News.get_news_time()
    file_name = News.generate_filename(news['sample'], 'mp4')
    output_file = conf['output_dir'] + file_name
    intro_duration = conf['intro_duration']
    news_list = news['data']
    
    # создаем размытую основу из кусков видео и наложенной музыкой
    draws = []
    clip_duration = intro_duration
    
    for line in news_list:
        news_duration, text = News.parse_line(line)
        if news_duration == 0:
            if 'news_duration' in conf:
                news_duration = conf['news_duration']
            else:
                news_duration = DEFAULT_NEWS_DURATION
            
        # нарезаем текст на строки
        text = News.split_text(text, conf['max_str_length'])
        if text == "":
            continue

        # получаем элемент drawtext
        dt_news = get_drawtext_news(clip_duration, news_duration, text)
        if dt_news == "":
            continue
        draws.append(dt_news)
        clip_duration += news_duration

    if len(draws) == 0:
        return '', 'Empty news list'
    
    dt_introtime = get_drawtext_introtime(0, conf['intro_duration'], news_time)
    draws.append(dt_introtime)
    #dt_logo = get_drawtext_logo(0, clip_duration, conf['logo_text'])
    #draws.append(dt_logo)
    dt_date = get_drawtext_time(conf['intro_duration'], clip_duration, news_time)
    draws.append(dt_date)
    vf = ''
    for d in draws:
        if d == "" or d == None:
            continue
        vf = vf + 'drawtext=' + d + ','
    vf = vf.rstrip(',')
    ffmpeg.input(conf['input_file']).output(output_file, vf=vf, t=clip_duration).run()
    #ff.add_effect(output_file, output_file, vf, clip_duration)
    #ffmpeg.input(input_file).output(output_file, vf=params, t=duration).run()

    return output_file, None
    #run(conf['input_file'], output_file, draws, clip_duration)