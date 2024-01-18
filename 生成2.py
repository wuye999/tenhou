######################################
# 根据可见手牌和牌河生成天凤牌谱。或者对牌谱中的手牌、牌河、点数状况等信息进行自定义编辑，并生成天凤牌谱链接
# 多个副露请用空格隔开，如"55碰5z 吃340s"
# 指定副露时，相关牌河里一定要有打出被副露的牌。例如指定碰对家8s，对家牌河需要存在8s才能被碰。
# 不能出现4枚以上一样的牌，不能出现2枚相同的赤宝牌，不能设置吃或碰后模切，否则会报错

# 牌河手模切写法：手切标志无，模切标志"d"。  手切8s:"8s"   模切8s:"d8s"
# 立直写法：立直标志"r"，立直后无需模切标志，统统模切。   打8s立直:"r8s"    模切8s立直"dr8s"
# 副露写法
## 吃。    13m吃2m:"吃213m"。
## 碰。    碰上家8s:"碰888s"   碰对家8s:"8碰88s"    碰下家8s:"88碰8s"
## 杠。    杠上家8s:"杠8888s"  杠对家8s:"8杠888s"   杠下家8s:"888杠8s"
## 暗杠。  暗杠8s:"888暗8m"
## 加杠。  碰上家8s,之后加杠8s:"碰888s 加8888s"   碰对家8s,之后加杠8s:"8碰88s 8加888s"   碰下家8s,之后加杠8s:"88碰8s 88加88s"
assign = {
    '场局次': '东1局',
    '本场数': 0,
    '场供': 1,
    '朵拉指示牌': "8p",
    '里朵拉指示牌': "",
    "东家": {
        '点数': 24000, 
        '手牌': "78m23457788899s", 
        '副露': "", 
        '牌河': "3z1m7sdr1sd3z6zd4m1z"
        },  
    "南家": {
        '点数': 25000, 
        '手牌': "", 
        '副露': "", 
        '牌河': "3z1sr5z7s1p4s8p6p"
        },
    "西家": {
        '点数': 25000, 
        '手牌': "", 
        '副露': "", 
        '牌河': "4zd1s9m7z1z1pd2m8p"
        },
    "北家": {
        '点数': 25000, 
        '手牌': "", 
        '副露': "", 
        '牌河': "d1p2m7z3z2zd6zd5pd2zr5p"
        },
}


######################################
######################################
######################################


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


# 检查副露 返回副露的牌组
def Inspection_dew(player):
    for paizu in data[player]['副露']:
        if 'c' in paizu:  # 吃
            eaten = int (paizu[1:3])  # 需要吃的牌
            if eaten == data[cycle_values(cycle_values(cycle_values(player)))]['最后出牌']:  # 与上家最后一次出牌对比
                return paizu
        elif 'p' in paizu:  # 碰
            index = paizu.index('p')  # p在字符串中的位置
            eaten = int (paizu[index + 1 : index + 3])  # 需要碰的牌
            if index == 0:  # 碰上家
                if eaten == data[cycle_values(cycle_values(cycle_values(player)))]['最后出牌']:  # 与上家最后一次出牌对比
                    # print(data[cycle_values(cycle_values(cycle_values(player)))]['出牌'] )
                    
                    return paizu 
            elif index == 2:  # 碰对家  
                if eaten == data[cycle_values(cycle_values(player))]['最后出牌']:  # 与对家最后一次出牌对比
                    return paizu 
            elif index == 4:  # 碰下家 
                if eaten == data[cycle_values(player)]['最后出牌']:  # 与下家最后一次出牌对比
                    return paizu 
        elif 'm' in paizu:  # 明杠
            index = paizu.index('m')  # m在字符串中的位置
            eaten = int (paizu[index + 1 : index + 3])  # 需要杠的牌
            if index == 0:  # 杠上家
                if eaten == data[cycle_values(cycle_values(cycle_values(player)))]['最后出牌']:  # 与上家最后一次出牌对比
                    return paizu 
            elif index == 2:  # 杠对家  
                if eaten == data[cycle_values(cycle_values(player))]['最后出牌']:  # 与对家最后一次出牌对比
                    return paizu 
            elif index == 6:  # 杠下家 
                if eaten == data[cycle_values(player)]['最后出牌']:  # 与下家最后一次出牌对比
                    return paizu 
        elif 'a' in paizu:  # 暗杠
            return paizu
            
        elif 'k' in paizu:  # 加杠
            index_k = paizu.index('k')  # m在字符串中的位置
            eaten_k = int (paizu[index_k + 1 : index_k + 3])  # 需要杠的牌
            FLAG_k = []
            # 检查是否存在相应的碰
            for paizu_2 in data[player]['副露']:
                if 'p' in paizu_2:
                    index_p = paizu_2.index('p')  # m在字符串中的位置
                    eaten_p = int (paizu_2[index_p + 1 : index_p + 3])  # 需要碰的牌
                    if eaten_k == eaten_p:  # 存在则不加杠
                        FLAG_k.append(False)
                    else:  # 不存在则加杠
                        FLAG_k.append(True)
                else:  # 不存在则加杠
                    FLAG_k.append(True)
            if FLAG_k and all(FLAG_k):
                return paizu      
            
            
