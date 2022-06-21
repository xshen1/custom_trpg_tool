from itertools import count
import random
from card import Card
import math


class battle_calculator:
    def __init__(self):
        self.character_list = {}
        self.init_round = {}
        self.init_cap = 0
        self.card_full = {}
        self.logs = []

    def add_card(self, name, card):
        # 添加角色/npc/怪物
        self.character_list[name] = card
        card.set_health()
        self.init_round[name] = 0

    def remove_card(self, name):
        # 移除角色/npc/怪物
        card = self.character_list.pop(name)
        return self.character_list, card

    def sort_status(self, list_healths):
        return sorted(list_healths, key=lambda healths: healths["行动值"], reverse=True)

    def display_battle_status(self):
        # 显示现在的hp,行动值
        list_status = []
        for name, card in self.character_list.items():
            card_status = {
                "名字": name,
                "行动值": self.init_round[name],
                "hp": card.hp,
                "max_health": card.max_health
            }
            list_status.append(card_status)
        return self.sort_status(list_status)

    def reset_status(self):
        # 重置轮盘
        list_status = []
        for name, card in self.character_list.items():
            self.init_round[name] = 0
            card.hp = card.max_health
            card_status = {
                "名字": name,
                "行动值": self.init_round[name],
                "hp": card.hp,
                "max_health": card.max_health
            }
            list_status.append(card_status)
        return self.sort_status(list_status)

    def start_battle(self):
        # 开始战斗
        fullname = []
        for name, card in self.character_list.items():
            self.init_round[name] = card.initiative_check()
        max_init = max(self.init_round.values())
        digits = len(str(max_init))
        digits = 10**digits if digits else 10
        self.init_cap = math.ceil(max_init/digits)*digits
        if max_init == self.init_cap:
            for name, init in self.init_round.items():
                if init >= max_init:
                    fullname.append(name)
            for name in fullname:
                encoded_value = max_init**2+max_init+random.uniform(1, 99)/100
                self.card_full[name] = encoded_value
        return self.display_battle_status()

    def modify_temp_initiative(self, name, init_charge=None, init_status_effect=None):
        # init_charge 是一次性充能,请输入 int
        # init_status_effect 是多回合的额外充能，请输入(数值,回合数)
        if init_charge:
            self.init_round[name] += init_charge
            if self.init_round[name] >= self.init_cap:
                self.card_full[name] = self.init_round[name] * \
                    self.init_cap + \
                    self.init_round[name]+random.uniform(1, 99)/100
        if init_status_effect:
            self.character_list[name].temp_init_change = init_status_effect

    def set_temp_status(self, name, con=0, strength=0, dex=0, wis=0):
        # init_charge 是一次性充能,请输入 int
        # init_status_effect 是多回合的额外充能，请输入(数值,回合数)
        stat = self.character_list[name].modify_temp_stat(
            {"耐力": con, "敏捷": dex, "力量": strength, "智力": wis})
        current_init = self.character_list[name].initiative_check()
        if current_init > self.init_cap:
            digits = len(str(current_init))-1
            digits = 10**digits if digits else 10
            self.init_cap = math.ceil(current_init/digits)*digits
        return stat

    def determine_next_card(self):
        # 检测谁动
        self.logs.append(str(self.display_battle_status()))
        sorted_name = sorted(self.card_full, reverse=True)
        self.card_full.pop(sorted_name[0])
        name = sorted_name[0]
        self.init_round[name] -= self.init_cap
        init_acmount, init_round = self.character_list[name].temp_init_change
        if init_round > 1:
            self.modify_temp_initiative(
                name, init_status_effect=(init_acmount, init_round-1))
        elif init_round == 1:
            self.modify_temp_initiative(
                name, init_status_effect=(0, 0))
        self.logs.append(name+"的回合.获得一点策略点")
        self.logs.append(str(self.display_battle_status()))
        return name

    def next_charge(self):
        # 进行下次充填,如果有超过最大填充的角色,进行回合
        self.logs.append("下次充填或者回合,开始计算")
        if self.card_full:
            return self.determine_next_card()
        for name, card in self.character_list.items():
            next_charge = self.init_round[name]+card.initiative_check()
            if next_charge >= self.init_cap:
                encoded_value = next_charge*self.init_cap +\
                    self.init_round[name] + random.uniform(1, 99)/100
                self.card_full[name] = encoded_value
            self.init_round[name] = next_charge
        if self.card_full:
            return self.determine_next_card()
        else:
            self.logs.append(str(self.display_battle_status()))

    def display_log(self):
        print("-----------------")
        logs = "\n".join(self.logs)
        print(logs)
        self.logs = []


if __name__ == '__main__':
    stat1 = {"耐力": 4, "敏捷": 4, "力量": 4, "智力": 4}
    stat2 = {"耐力": 5, "敏捷": 5, "力量": 4, "智力": 4}
    stat3 = {"耐力": 4, "敏捷": 6, "力量": 4, "智力": 4}
    test_card1 = Card("测试1", stat1)
    test_card2 = Card("测试2", stat2)
    test_card3 = Card("测试3", stat3, hp_ratio=10)
    battle_ground = battle_calculator()
    battle_ground.add_card("测试1", test_card1)
    battle_ground.add_card("测试2", test_card2)
    battle_ground.add_card("测试3", test_card3)
    print("测试获取战场信息", battle_ground.display_battle_status())
    print("开始战斗")
    status = battle_ground.start_battle()
    print("现在情况:", status)
    print("轮盘上限:", battle_ground.init_cap)
    battle_ground.next_charge()
    battle_ground.display_log()
    battle_ground.set_temp_status("测试3", dex=100)
    print("测试3:", battle_ground.character_list["测试3"].get_current_stat())
    print("测试3:", battle_ground.character_list["测试3"].initiative_check())
    print("轮盘上限:", battle_ground.init_cap)
    battle_ground.next_charge()
    battle_ground.display_log()
    battle_ground.set_temp_status("测试3", dex=0)
    battle_ground.modify_temp_initiative("测试2", init_charge=100)
    battle_ground.next_charge()
    battle_ground.display_log()
    battle_ground.modify_temp_initiative("测试1", init_status_effect=(100, 2))
    battle_ground.next_charge()
    battle_ground.display_log()
    battle_ground.next_charge()
    battle_ground.display_log()
    battle_ground.next_charge()
    battle_ground.display_log()
