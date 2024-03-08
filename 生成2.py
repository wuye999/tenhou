import json,random,re,sys
import pathlib
import copy
from datetime import datetime


def resource_path(relative_path):
    executable_path = sys.argv[0] 
    current_path = pathlib.Path(pathlib.Path(executable_path).resolve()).parents[0]  
    return pathlib.Path('/').joinpath(current_path, relative_path)


def readData(key: str) -> dict:
    path = resource_path(f"{key}.json")
    try:
        if not pathlib.Path(path).exists():
            print(f'数据文件不存在')
            with open(path, 'w',encoding='utf-8') as f:
                ...
            return {}
        with open(path, 'r',encoding='utf-8') as f:
            value = f.read()
        if value:
            return json.loads(value)
        else:
            print(f'数据为空')
            return {}
    except Exception as e:
        print(f'读取数据失败\n{e}')
        return {}


class Parsing_config:
    def __init__(self, assign):
        self.assign = assign
        self.mahjong_to_number_dict = {
            '1m': 11, '2m': 12, '3m': 13, '4m': 14, '5m': 15, '6m': 16, '7m': 17, '8m': 18, '9m': 19,
            '1p': 21, '2p': 22, '3p': 23, '4p': 24, '5p': 25, '6p': 26, '7p': 27, '8p': 28, '9p': 29,
            '1s': 31, '2s': 32, '3s': 33, '4s': 34, '5s': 35, '6s': 36, '7s': 37, '8s': 38, '9s': 39,
            '1z': 41, '2z': 42, '3z': 43, '4z': 44, '5z': 45, '6z': 46, '7z': 47,
            '0m': 51, '0p': 52, '0s': 53, 
        }
        self.number_to_mahjong_dict = {value: key for key, value in self.mahjong_to_number_dict.items()}
        self.assign_start()

    def string_to_mahjong_list(self,paizu):
        strlist = self.string_to_strlist(paizu)
        number_list = [self.mahjong_to_number(pai) for pai in strlist]
        return number_list
    
    def assign_start(self):
        self.assign['朵拉指示牌'] = self.string_to_mahjong_list(self.assign['朵拉指示牌'])
        self.assign['里朵拉指示牌'] = self.string_to_mahjong_list(self.assign['里朵拉指示牌'])
        self.assign['场局次'] = self.parse_round(self.assign['场局次'])
        for master in ['东家', '南家', '西家', '北家']:
            self.assign[master]['手牌'] = self.string_to_mahjong_list(self.assign[master]['手牌'])
            self.assign[master]['牌河'] = self.string_to_mahjong_list(self.assign[master]['牌河'])
            self.assign[master]['副露'] = self.string_to_mahjong_Secondary_list(self.assign[master]['副露'])
        self.hand_paihe_end()
        return self.assign
    
    def mahjong_to_number(self, mahjong_string):
        match len(mahjong_string):
            case 2:  
                number = self.mahjong_to_number_dict[mahjong_string]
                return number
            case 3 :  
                number = self.mahjong_to_number_dict[mahjong_string[1:]]
                return mahjong_string[0] + str(number)
            case 4 :  
                number = self.mahjong_to_number_dict(mahjong_string[2:])
                return mahjong_string[:2] + str(number)

    def string_to_strlist(self, mahjong_string: str):
        result = []
        L =  re.findall(r'd?r?\d+[mpsz]', mahjong_string)
        for LL in L: 
            current_mahjong = LL[-1]
            r = ''  
            for char in LL[:-1]:
                if char.isdigit():
                    result.append(r + char + current_mahjong)
                else: 
                    r += char  
        return result
        
    def string_to_mahjong_Secondary_list(self, mahjong_string):
        d = {'吃': 'c', '碰': 'p', '杠': 'm', '暗': 'a', '加': 'k'}
        result = []
        for paizu in mahjong_string.split(' '):
            if not paizu: continue
            current_mahjong = paizu[-1]
            paizu_new = ''
            for char in paizu :
                if char.isdigit():
                    paizu_new += str(self.mahjong_to_number(char + current_mahjong))
                elif char in 'mpsz':
                    ...
                elif char in '吃碰杠暗加':
                    paizu_new += d[char]
                else:
                    print(f'err: Parsing_config.string_to_mahjong_Secondary_list {char}')
            if 'a' in paizu_new : paizu_new = self.extract_aon(paizu_new)
            elif 'k' in  paizu_new : paizu_new = self.extract_kon(paizu_new)
            elif 'p' in paizu_new or 'm' in paizu_new : paizu_new = self.extract_pon(paizu_new)
            result.append(paizu_new)      
        return result
    
    def extract_pon(self, s):
        pattern = re.compile(r'([a-zA-Z]?\d{2})')
        result_list = pattern.findall(s)  
        index_n = [index for index, elem in enumerate(result_list) if any(char.isalpha() for char in elem)][0]  
        index_p = copy.deepcopy(result_list[index_n])
        result_list.remove(result_list[index_n])  
        result_new = [elem for elem in result_list if elem[0] != '5'] + [elem for elem in result_list if elem[0] == '5']  
        result_new.insert(index_n, index_p)
        substrings = ''.join(result_new)
        return substrings   
    
    def extract_aon(self, paizu_new):   
        if '51' in paizu_new: paizu_new= '151515a51'
        elif '52' in paizu_new: paizu_new= '252525a52'
        elif '53' in paizu_new: paizu_new= '353535a53'  
        return paizu_new
    
    def extract_kon(self, paizu_new):   
        pass 
        return paizu_new
    
    def parse_round(self, words):
        chinese_numerals = {'零': 0, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9}
        if len(words) == 3 and words.endswith("局"):
            direction = words[0]
            round_number_str = words[1:-1]  
            if round_number_str.isdigit():
                round_number = int(round_number_str)
            else:
                try:
                    round_number = int(chinese_numerals[round_number_str])
                except ValueError:
                    return None  
            match direction:
                case "东":
                    return (round_number - 1) % 4
                case "南":
                    return (round_number - 1) % 4 + 4
                case "西":
                    return (round_number - 1) % 4 + 8
                case "北":
                    return (round_number - 1) % 4 + 12
        return None 
    
    def extract_number(self, input_string):
        if isinstance(input_string, (int, float)):
            return input_string
        elif 'r' in input_string or 'd' in input_string:  
            number_part = ''.join(char for char in input_string if char.isdigit())  
            return int(number_part)
        else:
            return input_string
    
    def Remove_secondary_exposure(self, paizu) -> list:
        result_string = re.sub(r'[a-zA-Z]\d{2}', '', paizu)
        result_list = [int(result_string[i:i+2]) for i in range(0, len(result_string), 2)]
        if 'a' in paizu:  
            eaten = int (re.findall(r'[a-zA-Z](\d{2})', paizu)[0])  
            result_list.append(eaten)
            return result_list
        elif 'k' in paizu:  
            return [result_list[0]]
        else:
            return result_list
    
    def hand_paihe_end(self):
        for master in ['东家', '南家', '西家', '北家']:
            if self.assign[master]['手牌']:
                end_shoupai = self.assign[master]['手牌'][-1]
                self.assign[master]['牌河'].append('d' + str(end_shoupai))
        
                
