"""
Расчитать кто сколько кому должен денег. Кто-то закупается некоторыми товарами, остальные должны денег
"""


class Men:
    """Создание участника мероприятия """
    def __init__(self):
        self.name = ''  # имя
        self.sum = 0  # сколько внес изначально
        self.debt_to_me = 0  # сколько ему должны
        self.debt_i = 0  # сколько он должен


class Company:
    """Создание группы участников. Вычисление кто-кому должен."""
    def __init__(self):
        self.list = []  # список компании
        self.num = 0  # количество участников
        self.all_sum = 0  # общая сумма затрат
        self.get_company()  # ввод участников

    def get_company(self):  # Создаем группу участников и вносим предварительные их затраты
        try:
            self.num = int(input('Введите сколько человек в компании: '))
        except ValueError:
            print('Необходимо ввести целое число! Попробуйте еще раз.')
            self.get_company()
        for i in range(self.num):
            men = Men()
            print(f'{i + 1} участник:')
            men.name = input('Имя: ')
            work = True
            while work:
                try:
                    number = input('Предварительно внес сумму: ')
                    number = number.replace(',', '.')  # Если введено число через запятую, заменим его на число с точкой
                    men.sum = float(number)
                    self.list.append(men)
                    work = False
                except ValueError:
                    print('Значение должно быть числом! Попробуйте еще раз.')
        self.sum()
        return self.list

    def sum(self):  # Вычисляем общую сумму затрат (смету)
        for men in self.list:
            self.all_sum += men.sum

    @property
    def part_of_sum(self):  # Вычисляем солидарную ответственность
        return self.all_sum / self.num

    def debt(self):  # Разбираемся кто сколько должен или должны ему
        for men in self.list:
            if men.sum != 0:  # Если предварительно тратил
                men.debt_to_me = men.sum - self.part_of_sum  # то ему должны за вычетом солидарной ответственности
            if men.debt_to_me == 0:  # Если предварительно не тратил
                men.debt_i = self.part_of_sum   # то должен солидарную
            elif men.debt_to_me < 0:  # Если тебе должны отрицательное значение
                men.debt_i = self.part_of_sum - men.sum  # то ты должен солидарную за вычетом предварительно сданной
                men.debt_to_me = 0   # и, соответственно, тебе не должны

    def started(self):  # Для начала выведем сводно кто сколько сдавал и сколько он или ему должны
        for i in self.list:
            print(f'{i.name}: {i.sum}, ему должны: {format(i.debt_to_me, ".2f")}, он должен {format(i.debt_i, ".2f")}')
        print('\nОбщая смета: ', self.all_sum)
        print('Солидарная ответственнось: ', format(self.part_of_sum, ".2f"), end='\n\n')

    def who_should(self):
        for men in self.list:  # Проверяем каждого участника
            if men.debt_to_me > 0:  # Если мне должны
                for to_me in self.list:  # то спрашиваем каждого
                    if to_me.debt_i > 0:  # должен ли он, если да то спрашиваем
                        if men.debt_to_me > to_me.debt_i:  # мне должны больше чем он должен
                            men.debt_to_me = men.debt_to_me - to_me.debt_i  # забираем что у него есть
                            print(f'{to_me.name} отдает {men.name}: {format(to_me.debt_i, ".2f")} рублей')
                            to_me.debt_i = 0
                        if men.debt_to_me <= to_me.debt_i and men.debt_to_me != 0: # мне должны меньше или столько же чем он должен
                            print(f'{to_me.name} отдает {men.name}: {format(men.debt_to_me, ".2f")} рублей')
                            to_me.debt_i = to_me.debt_i - men.debt_to_me  # забираем часть, которую должны мне
                            men.debt_to_me = 0

    def calculation(self):  # основной ход вычислений
        self.debt()
        self.started()
        self.who_should()


if __name__ == "__main__":
    company = Company()
    company.calculation()
