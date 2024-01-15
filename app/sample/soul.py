import lib.news as News
import lib.ff as ff

DEFAULT_NEWS_DURATION = 6

def get_config():
    conf = {
        "pieces_dir": "./source/pieces_bumaga",
        "audio_file": "./source/music/summer.mp3",
        "output_dir": "./out/",
        "intro_duration": 2,
        "news_duration": 8,
        "max_str_length": 25,
        "logo_text": 'соль',
        "intro_text_1": '\      СВОДКА',
        "intro_text_2": '\            СОЛЬ          |',
        "blur_strength": 8,
    }

    return conf

def get_drawtext_logo(start, duration, text):
    text = ff.prepare_text(text)
    end = start + duration
    fontsize = 35
    fontcolor = 'white'
    font = './fonts/NeverMindCompact/NeverMindCompact-Extrabold.ttf'
    boxcolor = '#1A3D9F@0.9'
    pos_x = '(w-text_w)/2'
    pos_y = '(h-123)'
    enable = f"between(t,{start},{end})"
    drawtext=f"fontfile={font}:text='{text}':fontsize={fontsize}:fontcolor={fontcolor}:box=1:boxcolor={boxcolor}:boxborderw=20:x={pos_x}:y={pos_y}:enable='{enable}'"
    return drawtext


def get_drawtext_intro_1(start, duration, text):
    text = ff.prepare_text(text)
    end = start + duration
    fontsize = 100
    fontcolor = 'black'
    font = './fonts/NeverMindCompact/NeverMindCompact-Extrabold.ttf'
    boxcolor = 'white@0.9'
    pos_x = 0
    pos_y = 538
    enable = f"between(t,{start},{end})"
    drawtext=f"fontfile={font}:text='{text}':fontsize={fontsize}:fontcolor={fontcolor}:box=1:boxcolor={boxcolor}:boxborderw=20:x={pos_x}:y={pos_y}:enable='{enable}'"
    return drawtext


def get_drawtext_intro_2(start, duration, text):
    text = ff.prepare_text(text)
    end = start + duration
    fontsize = 100
    fontcolor = 'white'
    font = './fonts/NeverMindCompact/NeverMindCompact-Extrabold.ttf'
    boxcolor = '#1A3D9F@0.9'
    pos_x = '(w-text_w)/2'
    pos_y = '(h-text_h)/2-280'
    enable = f"between(t,{start},{end})"
    drawtext=f"fontfile={font}:text='{text}':fontsize={fontsize}:fontcolor={fontcolor}:box=1:boxcolor={boxcolor}:boxborderw=20:x={pos_x}:y={pos_y}:enable='{enable}'"
    return drawtext

def get_drawtext_introtime(start, duration, text):
    text = ff.prepare_text(text)
    end = start + duration
    fontsize = 60
    fontcolor = 'white'
    font = './fonts/NeverMindCompact/NeverMindCompact-Medium.ttf'
    pos_x = '(w-text_w)/2'
    pos_y = '(h-text_h)/2-400'
    
    enable = f"between(t,{start},{end})"
    drawtext=f"fontfile={font}:text='{text}':fontsize={fontsize}:fontcolor={fontcolor}:x={pos_x}:y={pos_y}:enable='{enable}'"
    return drawtext


def get_drawtext_time(start, duration, text):
    text = ff.prepare_text(text)
    end = start + duration
    fontsize = 30
    fontcolor = 'white'
    font = './fonts/NeverMindCompact/NeverMindCompact-DemiBold.ttf'
    pos_x = '(w-text_w)/2'
    pos_y = 170
    enable = f"between(t,{start},{end})"
    drawtext=f"fontfile={font}:text='{text}':fontsize={fontsize}:fontcolor={fontcolor}:x={pos_x}:y={pos_y}:enable='{enable}'"
    return drawtext

def get_drawtext_news(start, duration, text):
    text = str(text)
    if str(text) == "":
        return ""
    text = ff.prepare_text(text)
    end = start + duration
    pos_x = '(w-text_w)/2'
    pos_y = '((h-text_h)/2)+20'
    fontsize = 38
    fontcolor = 'white'
    font = './fonts/NeverMindCompact/NeverMindCompact-Regular.ttf'
    boxcolor = '#CD0808@0.5'
    enable = f"between(t,{start},{end})"
    alpha = f"'if(lt(t,{start}),0,if(lt(t,{end}),(t-{start})/2,if(lt(t,2),1,if(lt(t,{start}0),(0-(t-2))/0,0))))'"
    drawtext = f"fontfile={font}:text='{text}':fontsize={fontsize}:fontcolor={fontcolor}:box=1:boxcolor={boxcolor}:boxborderw=40:x={pos_x}:y={pos_y}:enable='{enable}':alpha={alpha}"
    return drawtext


def create_base(pieces_dir, output_video, blur_strength, audio_file, duration):
    
    files = ff.get_videofiles_list(pieces_dir)
    if files == None:
        print("Error: empty pieces list")
        exit()

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
        dt_news = get_drawtext_news(clip_duration, news_duration, text)
        if dt_news == "":
            continue
        draws.append(dt_news)
        clip_duration += news_duration

    if len(draws) == 0:
        return '', 'Empty news list'
    
    create_base(conf['pieces_dir'], output_file, conf['blur_strength'], conf['audio_file'], clip_duration)
    
    #dt_intro1 = get_drawtext_intro_1(0, intro_duration, conf['intro_text_1'])
    #draws.append(dt_intro1)
    dt_intro2 = get_drawtext_intro_2(0, intro_duration, conf['intro_text_2'])
    draws.append(dt_intro2)
    dt_introtime = get_drawtext_introtime(0, intro_duration, news_time)
    draws.append(dt_introtime)
    #dt_promo = get_drawtext_promo(intro_duration, promo_duration, conf['promo'])
    #draws.append(dt_promo)
    dt_logo = get_drawtext_logo(intro_duration, clip_duration, conf['logo_text'])
    draws.append(dt_logo)
    dt_date = get_drawtext_time(intro_duration, clip_duration, news_time)
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