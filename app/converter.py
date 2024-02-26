# Меняет разрешение на 720, соотношение сторон 9:16, удаляет метаданные, режит на куски

import lib.ff as ff
import lib.helper as helper


video_dir_path = '/Users/outsider/Source/python/text2video/source/video'
result_dir_path = '/Users/outsider/Source/python/text2video/source/1920_1080'
prefix = 'ff'
piece_duration = 9

def is_my_file(path):
    name = helper.get_file_name(path)
    name_split = name.split("_")
    if name_split[0] == prefix:
        return True
    return False


video_files = ff.get_videofiles_list(video_dir_path)
for file_path in video_files:
    if is_my_file(file_path) == True:
        continue

    #print(file_path)
    
    result_filename = helper.generate_filename(file_path)
    result_file_path = result_dir_path + "/" + result_filename
    vf = 'scale=1920:1080,format=yuv420p'
    ff.cut_video(file_path, result_dir_path, prefix, duration=piece_duration, vf = vf)
    #ff.change_resolution(file_path, result_file_path)
    #ff.cut_video(result_file_path, result_dir_path, prefix, duration=piece_duration)
    
    #helper.delete_file(result_file_path)