# 检查被副露 返回被副露的选手
def byexposed(player):
    out_draw = data[player]['出牌'][-1]  # 自家出的牌
    for paizu in data[cycle_values(player)]['副露']:
        # print(data[cycle_values(player)]['副露'])
        eaten = int (re.findall(r'[a-zA-Z](\d{2})', paizu)[0])  # 被副露的牌
        # 检查下家是否要吃
        if 'c' in paizu and out_draw == eaten:
            return cycle_values(player)  # 匹配成功，该牌被下家吃
        # 检查下家是否要碰
        elif 'p' in paizu and out_draw == eaten and paizu[0] == 'p':
            # print(1)
            return cycle_values(player)  # 匹配成功，该牌被下家碰
        # 检查下家是否要杠
        elif 'm' in paizu and out_draw == eaten and paizu[0] == 'm':
            return cycle_values(player)  # 匹配成功，该牌被下家杠
    
    for paizu in data[cycle_values(cycle_values(player))]['副露']:
        eaten = int (re.findall(r'[a-zA-Z](\d{2})', paizu)[0])  # 被副露的牌
        # 检查对家是否要碰
        if 'p' in paizu and out_draw == eaten and paizu[2] == 'p':
            return cycle_values(cycle_values(player))  # 匹配成功，该牌被对家碰
        # 检查对家是否要杠
        elif 'm' in paizu and out_draw == eaten and paizu[2] == 'm':
            return cycle_values(cycle_values(player))  # 匹配成功，该牌被对家杠
    
    for paizu in data[cycle_values(cycle_values(cycle_values(player)))]['副露']:
        eaten = int (re.findall(r'[a-zA-Z](\d{2})', paizu)[0])  # 被副露的牌
        # 检查上家是否要碰
        if 'p' in paizu and out_draw == eaten and paizu[4] == 'p':
            return cycle_values(cycle_values(cycle_values(player)))  # 匹配成功，该牌被上家碰
        # 检查上家是否要杠
        elif 'm' in paizu and out_draw == eaten and paizu[6] == 'm':
            return cycle_values(cycle_values(cycle_values(player)))  # 匹配成功，该牌被上家杠
    

# 删除副露 返回需要从手牌去掉的牌的列表
def Remove_secondary_exposure(paizu) -> list:
    result_string = re.sub(r'[a-zA-Z]\d{2}', '', paizu)
    result_list = [int(result_string[i:i+2]) for i in range(0, len(result_string), 2)]
    if 'a' in paizu:  # 暗杠返回4枚
        return [ result_list[0] for _ in range(4)]
    elif 'k' in paizu:  # 加杠返回1枚
        return [result_list[0]]
    else:
        return result_list
    
    
