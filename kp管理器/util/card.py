from copy import copy


import copy


class Skills:
    def __init__(self, name, points, type):
        self.name = name
        self.points = 10+points
        self.type = type
        # 技能类型包括 生存,突破,探索,辨识

    def modify_points(self, amount):
        self.points += int(amount)

    def dice_roll(self, stat, difficulty=0):
        equation = "+".join([str(self.points), str(stat//2)])
        if difficulty > 0:
            equation = equation+"+"+str(difficulty*10)
        else:
            equation = equation+str(difficulty*10)
        roll_output = ["ra", self.name, equation]
        return " ".join(roll_output)

    def skill_type(self):
        if self.type == "生存":
            return "耐力"
        if self.type == "突破":
            return "力量"
        if self.type == "探索":
            return "敏捷"
        if self.type == "辨识":
            return "智力"


class Card:
    def __init__(self, name, stat, hp_ratio=3):
        self.name = name
        self.base_stat = stat
        self.temp_stat = {"耐力": 0, "敏捷": 0, "力量": 0, "智力": 0}
        self.stat = copy.deepcopy(self.base_stat)
        # 属性包括(耐力,敏捷,力量,智力)
        self.hp_ratio = hp_ratio
        self.temp_init_change = (0, 0)
        self.initiative = self.initiative_check()
        self.skills = {"属性检测": Skills("属性", 0, "属性")}
        # 生存技能为(名字，数值，类型)

    def set_health(self):
        # 设置最大生命值以及现在生命值
        self.max_health = self.stat["耐力"]*self.hp_ratio
        self.hp = self.max_health

    def change_health(self, change_amount):
        # 改变现在生命值
        self.hp += change_amount

    def modify_stat(self, base_stat_change):
        # 改变基础属性
        for key in base_stat_change.keys():
            self.base_stat[key] += base_stat_change[key]
        self.set_health()
        return self.get_current_stat()

    def modify_temp_stat(self, temp_stat_change):
        # 改变基础属性以及临时属性
        self.temp_stat = temp_stat_change
        self.set_health()
        return self.get_current_stat()

    def get_current_stat(self):
        for key in self.stat.keys():
            self.stat[key] = self.base_stat[key] + self.temp_stat[key]
        return self.stat

    def initiative_check(self):
        change, round = self.temp_init_change
        return (self.stat["智力"]+self.stat["敏捷"])//2 + change

    def change_skills(self, skill_name, points, type):
        if skill_name in self.skills:
            self.skills[skill_name].modify_points(points)
        else:
            self.skills[skill_name] = Skills(skill_name, points, type)
        return self.skills[skill_name]

    def skill_check(self, skill_name, stat, difficulty=0):
        skill = self.skills.get(skill_name, self.skills["属性检测"])
        return skill.dice_roll(self.stat[stat], difficulty)


if __name__ == '__main__':
    stat = {"耐力": 4, "敏捷": 4, "力量": 4, "智力": 4}
    test_card = Card("测试", stat)
    print("测试获取现有属性", test_card.get_current_stat())
    current = test_card.modify_stat(base_stat_change={"耐力": 1})
    print("测试修改属性", current)
    print("测试行动", test_card.initiative_check())
    current = test_card.modify_stat(temp_stat_change={"力量": 1, "智力": 2})
    current = test_card.clear_temp_stat()
    print("测试清除临时属性", test_card.get_current_stat())
    print("测试行动", test_card.initiative_check())
    print("测试技能", test_card.skill_check("攀爬", "敏捷", 1))
    test_skills = test_card.change_skills("攀爬", 30, "探索")
    print("创建技能 攀爬 30 探索")
    print("测试技能", test_card.skill_check("攀爬", "敏捷", 1))
    test_card.hp_ratio = 5
    test_card.set_health()
    print("hp", test_card.hp)
