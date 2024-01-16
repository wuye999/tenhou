import json,random,os,re
import copy
import pdb

# 生成1副牌
def get_cards():
    cards = []
    cards.extend(list(range(11,20)))  # 万
    cards.extend(list(range(21,30)))  # 饼
    cards.extend(list(range(31,40)))  # 索
    cards.extend(list(range(41,48)))  # 字
    cards = cards * 4
    cards.remove(15), cards.remove(25), cards.remove(35)
    cards.append(51), cards.append(52), cards.append(53)  # 赤宝牌
    return cards


# 生成开局点数
def get_count():
    target_sum = 100000
    num1 = random.randint(1, target_sum - 3)
    num2 = random.randint(1, target_sum - num1 - 2)
    num3 = random.randint(1, target_sum - num1 - num2 - 1)
    # 计算第四个数确保总和为100000
    num4 = target_sum - num1 - num2 - num3
    return [num1, num2, num3, num4]
   

# 从牌库中摸一张牌 
def get_draw():
    random_value = random.choice(cards)  # 随机选择一个值
    cards.remove(random_value)  # 删除选中的值
    return random_value 
 
    
# 返回选手id   
def cycle_values(value = "Aさん"):
    values = list(data.keys())
    index = values.index(value)
    next_index = (index + 1) % len(values)
    return values[next_index]


# 开始牌局
def party(player):
    # 摸牌
    # 每次摸牌都从预设手牌里摸，预设手牌为空，则从预设牌河摸牌，最后从牌山摸牌
    if is_r(data[player]['手牌']):  # 需要立直时，先从牌库摸牌，立直后从预设牌河、牌山摸牌
        feel_draw = get_draw() 
    elif len(data[player]['预设手牌']) >2:
        feel_draw = random.choice(data[player]['预设手牌'])
        data[player]['预设手牌'].remove(feel_draw)  # 取出
    elif len(data[player]['预设手牌']) <= 2 and data[player]['预设手牌']:
        if data[player]['预设牌河']:
            feel_draw = data[player]['预设牌河'][0]
            data[player]['预设牌河'].remove(feel_draw)  # 取出
        else:
            feel_draw = random.choice(data[player]['预设手牌'])
            data[player]['预设手牌'].remove(feel_draw)  # 取出
    elif data[player]['预设牌河']:
        feel_draw = data[player]['预设牌河'][0]
        data[player]['预设牌河'].remove(feel_draw)  # 取出
    else:
        feel_draw = get_draw()  
    data[player]['取牌'].append(feel_draw)
    data[player]['手牌'].append(feel_draw)
    # pdb.set_trace()
    # 出牌
    # 先从预设手牌对照里打出
    if data[player]['预设牌河对照']:
        # print('y')
        out_draw = data[player]['预设牌河对照'][0]
        data[player]['预设牌河对照'].remove(out_draw)  # 删除选中的值
    elif is_r(data[player]['出牌']):  # 立直后模切
        out_draw = feel_draw
    # 其次再从 手牌 - 预设手牌对照 里选择
    elif list(set(data[player]['手牌']) - set(data[player]['预设手牌对照'])):
        out_draw =  random.choice(list(set(data[player]['手牌']) - set(data[player]['预设手牌对照'])))
    else: 
        # 最后模切
        out_draw = feel_draw
    if feel_draw == out_draw:
        data[player]['出牌'].append(60)
    else:
        data[player]['出牌'].append(out_draw)
    # pdb.set_trace()
    # print(out_draw)
    # print(data[player]['手牌'])
    data[player]['手牌'].remove(out_draw)  # 删除选中的值
    # pdb.set_trace()
    # 切换选手
    player = cycle_values(player)  
    # 剩余14张牌结束, 朵拉和里朵拉指示牌已用掉2枚
    if len(cards) <= 12:
        return
    return party(player)
    

# 获取场次，输入“东3局”，返回2
def parse_round(words):
    chinese_numerals = {'零': 0, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9}
    # 分割文字，提取方位和局数
    if len(words) == 3 and words.endswith("局"):
        direction = words[0]
        round_number_str = words[1:-1]  # 去掉"局"
        if round_number_str.isdigit():
            round_number = int(round_number_str)
        else:
            try:
                round_number = int(chinese_numerals[round_number_str])
            except ValueError:
                return None  # 如果无法转换为整数，返回None
        # 根据方位和局数计算返回值
        if direction == "东":
            return (round_number - 1) % 4
        elif direction == "南":
            return (round_number - 1) % 4 + 4
        elif direction == "西":
            return (round_number - 1) % 4 + 8
        elif direction == "北":
            return (round_number - 1) % 4 + 12
    return None 


