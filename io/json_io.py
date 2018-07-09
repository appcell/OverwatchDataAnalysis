import  zipfile
import os
import json

def un_zip(path):
    '''
    解压zip文件至 path _files

    Author:
        maocili

    Args:
        path:zip文件路径
    Returns:
        None

    '''
    zip_file = zipfile.ZipFile(path)
    if os.path.isdir(path[0:-4] + "_files"):
        pass
    else:
        os.mkdir(path[0:-4] + "_files")
    for names in zip_file.namelist():
        zip_file.extract(names, path[0:-4] + "_files/")
    zip_file.close()
    _get_data(path[0:-4] + "_files/")

def _get_data(path):
    '''
    解析json文件并输出一个dict

    Author:
        maocili

    Args:
        path:解压后文件夹路径
    Returns:
        None

    '''
    json_dict = {}
    f_list = os.listdir(path)
    for i in f_list:
        # 筛选出json文件
        if os.path.splitext(i)[1] == '.json':
            file =  open(path+i, 'r')
            arr = json.load(file)
            if not type(arr) == dict:
                for line  in range(len(arr)):
                    json_dict[line] = arr[line]
        print(json_dict)

un_zip('UITEST_data.zip')
