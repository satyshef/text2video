# МАСА Лайв с автогенерацией базы из 5с нарезок
import lib.news as News
import lib.ff as ff

def get_config():
    conf = {
        "pieces_dir": "./source/pieces_bumaga",
        "audio_file": "./source/music/musik_bumaga.mp3",
        "output_dir": "./out/",
        "news_duration": 7,
        "intro_duration": 2,
        "max_str_length": 25,
        "logo_text": '\ БУМАГА   ',
        "intro_text_1": '\ БУМАГА   ',
        "intro_text_2": 'НОВОСТИ',
        "blur_strength": 8,
    }
    return conf

def __get_drawtext_introtext_1(start, duration, text):
    text = ff.prepare_text(text)
    end = start + duration
    fontsize = 40
    fontcolor = 'white'
    font = './fonts/Geist-SemiBold.otf'
    boxcolor = 'red@0.9'
    pos_x = '(w-text_w)/2'
    pos_y = '((h-text_h)/2)-120'
    enable = f"between(t,{start},{end})"
    drawtext=f"fontfile={font}:text='{text}':fontsize={fontsize}:fontcolor={fontcolor}:box=1:boxcolor={boxcolor}:boxborderw=20:x={pos_x}:y={pos_y}:enable='{enable}'"
    return drawtext

def get_drawtext_introtext_1(start, duration, text):
    text = ff.prepare_text(text)
    end = start + duration
    fontsize = 150
    fontcolor = 'white'
    font = './fonts/Uni Sans Heavy.otf'
    boxcolor = '#184887@1'
    pos_x = '(w-text_w)/2'
    pos_y = '((h-text_h)/2)'
    enable = f"between(t,{start},{end})"
    drawtext=f"fontfile={font}:text='{text}':fontsize={fontsize}:fontcolor={fontcolor}:box=1:boxcolor={boxcolor}:boxborderw=20:x={pos_x}:y={pos_y}:enable='{enable}'"
    return drawtext

def get_drawtext_introtime(start, duration, text):
    text = ff.prepare_text(text)
    end = start + duration
    fontsize = 70
    fontcolor = 'white'
    font = './fonts/Uni Sans Heavy.otf'
    pos_x = '(w-text_w)/2'
    pos_y = '((h-text_h)/2)+200'
    
    enable = f"between(t,{start},{end})"
    drawtext=f"fontfile={font}:text='{text}':fontsize={fontsize}:fontcolor={fontcolor}:x={pos_x}:y={pos_y}:enable='{enable}'"
    return drawtext


def get_drawtext_logo(start, duration, text):
    text = ff.prepare_text(text)
    end = start + duration
    fontsize = 65
    fontcolor = 'white'
    font = './fonts/Uni Sans Heavy.otf'
    boxcolor = '#184887@1'
    pos_x = '(w-text_w)/2'
    pos_y = '((h-text_h)/2)-700'
    enable = f"between(t,{start},{end})"
    drawtext=f"fontfile={font}:text='{text}':fontsize={fontsize}:fontcolor={fontcolor}:box=1:boxcolor={boxcolor}:boxborderw=20:x={pos_x}:y={pos_y}:enable='{enable}'"
    return drawtext



def get_drawtext_time(start, duration, text):
    text = ff.prepare_text(text)
    end = start + duration
    fontsize = 50
    fontcolor = 'white'
    font = './fonts/Uni Sans Heavy.otf'
    pos_x = '(w-text_w)/2-290'
    pos_y = '((h-text_h)/2)+620'
    enable = f"between(t,{start},{end})"
    drawtext=f"fontfile={font}:text='{text}':fontsize={fontsize}:fontcolor={fontcolor}:x={pos_x}:y={pos_y}:enable='{enable}'"
    return drawtext

def get_drawtext_news(start, duration, text):
    text = str(text)
    if str(text) == "":
        return ""
    text = ff.prepare_text(text)
    end = start + duration
    font = './Cocogoose-Narrow/Cocogoose-Narrow-Regular-trial.ttf'
    fontsize = 54
    fontcolor = 'black'
    pos_x = '(w-text_w)/2'
    pos_y = '((h-text_h)/2)'
    boxcolor = 'white@0.8'
    #boxcolor = '202020@0.8'
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
    #return output_file, None
    #output_file = 'out/base (копия).mp4'
    pos = conf['intro_duration']
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
        dt_news = get_drawtext_news(pos, conf['news_duration'], text_news)
        if dt_news == "":
            continue
        draws.append(dt_news)
        pos += conf['news_duration']

    #return "err"
    if len(draws) == 0:
        return '', 'Empty news list'
    clip_duration = conf['intro_duration'] + (conf['news_duration'] * len(draws))
    
    create_base(conf['pieces_dir'], output_file, conf['blur_strength'], conf['audio_file'], clip_duration)
    print("OK")
    #return "test", None
    #clip_duration = conf['news_duration'] * len(draws)
    dt_introtext1 = get_drawtext_introtext_1(0, conf['intro_duration'], conf['intro_text_1'])
    draws.append(dt_introtext1)
    #dt_introtext2 = get_drawtext_introtext_2(0, conf['intro_duration'], conf['intro_text_2'])
    #draws.append(dt_introtext2)
    dt_introtime = get_drawtext_introtime(0, conf['intro_duration'], news_time)
    draws.append(dt_introtime)

    dt_logo = get_drawtext_logo(conf['intro_duration'], clip_duration, conf['logo_text'])
    draws.append(dt_logo)
    dt_date = get_drawtext_time(conf['intro_duration'], clip_duration, news_time)
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