# 解析牌代码，输入“123m”, 返回['11','12','13']
def string_to_mahjong_list(mahjong_string):
    # print(mahjong_string)
    result = []
    L =  re.findall(r'r?\d+[mpsz]', mahjong_string)
    # print(L)
    for LL in L:
        current_mahjong = LL[-1]
        r = ''  # 保留立直标记r
        for char in LL[:-1]:
            if char.isdigit():
                result.append(r + char + current_mahjong)
            else: 
                # print("y")
                r = char  # 保留立直标记r
    # print(result)
    def mahjong_to_number(mahjong_string):
        suit_mapping = {'m': 10, 'p': 20, 's': 30, 'z': 40}
        if len(mahjong_string) == 2:  # 普通1p
            number = int(mahjong_string[0])
        elif len(mahjong_string) == 3 and 'r' in mahjong_string:  # r1p
            number = int(mahjong_string[1])
        suit = suit_mapping[mahjong_string[-1]]
        if number == 0:
            if suit == 10 : return 51
            if suit == 20 : return 52
            if suit == 30 : return 53
        if len(mahjong_string) == 2:
            return number + suit  # 返回int 21
        elif len(mahjong_string) == 3 and 'r' in mahjong_string: 
            return mahjong_string[0] + str(number + suit)  # 返回str r21
    converted_numbers = [mahjong_to_number(mj) for mj in result]
    return converted_numbers


# 创建data
def get_data():
    # 分配场次，座次，手牌
    # 获取东家位置
    masterid = parse_round(assign['场局次']) % 4  # 东家座位
    master = list(data.keys())[masterid]  # 东家昵称
    # 填充内容
    data[master]['点数'] = copy.deepcopy(assign['东家']['点数'])
    data[master]['预设手牌'] = copy.deepcopy(string_to_mahjong_list(assign['东家']['手牌']))
    data[master]['预设牌河'] = copy.deepcopy(string_to_mahjong_list(assign['东家']['牌河']))
    data[master]['预设手牌对照'] = copy.deepcopy(data[master]['预设手牌'])
    data[master]['预设牌河对照'] = copy.deepcopy(data[master]['预设牌河'])
    
    data[cycle_values(master)]['点数'] = copy.deepcopy(assign['南家']['点数'])
    data[cycle_values(master)]['预设手牌'] = copy.deepcopy(string_to_mahjong_list(assign['南家']['手牌']))
    data[cycle_values(master)]['预设牌河'] = copy.deepcopy(string_to_mahjong_list(assign['南家']['牌河']))
    data[cycle_values(master)]['预设手牌对照'] = copy.deepcopy(data[cycle_values(master)]['预设手牌'])
    data[cycle_values(master)]['预设牌河对照'] = copy.deepcopy(data[cycle_values(master)]['预设牌河'])
    
    data[cycle_values(cycle_values(master))]['点数'] = copy.deepcopy(assign['西家']['点数'])
    data[cycle_values(cycle_values(master))]['预设手牌'] = copy.deepcopy(string_to_mahjong_list(assign['西家']['手牌']))
    data[cycle_values(cycle_values(master))]['预设牌河'] = copy.deepcopy(string_to_mahjong_list(assign['西家']['牌河']))
    data[cycle_values(cycle_values(master))]['预设手牌对照'] = copy.deepcopy(data[cycle_values(cycle_values(master))]['预设手牌'])
    data[cycle_values(cycle_values(master))]['预设牌河对照'] = copy.deepcopy(data[cycle_values(cycle_values(master))]['预设牌河'])
    
    data[cycle_values(cycle_values(cycle_values(master)))]['点数'] = copy.deepcopy(assign['北家']['点数'])
    data[cycle_values(cycle_values(cycle_values(master)))]['预设手牌'] = copy.deepcopy(string_to_mahjong_list(assign['北家']['手牌']))
    data[cycle_values(cycle_values(cycle_values(master)))]['预设牌河'] = copy.deepcopy(string_to_mahjong_list(assign['北家']['牌河']))
    data[cycle_values(cycle_values(cycle_values(master)))]['预设手牌对照'] = copy.deepcopy(data[cycle_values(cycle_values(cycle_values(master)))]['预设手牌'])
    data[cycle_values(cycle_values(cycle_values(master)))]['预设牌河对照'] = copy.deepcopy(data[cycle_values(cycle_values(cycle_values(master)))]['预设牌河'])


# 输入“r21”，返回int 21
def extract_number(input_string):
    # 使用isdigit检查字符串是否由数字组成
    if isinstance(input_string, (int, float)):
        return input_string
    if 'r' in input_string:  # '立直r的判断'
        number_part = ''.join(char for char in input_string if char.isdigit())  # 将提取到的数字部分转换为整数
        return int(number_part)


# 判断‘r’是否存在列表里
def is_r(my_list):
    if 'r' in str(my_list):
        for index, item in enumerate(my_list):
            if isinstance(item, str) and 'r' in item:
                return [index, item]
    else:
        return False
    
    