# 开始牌局
def party(player):
    # pdb.set_trace()
    # 摸牌
    # 每次摸牌都从预设手牌里摸，预设手牌为空，则从预设牌河摸牌，最后从牌山摸牌
    
    # 检查是否副露, 返回副露的牌组/None
    paizu = Inspection_dew(player)
    feel_draw = None
    out_draw = None
    Cut_hand = None
    
    if paizu and 'a' in paizu:  # 暗杠
                # 先从预设手牌摸牌
        if data[player]['预设手牌']:
            feel_draw = random.choice(data[player]['预设手牌'])
            data[player]['预设手牌'].remove(feel_draw)  # 取出
        # 再从预设牌河摸牌
        elif is_r(data[player]['预设牌河对照']):  # 立直前,先从预设手牌摸牌,其次牌山摸牌
            feel_draw = get_draw()
        elif [_ for _ in data[player]['预设牌河'] if 'd' not in str(_)]:  # 检查预设牌河是否还有非模切牌
            # 避免摸到d模切牌
            feel_draw = [_ for _ in data[player]['预设牌河'] if 'd' not in str(_)][0]
            data[player]['预设牌河'].remove(feel_draw)  # 取出
        else:
            # 已无预设,从牌山摸牌
            feel_draw = get_draw()
        data[player]['取牌'].append(feel_draw)  # 先摸牌
        data[player]['手牌'].append(feel_draw)
        data[player]['出牌'].append(paizu)  # 暗杠
        for pai in Remove_secondary_exposure(paizu):  # 清理暗杠后的手牌
            data[player]['手牌'].remove(pai)
        data[player]['副露'].remove(paizu)
        # print(data[player]['预设牌河对照'])
        # print(data[player]['预设牌河'])
        # feel_draw = get_draw()
        return party(player)  # 重新摸牌
    elif paizu and 'k' in paizu:  # 加杠
        # 加杠的牌被开局置入手牌里
                # 先从预设手牌摸牌
        if data[player]['预设手牌']:
            feel_draw = random.choice(data[player]['预设手牌'])
            data[player]['预设手牌'].remove(feel_draw)  # 取出
        # 再从预设牌河摸牌
        elif is_r(data[player]['预设牌河对照']):  # 立直前,先从预设手牌摸牌,其次牌山摸牌
            feel_draw = get_draw()
        elif [_ for _ in data[player]['预设牌河'] if 'd' not in str(_)]:  # 检查预设牌河是否还有非模切牌
            # 避免摸到d模切牌
            feel_draw = [_ for _ in data[player]['预设牌河'] if 'd' not in str(_)][0]
            data[player]['预设牌河'].remove(feel_draw)  # 取出
        else:
            # 已无预设,从牌山摸牌
            feel_draw = get_draw()
        data[player]['取牌'].append(feel_draw)  # 先摸牌
        data[player]['手牌'].append(feel_draw)
        data[player]['出牌'].append(paizu)  # 加杠
        for pai in Remove_secondary_exposure(paizu):  # 清理加杠后的手牌
            data[player]['手牌'].remove(pai)
        data[player]['副露'].remove(paizu)
        return party(player)  # 重新摸牌
    elif paizu and 'm' in paizu:  # 明杠
        data[player]['取牌'].append(paizu)  # 明杠取牌区显示
        for pai in Remove_secondary_exposure(paizu):  # 清理明杠后的手牌
            data[player]['手牌'].remove(pai)
        data[player]['副露'].remove(paizu)
        return party(player)  # 重新摸牌
    elif paizu:  # 吃、碰。 副露不摸牌，从手牌中去掉副露的牌
        for pai in Remove_secondary_exposure(paizu):
            data[player]['手牌'].remove(pai)
        data[player]['副露'].remove(paizu)
        feel_draw = paizu
    elif is_r(data[player]['出牌']):  # 立直后。 需要立直时，先从牌库摸牌，立直后从预设牌河、牌山摸牌
        if data[player]['预设牌河对照']:
            # print(data[player]['预设牌河对照'])
            # print(data[player]['预设牌河'])
            out_draw = data[player]['预设牌河对照'][0]
            data[player]['预设牌河对照'].remove(out_draw)  # 删除选中的值
            # print(data[player]['预设手牌'])
            # print(data[player]['手牌'])
            # pdb.set_trace()
            # if out_draw in data[player]['预设牌河']:
            try:
                data[player]['预设牌河'].remove(out_draw)  # 取出
            except:
                pdb.set_trace()
            out_draw = extract_number(out_draw)  # 确定模切该牌
            feel_draw = out_draw
        else:  # 预设牌河对照已打完，从牌山摸牌
            feel_draw = get_draw()
            out_draw = feel_draw
    else:
        # 获取本轮出牌，辨别手摸切
        if data[player]['预设牌河对照']:
            out_draw = data[player]['预设牌河对照'][0]
            data[player]['预设牌河对照'].remove(out_draw)  # 删除选中的值
            if 'd' in str(out_draw):  # 模切 先从预设牌河摸到该牌
                # print(out_draw)
                if 'dr' in out_draw: 
                    data[player]['预设牌河'].remove(out_draw)  # 取出
                    # feel_draw = extract_number(out_draw)  # 确定模切该牌
                    feel_draw = out_draw
                else:
                    data[player]['预设牌河'].remove(out_draw)  # 取出
                    out_draw = extract_number(out_draw)  # 确定模切该牌
                    feel_draw = out_draw
            else:
                # 手切，从手牌里选择对应的牌打出
                Cut_hand = True
                # 先从预设手牌摸牌
                if data[player]['预设手牌']:
                    feel_draw = random.choice(data[player]['预设手牌'])
                    data[player]['预设手牌'].remove(feel_draw)  # 取出
                # 再从预设牌河摸牌
                elif is_r(data[player]['预设牌河对照']):  # 立直前,先从预设手牌摸牌,其次牌山摸牌
                    feel_draw = get_draw()
                elif [_ for _ in data[player]['预设牌河'] if 'd' not in str(_)]:  # 检查预设牌河是否还有非模切牌
                    # 避免摸到d模切牌
                    feel_draw = [_ for _ in data[player]['预设牌河'] if 'd' not in str(_)][0]
                    data[player]['预设牌河'].remove(feel_draw)  # 取出
                else:
                    # 已无预设,从牌山摸牌
                    feel_draw = get_draw()
                out_draw = out_draw  # 确定手切的牌
        else:  # 预设牌河对照已打完，从牌山摸牌
            # 先从预设手牌摸牌
            if data[player]['预设手牌']:
                feel_draw = random.choice(data[player]['预设手牌'])
                data[player]['预设手牌'].remove(feel_draw)  # 取出
            # 再从预设牌河摸牌
            elif [_ for _ in data[player]['预设牌河'] if  'd' not in str(_)]:  # 检查预设牌河是否还有非模切牌
                # 避免摸到d模切牌
                feel_draw = [_ for _ in data[player]['预设牌河'] if  'd' not in str(_)][0]
                data[player]['预设牌河'].remove(feel_draw)  # 取出
            else:
                # 已无预设,从牌山摸牌
                feel_draw = get_draw()
        
    # 记录取牌    
    data[player]['取牌'].append(feel_draw)
    # 副露不摸牌，不放入手牌
    if not paizu: data[player]['手牌'].append(feel_draw)  # 摸到的牌加入手牌
    
    # 出牌
    # 副露后或预设打完后的出牌选择
    if not out_draw: 
        if data[player]['预设牌河对照']:
            out_draw = data[player]['预设牌河对照'][0]
            data[player]['预设牌河对照'].remove(out_draw)  # 删除选中的值
        # 其次再从 手牌 - 预设手牌对照 里选择
        elif list(set(data[player]['手牌']) - set(data[player]['预设手牌对照'])):
            out_draw =  random.choice(list(set(data[player]['手牌']) - set(data[player]['预设手牌对照'])))
        else: 
            # 最后模切
            if str(feel_draw).isdigit():
                out_draw = feel_draw
            else:
                out_draw = random.choice(data[player]['手牌'])
    
    # 记录出牌 
    if 'dr' in str(out_draw) :
        data[player]['出牌'].append('r60')
    elif feel_draw == out_draw and not Cut_hand:
        data[player]['出牌'].append(60)
    else:
        data[player]['出牌'].append(out_draw)
    data[player]['最后出牌'] = out_draw
    # pdb.set_trace()
    # print(out_draw)
    # print(data[player]['手牌'])
    # 打出的牌从手牌删除
    try:
        
        data[player]['手牌'].remove(out_draw)  # 删除选中的值
    except:
        # data[player]['手牌'].remove(extract_number(out_draw))
        pdb.set_trace()
        
    
    # 检查出牌是否为其他家副露，返回副露家选手/None
    Flag2 = byexposed(player)
    
    # 切换选手
    if Flag2:
        player = Flag2
    else:
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