class PaiSon:    
    def __init__(self, PlayerBox_1) -> None:
        self.PlayerBox_1 = PlayerBox_1
        self.cards = self.get_cards()
        self.remove_dorasign()
        self.remove_presuppose()
    
    def get_cards(self):
        cards = []
        cards.extend(list(range(11,20)))  
        cards.extend(list(range(21,30)))  
        cards.extend(list(range(31,40)))  
        cards.extend(list(range(41,48)))  
        cards = cards * 4
        cards.remove(15), cards.remove(25), cards.remove(35)
        cards.append(51), cards.append(52), cards.append(53)  
        return cards
    
    def get_count(self):
        target_sum = 100000
        num1 = random.randint(1, target_sum - 3)
        num2 = random.randint(1, target_sum - num1 - 2)
        num3 = random.randint(1, target_sum - num1 - num2 - 1)
        num4 = target_sum - num1 - num2 - num3
        return [num1, num2, num3, num4]

    def get_draw(self):
        random_value = random.choice(self.cards)  
        self.cards.remove(random_value)  
        return random_value 
    
    def remove_dorasign(self):
        for value in self.PlayerBox_1.assign['朵拉指示牌']:
            self.cards.remove(value) 
        for value in self.PlayerBox_1.assign['里朵拉指示牌']:
            self.cards.remove(value) 
    
    def remove_presuppose(self):
        try:
            for player in self.PlayerBox_1.data.keys():
                for pai in self.PlayerBox_1.data[player]['手牌牌库']:
                    self.cards.remove(self.PlayerBox_1.extract_number(pai))
                for pai in self.PlayerBox_1.data[player]['牌河牌库']:
                    self.cards.remove(self.PlayerBox_1.extract_number(pai))
                for paizu in self.PlayerBox_1.data[player]['副露']:
                    for pai in self.PlayerBox_1.Remove_secondary_exposure(paizu):
                        self.cards.remove(pai)
        except:
            input(f'使用了4枚以上相同的牌，或使用了两枚相同的赤宝牌 {self.PlayerBox_1.number_to_mahjong_dict.get(self.PlayerBox_1.extract_number(pai), pai)}')
            exit(0) 
    
    
