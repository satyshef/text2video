import lib.news as News
import lib.ff as ff

def get_config():
    conf = {
        "pieces_dir": "./source/pieces_pepper_news",
        "audio_file": "./source/music/track_1.mp3",
        "output_dir": "./out/",
        "intro_duration": 2,
        "promo": "Больше новостей\nв нашем Телеграм\n\nСсылка в профиле",
        "promo_duration": 3,
        "news_duration": 7,
        "max_str_length": 25,
        "logo_text": 'перец',
        "intro_text_1": '\        ОСТРО',
        "intro_text_2": '\ НОВОСТИ           |',
        "blur_strength": 10,
    }

    return conf

def get_drawtext_logo(start, duration, text):
    text = ff.prepare_text(text)
    end = start + duration
    fontsize = 35
    fontcolor = 'red'
    font = './fonts/Geist-UltraBlack.otf'
    boxcolor = 'white@0.5'
    pos_x = '(w-text_w)/2'
    pos_y = '(h-100)'
    enable = f"between(t,{start},{end})"
    drawtext=f"fontfile={font}:text='{text}':fontsize={fontsize}:fontcolor={fontcolor}:box=0:boxcolor={boxcolor}:boxborderw=20:x={pos_x}:y={pos_y}:enable='{enable}'"
    return drawtext


def get_drawtext_intro_1(start, duration, text):
    text = ff.prepare_text(text)
    end = start + duration
    fontsize = 100
    fontcolor = 'white'
    font = './fonts/Geist-SemiBold.otf'
    boxcolor = 'red@0.9'
    pos_x = 0
    pos_y = 238
    enable = f"between(t,{start},{end})"
    drawtext=f"fontfile={font}:text='{text}':fontsize={fontsize}:fontcolor={fontcolor}:box=1:boxcolor={boxcolor}:boxborderw=20:x={pos_x}:y={pos_y}:enable='{enable}'"
    return drawtext

def get_drawtext_intro_2(start, duration, text):
    text = ff.prepare_text(text)
    end = start + duration
    fontsize = 100
    fontcolor = 'red'
    font = './fonts/Geist-SemiBold.otf'
    boxcolor = 'white@0.9'
    pos_x = 100
    pos_y = 360
    enable = f"between(t,{start},{end})"
    drawtext=f"fontfile={font}:text='{text}':fontsize={fontsize}:fontcolor={fontcolor}:box=1:boxcolor={boxcolor}:boxborderw=20:x={pos_x}:y={pos_y}:enable='{enable}'"
    return drawtext

def get_drawtext_introtime(start, duration, text):
    text = ff.prepare_text(text)
    end = start + duration
    fontsize = 60
    fontcolor = 'white'
    font = './fonts/Geist-SemiBold.otf'
    pos_x = '(w-text_w)/2'
    pos_y = '(h-text_h)/2'
    
    enable = f"between(t,{start},{end})"
    drawtext=f"fontfile={font}:text='{text}':fontsize={fontsize}:fontcolor={fontcolor}:x={pos_x}:y={pos_y}:enable='{enable}'"
    return drawtext

def get_drawtext_promo(start, duration, text):
    text = ff.prepare_text(text)
    end = start + duration
    fontsize = 40
    fontcolor = 'white'
    font = './fonts/Geist-SemiBold.otf'
    boxcolor = 'red@0.7'
    pos_x = '(w-text_w)/2'
    pos_y = '(h-text_h)/2'
    
    enable = f"between(t,{start},{end})"
    drawtext=f"fontfile={font}:text='{text}':fontsize={fontsize}:fontcolor={fontcolor}:box=1:boxcolor={boxcolor}:boxborderw=40:x={pos_x}:y={pos_y}:enable='{enable}'"
    return drawtext