# 解析牌代码
def mahjong_to_number(mahjong_string):
    suit_mapping = {'m': 10, 'p': 20, 's': 30, 'z': 40}
    if len(mahjong_string) == 2:  # 普通1p
        number = int(mahjong_string[0])
    elif len(mahjong_string) == 3 :  # r1p,d1p
        number = int(mahjong_string[1])
    elif len(mahjong_string) == 4 :  # dr1p
        number = int(mahjong_string[2])
    suit = suit_mapping[mahjong_string[-1]]
    if number == 0:
        if suit == 10 : return 51
        if suit == 20 : return 52
        if suit == 30 : return 53
    if len(mahjong_string) == 2:
        return number + suit  # 返回int 21
    elif len(mahjong_string) == 3: 
        return mahjong_string[0] + str(number + suit)  # 返回str r21 d21
    elif len(mahjong_string) == 4: 
        return mahjong_string[0:2] + str(number + suit)  # 返回str dr21
        

# 解析手牌、牌河代码，输入“123m”, 返回['11','12','13']
def string_to_mahjong_list(mahjong_string):
    # print(mahjong_string)
    result = []
    L =  re.findall(r'd?r?\d+[mpsz]', mahjong_string)
    # print(L)
    for LL in L: 
        current_mahjong = LL[-1]
        r = ''  # 保留立直标记r,模切标志d
        for char in LL[:-1]:
            if char.isdigit():
                result.append(r + char + current_mahjong)
            else: 
                # print("y")
                r += char  # 保留立直标记r,模切标志d
    # print(result)
    converted_numbers = [mahjong_to_number(mj) for mj in result]
    return converted_numbers