class PlayerBox(Parsing_config):
    def __init__(self, Parsing_config_1) -> None:
        self.assign = Parsing_config_1.assign
        self.number_to_mahjong_dict = Parsing_config_1.number_to_mahjong_dict
        self.mahjong_to_number_dict = Parsing_config_1.mahjong_to_number_dict
        self.data = {
            "Aさん": {'点数': None, '配牌': [], '手牌': [], '副露': [], '取牌': [], '出牌': [], '手牌牌库': [], '牌河牌库': [], '预设手牌对照': [], '预设牌河对照': [], '最后出牌': None},
            "Bさん": {'点数': None, '配牌': [], '手牌': [], '副露': [], '取牌': [], '出牌': [], '手牌牌库': [], '牌河牌库': [], '预设手牌对照': [], '预设牌河对照': [], '最后出牌': None},
            "Cさん": {'点数': None, '配牌': [], '手牌': [], '副露': [], '取牌': [], '出牌': [], '手牌牌库': [], '牌河牌库': [], '预设手牌对照': [], '预设牌河对照': [], '最后出牌': None},
            "Dさん": {'点数': None, '配牌': [], '手牌': [], '副露': [], '取牌': [], '出牌': [], '手牌牌库': [], '牌河牌库': [], '预设手牌对照': [], '预设牌河对照': [], '最后出牌': None},
        }
        self.get_data()
    
    def get_data(self):
        masterid = self.assign['场局次'] % 4  
        master = list(self.data.keys())[masterid]  
        for player in ['东家', '南家', '西家', '北家']:
            self.data[master]['点数'] = copy.deepcopy(self.assign[player]['点数'])
            self.data[master]['手牌牌库'] = copy.deepcopy(self.assign[player]['手牌'])
            self.data[master]['牌河牌库'] = copy.deepcopy(self.assign[player]['牌河'])
            self.data[master]['预设手牌对照'] = copy.deepcopy(self.assign[player]['手牌'])
            self.data[master]['预设牌河对照'] = copy.deepcopy(self.assign[player]['牌河'])
            self.data[master]['副露'] = copy.deepcopy(self.assign[player]['副露'])
            master = self.cycle_values(master)
    
    def cycle_values(self,value = "Aさん"):
        values = list(self.data.keys())
        index = values.index(value)
        next_index = (index + 1) % len(values)
        return values[next_index]

    def is_r(self, my_list):
        if 'r' in str(my_list):
            for index, item in enumerate(my_list):
                if isinstance(item, str) and 'r' in item:
                    return [index + 1, item]
        else:
            return False
        
    
