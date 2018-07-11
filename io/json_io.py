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
        data

    '''
    zip_file = zipfile.ZipFile(path)
    if os.path.isdir(path[0:-4] + "_files"):
        pass
    else:
        os.mkdir(path[0:-4] + "_files")
    for names in zip_file.namelist():
        zip_file.extract(names, path[0:-4] + "_files/")
    zip_file.close()
    data = _get_data(path[0:-4] + "_files/")
    return data

def _get_data(path):
    '''
    解析json文件并输出一个dict

    Author:
        maocili

    Args:
        path:解压后文件夹路径
    Returns:
        data {0: {'time': 0.0, 'players': [{'index': 1, 'team': 'Team A', 'chara': 'lucio', 'is_ult_ready': False, 'is_dead': False, 'ult_charge': 1, 'dva_status': 2},...

    '''
    json_dict = {}
    data=[]
    f_list = os.listdir(path)
    for i in f_list:
        # 筛选出json文件
        if os.path.splitext(i)[1] == '.json':
            file =  open(path+i, 'r')
            arr = json.load(file)
            if not type(arr) == dict:
                for line  in range(len(arr)):
                    json_dict[line] = arr[line]
                data.append(json_dict)
    return(data)


#  时 分 秒 转为 秒
time_format_s = lambda h, m, s: h * 60 * 60 + m * 60 + s

def get_eliminate(start,end):
    '''
      输出data_sheet1中指定时间段的击杀事件
      Author:
          maocili
      Args:
          start:开始时间
          end: 结束时间
      Returns:
          data_list
      '''
    file = open('UITEST_data_files\\data_sheet1.json', 'r')
    arr = json.load(file)
    for line in range(len(arr)):
        json_dict[line] = arr[line]
    data_list=[]
    for i in json_dict:
        time_arr = json_dict[i]['time'].split(':')
        time_s = time_format_s(int(time_arr[0]),int(time_arr[1]),float(time_arr[2]))
        if time_s>=start and time_s<=end and json_dict[i]['action']=='Eliminate':
            data_list.append(json_dict[i])
    return data_list

def get_arr_eliminate(data,start,end):
    '''
      输入一个包含击杀事件的array 开始时间 结束时间 在这个array之后添加从开始时间到结束时间内的击杀事件
        Author:
            maocili
        Args:
            data:包含击杀事件的arrary list
            start: 开始时间
            end: 结束时间
        Returns:
            eliminate_arr 在输入的list 基础上添加从开始时间到结束时间内的击杀事件

      '''
    eliminate_arr=data.copy()
    for i in data:
        time_arr = i['time'].split(':')
        time_s = time_format_s(int(time_arr[0]), int(time_arr[1]), float(time_arr[2]))
        if time_s>=start and time_s<=end and i['action']=='Eliminate':
            eliminate_arr.append(i)
    return eliminate_arr

# get_eliminate(20.5,33.0)
# file = open('UITEST_data_files\\data_sheet1.json', 'r')
# arr = json.load(file)
# get_arr_eliminate(arr,21,30)

# print(un_zip('UITEST_data.zip'))
