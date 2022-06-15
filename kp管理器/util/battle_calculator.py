from card import Card
import math


class battle_calculator:
    def __init__(self):
        self.character_list = {}
        self.init_round = {}
        self.init_cap = 0

    def add_card(self, name, card):
        self.character_list[name] = card
        card.set_health()
        self.init_round[name] = 0

    def remove_card(self, name):
        card = self.character_list.pop(name)
        return self.character_list, card

    def sort_status(self, list_healths):
        return sorted(list_healths, key=lambda healths: healths["initiative"], reverse=True)

    def display_battle_status(self):
        list_status = []
        for name, card in self.character_list.items():
            card_status = {
                "name": name,
                "initiative": self.init_round[name],
                "hp": card.hp,
                "max_health": card.max_health
            }
            list_status.append(card_status)
        return self.sort_status(list_status)

    def reset_status(self):
        list_status = []
        for name, card in self.character_list.items():
            self.init_round[name] = 0
            card.hp = card.max_health
            card_status = {
                "name": name,
                "initiative": self.init_round[name],
                "hp": card.hp,
                "max_health": card.max_health
            }
            list_status.append(card_status)
        return self.sort_status(list_status)

    def start_battle(self):
        for name, card in self.character_list.items():
            self.init_round[name] = card.initiative_check()
        max_init = max(self.init_round.values())
        self.init_cap = math.ceil(max_init/10)*10
        return self.display_battle_status()


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
    status = battle_ground.start_battle()
    print("现在情况:", status)
    print("轮盘上限:", battle_ground.init_cap)
    test_card3.change_health(-10)
    print("模拟扣血", battle_ground.display_battle_status())
    cur_status = battle_ground.reset_status()
    print("重置战场", cur_status)
