import json
import copy
json_dict = {}

'''
3. 1) 根据data_sheet3.json 输入开始时间和结束时间 输出该时间段内每个英雄的大招能量变化
   2) 输入一个包含每个英雄大招能量变化的array 开始时间 结束时间 修改这个array使其表示出在array的基础上 经过开始-结束这段时间之后 每个英雄的大招能量变化
   3) 输入开始和结束时间 输出一个包含这段时间内每个人每一帧的大招能量的array 格式应该是[选手1 选手2 ....]，其中每个选手包括[能量1 能量2...]这样的
'''

#  时 分 秒 转为 秒
time_format_s = lambda h, m, s: h * 60 * 60 + m * 60 + s


def get_ult(start,end):
    ult_list=[]

    #玩家英雄对应信息
    player_info = {}


    data_3_files = open('UITEST_data_files\\data_sheet3.json', 'r')
    data_3_json = json.load(data_3_files)

    data_2_files = open('UITEST_data_files\\data_sheet2.json', 'r')
    data_2_json = json.load(data_2_files)

    index_name={}
    for name,line in zip(data_2_json,range(len(data_2_json))):
        for players in name['players']:

            index_name['team'] = line
            index_name['name'] = players['name']

            player_info[players['index']]=index_name.copy()

    ult_change = {}
    for i in data_3_json:

        time_arr = i['time'].split(':')
        time_s = time_format_s(int(time_arr[0]), int(time_arr[1]), float(time_arr[2]))
        if start <= time_s and time_s <= end:

            ult_change['time'] = time_s

            for ult in i['players']:
                player_info[ult['index']]['chara'] = ult['chara']
                player_info[ult['index']]['ults'] = ult['ults']

            ult_change['ult_info'] = player_info.copy()
            ult_list.append(copy.deepcopy(ult_change))
    return ult_list


def ult_change(start, end, data):
    data = data.copy()
    arr_data = {}
    startTime={}
    endTime={}
    arr_time={}

    arr_data['start_time'] = start
    arr_data['end_time'] = end

    for data_info in data:
        if start == data_info['time']:
            startTime = data_info
        if end == data_info['time']:
            endTime  = data_info
    ult_info = {}
    info_list = []
    for s_index in startTime['ult_info']:
        varitation = endTime['ult_info'][s_index]['ults']-startTime['ult_info'][s_index]['ults']

        ult_info['team'] = startTime['ult_info'][s_index]['team']
        ult_info['player'] = startTime['ult_info'][s_index]['name']
        ult_info['ult_varitation'] =varitation

        info_list.append(ult_info.copy())
    arr_data['ult_info'] = copy.deepcopy(info_list)
    return arr_data



arr = get_ult(10.0,50.0)
# for i in arr:
#     print(i)
a = ult_change(15.0,25.0,arr)
print(a)