# 解析副露牌代码，输入“吃213m”, 返回"c121113"
def string_to_mahjong_Secondary_list(mahjong_string):
    d = {'吃': 'c', '碰': 'p', '杠': 'm', '暗': 'a', '加': 'k'}
    result = []
    for paizu in mahjong_string.split(' '):
        if not paizu: continue
        current_mahjong = ''
        if 'm' in paizu: current_mahjong = 'm'
        elif 'p' in paizu: current_mahjong = 'p'
        elif 's' in paizu: current_mahjong = 's'
        elif 'z' in paizu: current_mahjong = 'z'
        paizu_new = ''
        for char in paizu :
            if char.isdigit():
                paizu_new += str(mahjong_to_number(char + current_mahjong))
            elif char in 'mpsz':
                ...
            else:
                paizu_new += d[char]
        result.append(paizu_new)        
    return result


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
    data[master]['副露'] = copy.deepcopy(string_to_mahjong_Secondary_list(assign['东家']['副露']))
    
    data[cycle_values(master)]['点数'] = copy.deepcopy(assign['南家']['点数'])
    data[cycle_values(master)]['预设手牌'] = copy.deepcopy(string_to_mahjong_list(assign['南家']['手牌']))
    data[cycle_values(master)]['预设牌河'] = copy.deepcopy(string_to_mahjong_list(assign['南家']['牌河']))
    data[cycle_values(master)]['预设手牌对照'] = copy.deepcopy(data[cycle_values(master)]['预设手牌'])
    data[cycle_values(master)]['预设牌河对照'] = copy.deepcopy(data[cycle_values(master)]['预设牌河'])
    data[cycle_values(master)]['副露'] = copy.deepcopy(string_to_mahjong_Secondary_list(assign['南家']['副露']))
    
    data[cycle_values(cycle_values(master))]['点数'] = copy.deepcopy(assign['西家']['点数'])
    data[cycle_values(cycle_values(master))]['预设手牌'] = copy.deepcopy(string_to_mahjong_list(assign['西家']['手牌']))
    data[cycle_values(cycle_values(master))]['预设牌河'] = copy.deepcopy(string_to_mahjong_list(assign['西家']['牌河']))
    data[cycle_values(cycle_values(master))]['预设手牌对照'] = copy.deepcopy(data[cycle_values(cycle_values(master))]['预设手牌'])
    data[cycle_values(cycle_values(master))]['预设牌河对照'] = copy.deepcopy(data[cycle_values(cycle_values(master))]['预设牌河'])
    data[cycle_values(cycle_values(master))]['副露'] = copy.deepcopy(string_to_mahjong_Secondary_list(assign['西家']['副露']))
    
    data[cycle_values(cycle_values(cycle_values(master)))]['点数'] = copy.deepcopy(assign['北家']['点数'])
    data[cycle_values(cycle_values(cycle_values(master)))]['预设手牌'] = copy.deepcopy(string_to_mahjong_list(assign['北家']['手牌']))
    data[cycle_values(cycle_values(cycle_values(master)))]['预设牌河'] = copy.deepcopy(string_to_mahjong_list(assign['北家']['牌河']))
    data[cycle_values(cycle_values(cycle_values(master)))]['预设手牌对照'] = copy.deepcopy(data[cycle_values(cycle_values(cycle_values(master)))]['预设手牌'])
    data[cycle_values(cycle_values(cycle_values(master)))]['预设牌河对照'] = copy.deepcopy(data[cycle_values(cycle_values(cycle_values(master)))]['预设牌河'])
    data[cycle_values(cycle_values(cycle_values(master)))]['副露'] = copy.deepcopy(string_to_mahjong_Secondary_list(assign['北家']['副露']))


