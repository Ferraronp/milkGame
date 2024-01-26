class Game:
    def __init__(self, **kwargs):
        self.money = 20.0 if 'money' not in kwargs else float(kwargs['money'])
        self.money_level = 0 if 'money_level' not in kwargs else int(kwargs['money_level'])
        self.milk = 0.0 if 'milk' not in kwargs else float(kwargs['milk'])
        self.milk_level = 0 if 'milk_level' not in kwargs else int(kwargs['milk_level'])
        self.auto_click = 0 if 'auto_click' not in kwargs else int(kwargs['auto_click'])
        self.auto_sell = 0 if 'auto_sell' not in kwargs else int(kwargs['auto_sell'])
        self.auto_click_price = 100
        self.auto_sell_price = 100
        self.milk_levels = [
            {'limit': 0,
             'price': 0,
             'image': 'img/game/milk/none.png',
             'size': (1, 1),
             'worker_image': 'img/game/milk/none.png',
             'worker_image_size': (1, 1),
             'xy_worker': (300, 300)},

            {'limit': 1,
             'price': 10,
             'image': 'img/game/milk/bottle.png',
             'size': (25, 100),
             'worker_image': 'img/game/milk/chat.png',
             'worker_image_size': (90, 163),
             'xy_worker': (350, 300),
             'description': 'Нанять чач',
             'button_width': 250},  # Бутылка с молоком

            {'limit': 2,
             'price': 25,
             'image': 'img/game/milk/bottles.png',
             'size': (100, 100),
             'worker_image': 'img/game/milk/chat.png',
             'worker_image_size': (90, 163),
             'xy_worker': (350, 300),
             'description': 'Купить ещё бутылок',
             'button_width': 320},  # много бутылок

            {'limit': 4,
             'price': 50,
             'image': 'img/game/milk/bucket.png',
             'size': (100, 110),
             'worker_image': 'img/game/milk/neo.png',
             'worker_image_size': (220, 245),
             'xy_worker': (300, 230),
             'description': 'Нанять Нео',
             'button_width': 250},  # Нео и арт с молочником

            {'limit': 8,
             'price': 80,
             'image': 'img/game/milk/bucket_2.png',
             'size': (150, 110),
             'worker_image': 'img/game/milk/neo.png',
             'worker_image_size': (220, 245),
             'xy_worker': (300, 230),
             'description': 'Купить ещё ведро',
             'button_width': 300},  # +несколько вёдер

            {'limit': 12,
             'price': 90,
             'image': 'img/game/milk/bucket_3.png',
             'size': (180, 110),
             'worker_image': 'img/game/milk/neo.png',
             'worker_image_size': (220, 245),
             'xy_worker': (300, 230),
             'description': 'Купить ещё ведро',
             'button_width': 300},  # +ещё вёдра

            {'limit': 20,
             'price': 100,
             'image': 'img/game/milk/shalker.png',
             'size': (100, 100),
             'worker_image': 'img/game/milk/labus.png',
             'worker_image_size': (240, 224),
             'xy_worker': (260, 270),
             'description': 'Нанять Арлабуса',
             'button_width': 290},  # арлабус и его шалкер

            # {'limit': 432,
            #  'price': 120,
            #  'image': 'img/game/milk/shalkers.png',
            #  'size': (200, 100),
            #  'worker_image': 'img/game/milk/labus.png',
            #  'worker_image_size': (240, 224),
            #  'xy_worker': (250, 260),
            #  'description': 'Купить ещё шалкеров',
            #  'button_width': 350}  # больше шалкеров
        ]

        self.money_levels = [
            {'cost': 0,
             'price': 0,
             'image': 'img/game/cows/none.png',
             'size': (1, 1),
             'description': '',
             'button_width': 5},

            {'cost': 1,
             'price': 10,
             'image': 'img/game/cows/cow.png',
             'size': (282, 293),
             'description': 'Купить корову',
             'button_width': 250},  # cow

            {'cost': 1.5,
             'price': 30,
             'image': 'img/game/cows/farm.png',
             'size': (260, 250),
             'description': 'Купить ферму',
             'button_width': 250},  # farm

            {'cost': 2,
             'price': 50,
             'image': 'img/game/cows/minecraft_cow.png',
             'size': (250, 250),
             'description': 'Купить майнкрафт корову',
             'button_width': 390},  # minecraft cow

            {'cost': 2.5,
             'price': 100,
             'image': 'img/game/cows/ketrin.jpg',
             'size': (197, 280),
             'description': 'Купить Кэт-корову',
             'button_width': 310},  # ketrin

            {'cost': 3.5,
             'price': 150,
             'image': 'img/game/cows/ketrin_ytka.png',
             'size': (297, 280),
             'description': 'Пригласить на работу утку',
             'button_width': 400},  # колаб с утка(у арта кэт утка и творог)

            {'cost': 5,
             'price': 200,
             'image': 'img/game/cows/ketrin_cneg.png',
             'size': (297, 280),
             'description': 'Пригласить на работу снег',
             'button_width': 410}  # колаб с снегом(у арта кэт мороженное)
        ]

    def update(self, seconds: float):
        self.milk_level = min(self.milk_level, len(self.milk_levels) - 1)
        ras = self.milk + seconds * self.auto_click * 0.1
        if ras > 1 and self.auto_sell:
            self.milk = min(ras, self.milk_levels[self.milk_level]['limit'])
            self.sell_milk()
            self.milk = 0
            return
        self.milk = min(ras, self.milk_levels[self.milk_level]['limit'])

    def sell_milk(self):
        self.money += self.get_money_of_milk()
        self.money = round(self.money, 2)
        self.milk = 0

    def update_money(self):
        if self.money_level + 1 == len(self.money_levels):
            return
        if self.money >= self.money_levels[self.money_level + 1]['price']:
            self.money -= self.money_levels[self.money_level + 1]['price']
            self.money = round(self.money, 2)
            self.money_level += 1

    def update_milk(self):
        if self.milk_level + 1 == len(self.milk_levels):
            return
        if self.money >= self.milk_levels[self.milk_level + 1]['price']:
            self.money -= self.milk_levels[self.milk_level + 1]['price']
            self.money = round(self.money, 2)
            self.milk_level += 1

    def update_milk_on_click(self):
        self.milk_level = min(self.milk_level, len(self.milk_levels) - 1)
        ras = self.milk + 0.15
        if ras > 1 and self.auto_sell:
            self.milk = min(ras, self.milk_levels[self.milk_level]['limit'])
            self.sell_milk()
            self.milk = 0
            return
        self.milk = min(ras, self.milk_levels[self.milk_level]['limit'])

    def get_money_of_milk(self):
        return float(round(self.money_levels[self.money_level]['cost'] * self.milk, 2))

    def buy_auto_click(self):
        if self.money < self.auto_click_price:
            return
        self.auto_click += 1
        self.money -= self.auto_click_price
        self.money = round(self.money, 2)
        self.auto_click_price += 10 * self.auto_click

    def buy_auto_sell(self):
        if self.money < self.auto_sell_price:
            return
        self.auto_sell = 1
        self.money -= self.auto_sell_price
        self.money = round(self.money, 2)
