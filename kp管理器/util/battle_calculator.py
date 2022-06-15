from card import Card
import math


class battle_calculatorß:
    def __init__(self):
        self.character_list = {}
        self.init_round = {}
        self.init_cap = 0

    def add_card(self, name, card):
        self.character_list[name] = card
        self.init_round[name] = 0

    def remove_card(self, name):
        card = self.character_list.pop(name)
        return self.character_list, card

    def sort_status(self, list_healths):
        return sorted(list_healths, key=lambda healths: healths["initiative"], reverse=True)

    def display_battle_status(self):
        list_status = []
        for card in self.character_list:
            name = card.name
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
        for card in self.character_list:
            name = card.name
            self.init_round[name] = 0
            card.hp = card.max_health
            card_status = {
                "name": name,
                "initiative": self.init_round[name],
                "hp": card.hp,
                "max_health": card.max_health
            }
        return self.sort_status(list_status)

    def start_battle(self):
        for card in self.character_list:
            self.init_round[card.name] = card.initiative_check()
        max_init = max(self.init_round.values)
        self.init_cap = math.ceil(max_init/10)*10
        return self.display_battle_status()


if __name__ == '__main__':