# 制定配牌    
def licensing():    
    # 制定配牌    
    for player in data.keys():
        # 从牌山取出预设手牌
        for p in data[player]['预设手牌']:
            cards.remove(extract_number(p))
        # 从牌山取出预设牌河
        for p in data[player]['预设牌河']:
            cards.remove(extract_number(p))
        if is_r(data[player]['预设牌河']):  # 判断预设牌河里是否有立直
            # 计数巡目，从预设牌河中取  r序号 枚,加入配牌
            for _ in range( is_r(data[player]['预设牌河'])[0] + 1):
                if not data[player]['预设牌河']:
                    break
                p =  data[player]['预设牌河'][0]
                data[player]['配牌'].append(p)
                data[player]['预设牌河'].remove(p)  # 取出
        elif True:
            # 计数巡目，从预设手牌中取  13-巡目（预设牌河） 枚
            for _ in range(13 - len(data[player]['预设牌河'])):
                if not data[player]['预设手牌']:
                    break
                p =  random.choice(data[player]['预设手牌'])
                data[player]['配牌'].append(p)
                data[player]['预设手牌'].remove(p)  # 取出
            # 计数巡目，从预设牌河中取  13 - 配牌 枚
            for _ in range(13 - len(data[player]['配牌'])):
                if not data[player]['预设牌河']:
                    break
                p =  data[player]['预设牌河'][0]
                data[player]['配牌'].append(p)
                data[player]['预设牌河'].remove(p)  # 取出
        # 从牌山随机取出 剩余手牌
        for _ in range(13 - len(data[player]['配牌'])):
            data[player]['配牌'].append(get_draw())
        data[player]['手牌'] = copy.deepcopy(data[player]['配牌'])
        # print(data[player]['手牌'])

        
if __name__ == "__main__":
    # 指定场次，牌河，手牌
    # 报错是你需要的牌不幸被他家摸完了，请重新运行
    assign = {
        '场局次': '东4局',
        '本场数': 0,
        '场供': 1,
        '朵拉指示牌': "5p",
        '里朵拉指示牌': "",
        "东家": {'点数': 24500, '手牌': "11267m4p2246778s4s", '牌河': "4z8p7z1p1p"},  
        "南家": {'点数': 23500, '手牌': "", '牌河': "9s9m6z7z3s"},
        "西家": {'点数': 29500, '手牌': "", '牌河': "1s1z6z4sr8s"},  # r8s: 打8s立直
        "北家": {'点数': 21500, '手牌': "", '牌河': "2z1s6z4z4s"},
    }
    # 生成1副牌
    cards = get_cards()
    # 创建data
    data = {
        "Aさん": {'点数': None, '配牌': [], '手牌': [], '取牌': [], '出牌': [], '预设手牌': [], '预设牌河': [], '预设手牌对照': [], '预设牌河对照': []},
        "Bさん": {'点数': None, '配牌': [], '手牌': [], '取牌': [], '出牌': [], '预设手牌': [], '预设牌河': [], '预设手牌对照': [], '预设牌河对照': []},
        "Cさん": {'点数': None, '配牌': [], '手牌': [], '取牌': [], '出牌': [], '预设手牌': [], '预设牌河': [], '预设手牌对照': [], '预设牌河对照': []},
        "Dさん": {'点数': None, '配牌': [], '手牌': [], '取牌': [], '出牌': [], '预设手牌': [], '预设牌河': [], '预设手牌对照': [], '预设牌河对照': []},
    }
    get_data()  # 填充data
    
    # 生成天凤log
    Tenhou_log = {
        "title": ["玉の間四人南","Sat, 13 Jan 2024 13:52:48 GMT"],
        "name": list(data.keys()),  # 名称顺序 东，南，西，北
        "rule": {"disp":"玉の間四人南","aka53":1,"aka52":1,"aka51":1},
        "log": [[
            [parse_round(assign['场局次']), assign['本场数'], assign['场供']-1],  # 场次
            [data[player]['点数'] for player in data.keys()],  # 点数
            string_to_mahjong_list(assign['朵拉指示牌']),  # 朵拉指示牌
            string_to_mahjong_list(assign['里朵拉指示牌']),  # 里朵拉指示牌
        ]]
    }
    # 从牌山取出朵拉指示牌
    for value in string_to_mahjong_list(assign['朵拉指示牌']):
        cards.remove(value) 
    for value in string_to_mahjong_list(assign['里朵拉指示牌']):
        cards.remove(value) 
    # 生成配牌
    licensing()
    # 开始对局
    masterid = parse_round(assign['场局次']) % 4  # 东家座位
    master = list(data.keys())[masterid]  # 东家昵称
    party(master)
    # 生成天凤牌谱    
    # print(data)
    for player in data.keys():
        Tenhou_log['log'][0].append([extract_number(c) for c in data[player]['配牌']])
        Tenhou_log['log'][0].append([extract_number(c) for c in data[player]['取牌']])
        Tenhou_log['log'][0].append(data[player]['出牌'])
    Tenhou_log['log'][0].append(["和了",[-1300,3700,-700,-700],[1,1,1,"20符3飜700-1300点","門前清自摸和(1飜)","平和(1飜)","立直(1飜)","裏ドラ(0飜)"]])
    with open("tenhou_log.txt", "w", encoding='utf-8') as file:
        file.write("https://tenhou.net/5/#json=" + json.dumps(Tenhou_log,ensure_ascii=False) )
    print("生成牌谱成功。")