# 输入“r21”，返回int 21
def extract_number(input_string):
    # 使用isdigit检查字符串是否由数字组成
    if isinstance(input_string, (int, float)):
        return input_string
    if 'r' in input_string and 'd' in input_string:  # '模切立直r的判断
        input_string = input_string[1:]
        number_part = ''.join(char for char in input_string if char.isdigit())  # 将提取到的数字部分转换为整数
        return int(number_part)
    elif 'r' in input_string or 'd' in input_string:  # '立直r的判断' 模切的判断
        number_part = ''.join(char for char in input_string if char.isdigit())  # 将提取到的数字部分转换为整数
        return int(number_part)
    else:
        return input_string


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
            # print(p)
            cards.remove(extract_number(p))
        # 从牌山取出预设牌河
        for p in data[player]['预设牌河']:
            # print(p)
            cards.remove(extract_number(p))
        # 从牌山中取出需要副露的牌
        for paizu in data[player]['副露']:
            for pai in Remove_secondary_exposure(paizu):
                # print(data[player]['副露'])
                # print(pai)
                cards.remove(pai)
    for player in data.keys():
        # 先将需要副露的牌置入配牌
        for paizu in data[player]['副露']:
            for pai in Remove_secondary_exposure(paizu):
                data[player]['配牌'].append(pai)
        if is_r(data[player]['预设牌河对照']):  # 判断预设牌河里是否有立直
            # print(1)
            # 计数巡目，从预设牌河中取 立直巡目 枚,加入配牌
            # 不包含模切牌的预设牌河
            # print(data[player]['预设牌河'])
            p_list = [_ for _ in data[player]['预设牌河'] if  'd' not in str(_)]
            # print(p_list)
            # print(p_list)
            # if data[player]['预设手牌对照']:
            #     number = is_r(data[player]['预设牌河对照'])[0]+1
            # else:
            #     number = is_r(data[player]['预设牌河对照'])[0]
            number = is_r(data[player]['预设牌河对照'])[0]
            for index  in range( number):
                # print(2)
                if index > len(p_list) -1 :
                    break
                p =  p_list[index]
                data[player]['配牌'].append(p)
                # print(p)
                # print( data[player]['预设牌河'])
                data[player]['预设牌河'].remove(p)  # 取出
            print(data[player]['配牌'])
            # 计数巡目，从预设手牌中取  13 - 立直巡目 - 副露占用枚,置入配牌
            for _ in range(13 - len(data[player]['配牌'])):
                # print(3)
                if not data[player]['预设手牌']:
                    break
                p =  random.choice(data[player]['预设手牌'])
                data[player]['配牌'].append(p)
                data[player]['预设手牌'].remove(p)  # 取出
            print(data[player]['配牌'])
        elif True:
            # 计数巡目，从预设手牌中取  13 - 巡目（预设牌河）-副露占用 枚,置入配牌
            for _ in range(13 - len(data[player]['预设牌河']) - len(data[player]['配牌'])):
                if not data[player]['预设手牌']:
                    break
                p =  random.choice(data[player]['预设手牌'])
                data[player]['配牌'].append(p)
                data[player]['预设手牌'].remove(p)  # 取出
            # 计数巡目，从预设牌河中取  13 - 配牌 枚
            # 不包含模切牌的预设牌河
            p_list = [_ for _ in data[player]['预设牌河'] if  'd' not in str(_)]
            p_number = 13 - len(data[player]['配牌']) - len(p_list) 
            for index in range(13 - len(data[player]['配牌'])):
                if index > len(p_list) -1 :
                    break
                p =  p_list[index]
                data[player]['配牌'].append(p)
                data[player]['预设牌河'].remove(p)  # 取出
            # 从预设手牌置入 缺少的模切 枚配牌
            for _ in range(p_number):
                if not data[player]['预设手牌']:
                    break
                p =  random.choice(data[player]['预设手牌'])
                data[player]['配牌'].append(p)
                data[player]['预设手牌'].remove(p)  # 取出
                
        # 从牌山随机取出 剩余手牌
        for _ in range(13 - len(data[player]['配牌'])):
            data[player]['配牌'].append(get_draw())
        data[player]['手牌'] = copy.deepcopy(data[player]['配牌'])
        # print(data[player]['手牌'])

        