def get_drawtext_time(start, duration, text):
    text = ff.prepare_text(text)
    end = start + duration
    fontsize = 30
    fontcolor = 'white'
    font = './fonts/Geist-SemiBold.otf'
    pos_x = '(w-text_w)/2'
    pos_y = 150
    enable = f"between(t,{start},{end})"
    drawtext=f"fontfile={font}:text='{text}':fontsize={fontsize}:fontcolor={fontcolor}:x={pos_x}:y={pos_y}:enable='{enable}'"
    return drawtext

def get_drawtext_news(start, duration, text):
    text = str(text)
    if str(text) == "":
        return ""
    text = ff.prepare_text(text)
    end = start + duration
    fontsize = 38
    fontcolor = 'white'
    boxcolor = 'red@0.7'
    enable = f"between(t,{start},{end})"
    alpha = f"'if(lt(t,{start}),0,if(lt(t,{end}),(t-{start})/2,if(lt(t,2),1,if(lt(t,{start}0),(0-(t-2))/0,0))))'"
    drawtext = f"text='{text}':fontsize={fontsize}:fontcolor={fontcolor}:box=1:boxcolor={boxcolor}:boxborderw=40:x=(w-text_w)/2:y=((h-text_h)/2)-20:enable='{enable}':alpha={alpha}"
    return drawtext


def create_base(pieces_dir, output_video, blur_strength, audio_file, duration):
    
    files = ff.get_videofiles_list(pieces_dir)
    if files == None:
        print("Error: empty pieces list")
        exit()

    ff.concatenate_videos(files, output_video, duration)
    ff.blur_video(output_video, output_video, blur_strength)
    ff.overlay_audio(output_video, audio_file, output_video)

def ___run(input_file, output_file, texts, duration):
    #params = 'drawtext=' + texts[0] + ',' + 'drawtext=' + texts[1]
    vf = ''
    for d in texts:
        if d == "" or d == None:
            continue
        vf = vf + 'drawtext=' + d + ','
    vf = vf.rstrip(',')
    ff.add_effect(input_file, output_file, vf, duration)
    #ffmpeg.input(input_file).output(output_file, vf=params, t=duration).run()

def run(news):
    conf = get_config()
    news_time = News.get_news_time()
    file_name = News.generate_filename(news['sample'], 'mp4')
    output_file = conf['output_dir'] + file_name
    intro_duration = conf['intro_duration']
    promo_duration = conf['promo_duration']
    pre_duration = intro_duration + promo_duration
    pos = pre_duration
    news_duration = conf['news_duration']
    # создаем размытую основу из кусков видео и наложенной музыкой
    draws = []
    news_list = news['data']
    #news_list = News.load_news()
    
    for n in news_list:
        # нарезаем строки
        text_news = News.split_text(n, conf['max_str_length'])
        if text_news == "":
            continue
        # получаем элемент drawtext
        dt_news = get_drawtext_news(pos, news_duration, text_news)
        if dt_news == "":
            continue
        draws.append(dt_news)
        pos += news_duration

    if len(draws) == 0:
        return '', 'Empty news list'
    clip_duration = pre_duration + (news_duration * len(news_list))
    create_base(conf['pieces_dir'], output_file, conf['blur_strength'], conf['audio_file'], clip_duration)
    
    dt_intro1 = get_drawtext_intro_1(0, intro_duration, conf['intro_text_1'])
    draws.append(dt_intro1)
    dt_intro2 = get_drawtext_intro_2(0, intro_duration, conf['intro_text_2'])
    draws.append(dt_intro2)
    dt_introtime = get_drawtext_introtime(0, intro_duration, news_time)
    draws.append(dt_introtime)
    dt_promo = get_drawtext_promo(intro_duration, promo_duration, conf['promo'])
    draws.append(dt_promo)
    dt_logo = get_drawtext_logo(0, clip_duration, conf['logo_text'])
    draws.append(dt_logo)
    dt_date = get_drawtext_time(pre_duration, clip_duration, news_time)
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