class Party:
    def __init__(self, PlayerBox_1, PaiSon_1) -> None:
        self.PlayerBox_1 = PlayerBox_1
        self.PaiSon_1 = PaiSon_1
        self.data = self.PlayerBox_1.data
        self.cards = self.PaiSon_1.cards
        self.assign = self.PlayerBox_1.assign
        self.masterid = self.assign['场局次'] % 4  
        self.master = list(self.data.keys())[self.masterid]  
        self.player = self.master
        
    def end_party(self):
        if len(self.cards) + len(self.assign['朵拉指示牌']) + len(self.assign['里朵拉指示牌']) <= 14 :
            return True
        
    def start(self):
        is_end = self.end_party()
        if is_end: return
        paizu = self.Inspection_dew()
        if paizu:
            self.Secondary_dew(paizu)
            if 'a' in paizu or 'k' in paizu or 'm' in paizu: 
                return self.start()
        if paizu and ('c' in paizu or 'p' in paizu):
            feel_draw = paizu
            out_draw = None
        else:
            feel_draw, out_draw =  self.get_pai()
        self.add_hand(feel_draw, paizu)
        self.Record_feel_card(feel_draw)
        if not out_draw:
            out_draw = self.get_out_draw(feel_draw, out_draw)
        self.remove_hand(out_draw)
        self.Record_out_card(feel_draw, out_draw)
        new_player = self.byexposed()
        if new_player:
            self.player = new_player
        else:
            self.player = self.PlayerBox_1.cycle_values(self.player)
        return self.start()

    def byexposed(self):
        cycle_values = self.PlayerBox_1.cycle_values
        out_draw = self.data[self.player]['最后出牌']  
        for paizu in self.data[cycle_values(self.player)]['副露']:
            eaten = int (re.findall(r'[a-zA-Z](\d{2})', paizu)[0])  
            if 'c' in paizu and out_draw == eaten:
                return cycle_values(self.player)  
            elif 'p' in paizu and out_draw == eaten and paizu[0] == 'p':
                return cycle_values(self.player)  
            elif 'm' in paizu and out_draw == eaten and paizu[0] == 'm':
                return cycle_values(self.player)  
        for paizu in self.data[cycle_values(cycle_values(self.player))]['副露']:
            eaten = int (re.findall(r'[a-zA-Z](\d{2})', paizu)[0])  
            if 'p' in paizu and out_draw == eaten and paizu[2] == 'p':
                return cycle_values(cycle_values(self.player))  
            elif 'm' in paizu and out_draw == eaten and paizu[2] == 'm':
                return cycle_values(cycle_values(self.player))  
        for paizu in self.data[cycle_values(cycle_values(cycle_values(self.player)))]['副露']:
            eaten = int (re.findall(r'[a-zA-Z](\d{2})', paizu)[0])  
            if 'p' in paizu and out_draw == eaten and paizu[4] == 'p':
                return cycle_values(cycle_values(cycle_values(self.player)))  
            elif 'm' in paizu and out_draw == eaten and paizu[6] == 'm':
                return cycle_values(cycle_values(cycle_values(self.player)))  

    def remove_hand(self, out_draw):
        try:
            self.data[self.player]['手牌'].remove(out_draw)  
        except:
            input(f'副露或立直后手切 {self.PlayerBox_1.number_to_mahjong_dict.get(self.PlayerBox_1.extract_number(out_draw), out_draw)}')
            exit(0)  

    def add_hand(self, feel_draw, paizu):
        if not paizu: self.data[self.player]['手牌'].append(feel_draw)  

    def get_out_draw(self, feel_draw, out_draw):
        if list(set(self.data[self.player]['手牌']) - set(self.data[self.player]['预设手牌对照'])):
            out_draw =  random.choice(list(set(self.data[self.player]['手牌']) - set(self.data[self.player]['预设手牌对照'])))
        else: 
            out_draw = feel_draw
        return out_draw

    def Record_out_card(self, feel_draw, out_draw):
        if feel_draw == out_draw and not self.data[self.player]['预设牌河对照']:
            self.data[self.player]['出牌'].append(60)
        else:
            self.data[self.player]['出牌'].append(out_draw)
        self.data[self.player]['最后出牌'] = self.PlayerBox_1.extract_number(out_draw)
    
    def Record_feel_card(self, feel_draw):
        self.data[self.player]['取牌'].append(feel_draw)
        
    def Secondary_dew(self, paizu):
        feel_draw = None
        if 'a' in paizu or 'k' in paizu:  
            feel_draw = self.get_fulu_pai()
            self.data[self.player]['取牌'].append(feel_draw)  
            self.data[self.player]['手牌'].append(feel_draw)
            self.data[self.player]['出牌'].append(paizu)  
            for pai in self.PlayerBox_1.Remove_secondary_exposure(paizu):  
                self.data[self.player]['手牌'].remove(pai)
            self.data[self.player]['副露'].remove(paizu)
            return None  
        elif 'm' in paizu:  
            self.data[self.player]['取牌'].append(paizu)  
            for pai in self.PlayerBox_1.Remove_secondary_exposure(paizu):  
                self.data[self.player]['手牌'].remove(pai)
            self.data[self.player]['副露'].remove(paizu)
            self.data[self.player]['出牌'].append(0)
            return None  
        elif paizu:  
            for pai in self.PlayerBox_1.Remove_secondary_exposure(paizu):
                self.data[self.player]['手牌'].remove(pai)
            self.data[self.player]['副露'].remove(paizu)
            feel_draw = paizu
            return feel_draw
            
    def get_pai(self):
        out_draw = None
        if self.data[self.player]['预设牌河对照']:
            out_draw = self.data[self.player]['预设牌河对照'][0]
            self.data[self.player]['预设牌河对照'].remove(out_draw)  
        if 'd' in str(out_draw):
            feel_draw = self.die_cut(out_draw)
        else:
            feel_draw = self.get_fulu_pai()
        return feel_draw, out_draw
    
    
    def get_fulu_pai(self):
        if self.Inspect_Not_Rlchi_d_paihe() and not self.PlayerBox_1.is_r(self.data[self.player]['预设牌河对照']):
            feel_draw = self.Not_Rlchi_d_paihe()
        elif self.Inspect_Rlchi_d_paihe() and self.PlayerBox_1.is_r(self.data[self.player]['预设牌河对照']):
            feel_draw = self.Rlchi_d_paihe()
        elif self.data[self.player]['手牌牌库']:
            feel_draw = self.Han_card_library()
        else:
            feel_draw = self.PaiSon_1.get_draw()
        return feel_draw  
     
    def Han_card_library(self):
        feel_draw = random.choice(self.data[self.player]['手牌牌库'])
        self.data[self.player]['手牌牌库'].remove(feel_draw)  
        return feel_draw
    
    def die_cut(self, out_draw):
        self.data[self.player]['牌河牌库'].remove(out_draw)  
        feel_draw = out_draw  
        return feel_draw

    def Inspect_Not_Rlchi_d_paihe(self):
        paihe = self.data[self.player]['牌河牌库']
        paihe_nod = [pai for pai in paihe if 'd' not in str(pai)]
        if paihe_nod:
            return paihe_nod[0]
        else:
            return None
    
    def Inspect_Rlchi_d_paihe(self):
        richi_bout = self.PlayerBox_1.is_r(self.data[self.player]['牌河牌库'])  
        if richi_bout:
            richi_bout = richi_bout[0]
            Lichi_front_paihe = self.data[self.player]['牌河牌库'][:richi_bout-1]
            Lichi_front_paihe_nod = [pai for pai in Lichi_front_paihe if 'd' not in str(pai)]
            return Lichi_front_paihe_nod[0]
        else:
            return None
        
    def Not_Rlchi_d_paihe(self):
        paihe = self.data[self.player]['牌河牌库']
        paihe_nod = [pai for pai in paihe if 'd' not in str(pai)]
        if paihe_nod:
            feel_draw = paihe_nod[0]
            self.data[self.player]['牌河牌库'].remove(feel_draw)
            return feel_draw
        else:
            return None
    
    def Rlchi_d_paihe(self):
        richi_bout = self.PlayerBox_1.is_r(self.data[self.player]['牌河牌库'])  
        if richi_bout:
            richi_bout = richi_bout[0]
            Lichi_front_paihe = self.data[self.player]['牌河牌库'][:richi_bout-1]
            Lichi_front_paihe_nod = [pai for pai in Lichi_front_paihe if 'd' not in str(pai)]
            feel_draw = Lichi_front_paihe_nod[0]
            self.data[self.player]['牌河牌库'].remove(feel_draw)
            return feel_draw
        else:
            return None
    
    def Inspection_dew(self):
        cycle_values = self.PlayerBox_1.cycle_values
        for paizu in self.data[self.player]['副露']:
            if 'c' in paizu:  
                eaten = int (paizu[1:3])  
                if eaten == self.data[cycle_values(cycle_values(cycle_values(self.player)))]['最后出牌']:  
                    return paizu
            elif 'p' in paizu:  
                index = paizu.index('p')  
                eaten = int (paizu[index + 1 : index + 3])  
                match index:
                    case 0:  
                        if eaten == self.data[cycle_values(cycle_values(cycle_values(self.player)))]['最后出牌']:  
                            return paizu 
                    case 2:  
                        if eaten == self.data[cycle_values(cycle_values(self.player))]['最后出牌']:  
                            return paizu 
                    case 4:  
                        if eaten == self.data[cycle_values(self.player)]['最后出牌']:  
                            return paizu 
            elif 'm' in paizu:  
                index = paizu.index('m')  
                eaten = int (paizu[index + 1 : index + 3])  
                match index:
                    case 0:
                        if eaten == self.data[cycle_values(cycle_values(cycle_values(self.player)))]['最后出牌']:  
                            return paizu 
                    case 2:  
                        if eaten == self.data[cycle_values(cycle_values(self.player))]['最后出牌']:  
                            return paizu 
                    case 6:  
                        if eaten == self.data[cycle_values(self.player)]['最后出牌']:  
                            return paizu 
            elif 'a' in paizu:  
                return paizu
            elif 'k' in paizu:  
                index_k = paizu.index('k')  
                eaten_k = int (paizu[index_k + 1 : index_k + 3])  
                FLAG_k = []
                for paizu_2 in self.data[self.player]['副露']:
                    if 'p' in paizu_2:
                        index_p = paizu_2.index('p')  
                        eaten_p = int (paizu_2[index_p + 1 : index_p + 3])  
                        if eaten_k == eaten_p:  
                            FLAG_k.append(False)
                        else:  
                            FLAG_k.append(True)
                    else:  
                        FLAG_k.append(True)
                if FLAG_k and all(FLAG_k):
                    return paizu   
 