if __name__ == "__main__":
    # 生成1副牌
    cards = get_cards()
    # 创建data
    data = {
        "Aさん": {'点数': None, '配牌': [], '手牌': [], '副露': [], '取牌': [], '出牌': [], '预设手牌': [], '预设牌河': [], '预设手牌对照': [], '预设牌河对照': [], '最后出牌': None},
        "Bさん": {'点数': None, '配牌': [], '手牌': [], '副露': [], '取牌': [], '出牌': [], '预设手牌': [], '预设牌河': [], '预设手牌对照': [], '预设牌河对照': [], '最后出牌': None},
        "Cさん": {'点数': None, '配牌': [], '手牌': [], '副露': [], '取牌': [], '出牌': [], '预设手牌': [], '预设牌河': [], '预设手牌对照': [], '预设牌河对照': [], '最后出牌': None},
        "Dさん": {'点数': None, '配牌': [], '手牌': [], '副露': [], '取牌': [], '出牌': [], '预设手牌': [], '预设牌河': [], '预设手牌对照': [], '预设牌河对照': [], '最后出牌': None},
    }
    get_data()  # 填充data
    
    # 生成天凤log
    Tenhou_log = {
        "title": ["玉の間四人南","Sat, 13 Jan 2024 13:52:48 GMT"],
        "name": list(data.keys()),  # 名称顺序 东，南，西，北
        "rule": {"disp":"玉の間四人南","aka53":1,"aka52":1,"aka51":1},
        "log": [[
            [parse_round(assign['场局次']), assign['本场数'], assign['场供']],  # 场次
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



