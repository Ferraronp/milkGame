class Game:
    def __init__(self, **kwargs):
        self.money = 20 if 'money' not in kwargs else kwargs['money']
        self.money_level = 0 if 'money_level' not in kwargs else kwargs['money_level']
        self.milk = 0 if 'milk' not in kwargs else kwargs['milk']
        self.milk_level = 0 if 'milk_level' not in kwargs else kwargs['milk_level']
        self.auto_click = 0 if 'auto_click' not in kwargs else kwargs['auto_click']
        self.__milk_levels = [
            {'limit': 0, 'price': 0},
            {'limit': 1, 'price': 10},  # Бутылка с молоком
            {'limit': 2, 'price': 25},  # Нео и арт с молочником
            {'limit': 8, 'price': 90},
            {'limit': 16, 'price': 200},  # Фарадей(ну где то должен быть)
            {'limit': 40, 'price': 600},
            {'limit': 150, 'price': 3500},
            {'limit': 432, 'price': 12000}  # арлабус и его шалкер
        ]
        self.__money_levels = [
            {'cost': 0, 'price': 0},
            {'cost': 0.5, 'price': 10},  # cow
            {'cost': 1, 'price': 30},  # farm
            {'cost': 2, 'price': 150},  # minecraft cow
            {'cost': 2.5, 'price': 500},  # ketrin
            {'cost': 3.5, 'price': 1000},  # колаб с утка(у арта кэт утка и творог)
            {'cost': 5, 'price': 14000}  # колаб с снегом(у арта кэт мороженное)
        ]

    def update(self, seconds: float):
        self.milk_level = min(self.milk_level, len(self.__milk_levels) - 1)
        ras = self.milk + seconds * self.auto_click * 0.1 + 0.2
        self.milk = min(ras, self.__milk_levels[self.milk_level]['limit'])

    def sell_milk(self):
        self.money += self.__money_levels[self.money_level]['cost'] * self.milk * 0.4

    def update_money(self):
        if self.money_level + 1 == len(self.__money_levels):
            return
        if self.money > self.__money_levels[self.money_level + 1]['price']:
            self.money -= self.__money_levels[self.money_level + 1]['price']
            self.money_level += 1

    def update_milk(self):
        if self.milk_level + 1 == len(self.__milk_levels):
            return
        if self.money > self.__milk_levels[self.milk_level + 1]['price']:
            self.money -= self.__milk_levels[self.milk_level + 1]['price']
            self.milk_level += 1

    def update_milk_on_click(self):
        self.milk_level = min(self.milk_level, len(self.__milk_levels) - 1)
        ras = self.milk + 0.15
        self.milk = min(ras, self.__milk_levels[self.milk_level]['limit'])