class Licensing:
    def __init__(self, PlayerBox_1, PaiSon_1) -> None:
        self.PlayerBox_1 = PlayerBox_1
        self.PaiSon_1 = PaiSon_1
        self.data = self.PlayerBox_1.data
        self.assign = self.PlayerBox_1.assign
        self.all_formulate()
    
    def all_formulate(self):
        for player in self.data.keys():
            self.formulate(player)
            self.set_hand_pai(player)
    
    def formulate(self, player):
        if self.PlayerBox_1.is_r(self.data[player]['预设牌河对照']):
            Lichi_front_paihe_nod, frontLichi_paihe_d, richi_bout = self.get_frontLichi_paihe(player)
            paihe_nod, paihe_d = Lichi_front_paihe_nod, frontLichi_paihe_d
        else:
            paihe_nod, paihe_d, bout = self.get_paihe(player)
        self.place(player)
        place_number = len(self.data[player]['配牌'])
        for i in range(13 - place_number):
            if paihe_nod:
                pai = paihe_nod[0] 
                paihe_nod.remove(pai)  
                self.data[player]['牌河牌库'].remove(pai)  
                self.data[player]['配牌'].append(pai)
            else:
                break
        place_number = len(self.data[player]['配牌'])
        for i in range(13 - place_number):
            if self.data[player]['手牌牌库']:
                pai = random.choice(self.data[player]['手牌牌库'])
                self.data[player]['手牌牌库'].remove(pai)  
                self.data[player]['配牌'].append(pai)
            else:
                break
        place_number = len(self.data[player]['配牌'])
        for i in range(13 - place_number):
            pai = self.PaiSon_1.get_draw()
            self.data[player]['配牌'].append(pai)
    
    def set_hand_pai(self, player):
        self.data[player]['手牌'] = copy.deepcopy(self.data[player]['配牌'])
    
    def get_frontLichi_paihe(self, player):
        richi_bout = self.PlayerBox_1.is_r(self.data[player]['预设牌河对照'])[0]  
        Lichi_front_paihe = self.data[player]['预设牌河对照'][:richi_bout-1]
        Lichi_front_paihe_nod = [pai for pai in Lichi_front_paihe if 'd' not in str(pai)]
        frontLichi_paihe_d = [pai for pai in Lichi_front_paihe if 'd' in str(pai)]
        return Lichi_front_paihe_nod, frontLichi_paihe_d, richi_bout
    
    def get_paihe(self, player):
        paihe = self.data[player]['预设牌河对照']
        paihe_nod = [pai for pai in paihe if 'd' not in str(pai)]
        paihe_d = [pai for pai in paihe if 'd' in str(pai)]
        return paihe_nod, paihe_d, len(paihe)
    
    def place(self, player):
        for paizu in self.data[player]['副露']:
            for pai in self.PlayerBox_1.Remove_secondary_exposure(paizu):
                self.data[player]['配牌'].append(pai)
            
    
