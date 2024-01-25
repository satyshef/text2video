# МАСА Лайв с автогенерацией базы из 5с нарезок
import lib.news as News
import lib.ff as ff

DEFAULT_NEWS_DURATION = 6

def get_config():
    conf = {
        "pieces_dir": "./source/base_news7/",
        "audio_file": "./source/music/collection1/funkyelement.mp3",
        "output_dir": "./out/",
        "news_duration": 7,
        "intro_duration": 2,
        "intro_font": "./fonts/azoft-sans/Azoft Sans-Bold.otf",
        "logo_text": '\ 7news          |',
        "intro_text": 'НОВОСТИ',
        "basic_font": "./fonts/cruinn/Cruinn Black.ttf",
        "max_str_length": 25,
        "blur_strength": 0,
    }

    return conf


def get_drawtext_intrologo(start, duration, font):
    text = '7'
    text = ff.prepare_text(text)
    end = start + duration
    fontsize = 200
    fontcolor = 'white'
    #font = './fonts/Geist-SemiBold.otf'
    #boxcolor = '#0080FF@0.9'
    boxcolor = '#CC0000@0.9'
    pos_x = '(w-text_w)/2'
    pos_y = '((h-text_h)/2)-250'
    enable = f"between(t,{start},{end})"
    drawtext=f"fontfile={font}:text='{text}':fontsize={fontsize}:fontcolor={fontcolor}:box=1:boxcolor={boxcolor}:boxborderw=40:x={pos_x}:y={pos_y}:enable='{enable}'"
    return drawtext


def get_drawtext_introtext(start, duration, text, font):
    text = ff.prepare_text(text)
    end = start + duration
    fontsize = 120
    fontcolor = 'white'
    #font = './fonts/Geist-SemiBold.otf'
    boxcolor = 'white@0.9'
    pos_x = '(w-text_w)/2'
    pos_y = '((h-text_h)/2)-60'
    enable = f"between(t,{start},{end})"
    drawtext=f"fontfile={font}:text='{text}':fontsize={fontsize}:fontcolor={fontcolor}:box=0:boxcolor={boxcolor}:boxborderw=20:x={pos_x}:y={pos_y}:enable='{enable}'"
    return drawtext

def get_drawtext_introtime(start, duration, text, font):
    text = ff.prepare_text(text)
    end = start + duration
    fontsize = 60
    fontcolor = 'white'
    #font = './fonts/Geist-SemiBold.otf'
    pos_x = '(w-text_w)/2'
    pos_y = '((h-text_h)/2)+40'
    
    enable = f"between(t,{start},{end})"
    drawtext=f"fontfile={font}:text='{text}':fontsize={fontsize}:fontcolor={fontcolor}:x={pos_x}:y={pos_y}:enable='{enable}'"
    return drawtext


def get_drawtext_logo(start, duration, text, font):
    text = ff.prepare_text(text)
    end = start + duration
    fontsize = 35
    fontcolor = 'white'
    #font = './fonts/Geist-SemiBold.otf'
    #boxcolor = '#0080FF@0.9'
    boxcolor = '#CC0000@0.9'
    pos_x = '(w-text_w)+10'
    pos_y = 150
    enable = f"between(t,{start},{end})"
    drawtext=f"fontfile={font}:text='{text}':fontsize={fontsize}:fontcolor={fontcolor}:box=1:boxcolor={boxcolor}:boxborderw=20:x={pos_x}:y={pos_y}:enable='{enable}'"
    return drawtext



def get_drawtext_time(start, duration, text, font):
    text = ff.prepare_text(text)
    end = start + duration
    fontsize = 35
    fontcolor = 'white'
    #font = './fonts/Geist-SemiBold.otf'
    pos_x = 30
    pos_y = 150
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
    fontsize = 38
    fontcolor = 'white'
    #boxcolor = '#606060@0.8'
    #boxcolor = 'black@0.8'
    boxcolor = '#0080FF@0.7'
    pos_x = '(w-text_w)/2'
    pos_y = '((h-text_h)/2)+70'
    enable = f"between(t,{start},{end})"
    alpha = f"'if(lt(t,{start}),0,if(lt(t,{end}),(t-{start})/2,if(lt(t,2),1,if(lt(t,{start}0),(0-(t-2))/0,0))))'"
    #drawtext = f"text='{text}':fontsize={fontsize}:fontcolor={fontcolor}:box=1:boxcolor={boxcolor}:boxborderw=20:x=(w-text_w)/2:y=((h-text_h)/2)-20:enable='{enable}':alpha={alpha}"
    drawtext = f"fontfile={font}:text='{text}':fontsize={fontsize}:fontcolor={fontcolor}:box=1:boxcolor={boxcolor}:boxborderw=40:x={pos_x}:y={pos_y}:enable='{enable}':alpha={alpha}"
    return drawtext


def create_base(pieces_dir, output_video, blur_strength, audio_file, duration):
    
    files = ff.get_videofiles_list(pieces_dir)
    if files == None:
        print("Error: empty pieces list")
        exit()
    
    #cut_and_concat_videos(files, output_video)
    ff.concatenate_videos(files, output_video, duration)
    ff.blur_video(output_video, output_video, blur_strength)
    ff.overlay_audio(output_video, audio_file, output_video)

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
        dt_news = get_drawtext_news(clip_duration, news_duration, text, conf['basic_font'])
        if dt_news == "":
            continue
        draws.append(dt_news)
        clip_duration += news_duration

    if len(draws) == 0:
        return '', 'Empty news list'
    
    audio_file = News.get_random_file_or_directory(conf['audio_file'])
    create_base(conf['pieces_dir'], output_file, conf['blur_strength'], audio_file, clip_duration)

    #clip_duration = conf['news_duration'] * len(draws)
    dt_intrologo = get_drawtext_intrologo(0, conf['intro_duration'], conf['intro_font'])
    draws.append(dt_intrologo)
    dt_introtext = get_drawtext_introtext(0, conf['intro_duration'], conf['intro_text'], conf['intro_font'])
    draws.append(dt_introtext)
    dt_introtime = get_drawtext_introtime(0, conf['intro_duration'], news_time, conf['intro_font'])
    draws.append(dt_introtime)
    dt_logo = get_drawtext_logo(conf['intro_duration'], clip_duration, conf['logo_text'], conf['intro_font'])
    draws.append(dt_logo)
    dt_date = get_drawtext_time(conf['intro_duration'], clip_duration, news_time, conf['intro_font'])
    draws.append(dt_date)
    #run(output_file, output_file, draws, clip_duration)
    #ff.remove_metadata(result_path, result_path)
    vf = ''
    for d in draws:
        if d == "" or d == None:
            continue
        vf = vf + 'drawtext=' + d + ','
    vf = vf.rstrip(',')
    ff.add_effect(output_file, output_file, vf, clip_duration)
    #ffmpeg.input(input_file).output(output_file, vf=params, t=duration).run()

    return output_file, None