class TenhouLog:
    def __init__(self, PlayerBox_1) -> None:
        self.PlayerBox_1 = PlayerBox_1
        self.data = self.PlayerBox_1.data
        self.assign = self.PlayerBox_1.assign
        self.log = {
        "title": ["玉の間四人南",self.format_time()],
        "name": list(self.data.keys()),  
        "rule": {"disp":"玉の間四人南","aka53":1,"aka52":1,"aka51":1},
        "log": [[
            [self.assign['场局次'], self.assign['本场数'], self.assign['场供']],  
            [self.data[player]['点数'] for player in self.data.keys()],  
            self.assign['朵拉指示牌'],  
            self.assign['里朵拉指示牌'],  
            ]]
        }
    
    def format_time(self):
        now = datetime.utcnow()
        formatted_time = now.strftime("%a, %d %b %Y %H:%M:%S GMT")
        return formatted_time
        
    def start(self):
        self.set_log()
        self.save_log()
        
    def set_log(self):
        for player in self.data.keys():
            self.PlayerBox_1.extract_number
            self.log['log'][0].append([self.PlayerBox_1.extract_number(c) for c in self.data[player]['配牌']])
            self.log['log'][0].append([self.PlayerBox_1.extract_number(c) for c in self.data[player]['取牌']])
            self.log['log'][0].append([self.formatting_chupai(c) for c in self.data[player]['出牌']])
        self.log['log'][0].append(["全員聴牌"])
        
    def formatting_chupai(self, pai):
        if isinstance(pai, int):
            return pai
        elif 'dr' in pai :
            return 'r60'
        elif 'd' in pai:
            return 60
        elif 'r' in pai:
            return pai
        else:
            return pai
    
    def save_log(self):
        with open("tenhou_log.txt", "w", encoding='utf-8') as file:
            file.write("https://tenhou.net/6/#json=" + json.dumps(self.log, ensure_ascii=False) )
        
        
if __name__ == "__main__":
    assign =  readData('配置')
    Parsing_config_1 = Parsing_config(assign)
    PlayerBox_1 = PlayerBox(Parsing_config_1)
    PaiSon_1 = PaiSon(PlayerBox_1)
    Licensing_1 = Licensing(PlayerBox_1, PaiSon_1)
    Party_1 = Party(PlayerBox_1, PaiSon_1)
    Party_1.start()
    TenhouLog_1= TenhouLog(PlayerBox_1)
    TenhouLog_1.start()
    print("生成牌谱成功。")
    input('按回车关闭')
