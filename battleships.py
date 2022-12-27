# Решать задачу будем последовательной реализацией нужных классов. Во многих случаях правильное разбиение кода на классы делает ваш код хорошо читаемым и экономит очень много времени. Можно выделить две группы классов:

# Внутренняя логика игры — корабли, игровая доска и вся логика связанная с ней.
# Внешняя логика игры — пользовательский интерфейс, искусственный интеллект, игровой контроллер, который считает побитые корабли.
# В начале имеет смысл написать классы исключений, которые будет использовать наша программа. Например, когда игрок пытается выстрелить в клетку за пределами поля, во внутренней логике должно выбрасываться соответствующее исключение BoardOutException, а потом отлавливаться во внешней логике, выводя сообщение об этой ошибке пользователю.

# Далее нужно реализовать класс Dot — класс точек на поле. Каждая точка описывается параметрами:

# Координата по оси x .
# Координата по оси y .
# В программе мы будем часто обмениваться информацией о точках на поле, поэтому имеет смысле сделать отдельный тип данных для них. Очень удобно будет реализовать в этом классе метод __eq__, чтобы точки можно было проверять на равенство. Тогда, чтобы проверить, находится ли точка в списке, достаточно просто использовать оператор in, как мы делали это с числами .

# Следующим идёт класс Ship — корабль на игровом поле, который описывается параметрами:

# Длина.
# Точка, где размещён нос корабля.
# Направление корабля (вертикальное/горизонтальное).
# Количеством жизней (сколько точек корабля еще не подбито).
# И имеет методы:

# Метод dots, который возвращает список всех точек корабля.
# Самый важный класс во внутренней логике — класс Board — игровая доска. Доска описывается параметрами:

# Двумерный список, в котором хранятся состояния каждой из клеток.
# Список кораблей доски.
# Параметр hid типа bool — информация о том, нужно ли скрывать корабли на доске (для вывода доски врага) или нет (для своей доски).
# Количество живых кораблей на доске.
# И имеет методы:

# Метод add_ship, который ставит корабль на доску (если ставить не получается, выбрасываем исключения).
# Метод contour, который обводит корабль по контуру. Он будет полезен и в ходе самой игры, и в при расстановке кораблей (помечает соседние точки, где корабля по правилам быть не может).
# Метод, который выводит доску в консоль в зависимости от параметра hid.
# Метод out, который для точки (объекта класса Dot) возвращает True, если точка выходит за пределы поля, и False, если не выходит.
# Метод shot, который делает выстрел по доске (если есть попытка выстрелить за пределы и в использованную точку, нужно выбрасывать исключения).
# Теперь нужно заняться внешней логикой: Класс Player — класс игрока в игру (и AI, и пользователь). Этот класс будет родителем для классов с AI и с пользователем. Игрок описывается параметрами:

# Собственная доска (объект класса Board)
# Доска врага.
# И имеет следующие методы:

# ask — метод, который «спрашивает» игрока, в какую клетку он делает выстрел. Пока мы делаем общий для AI и пользователя класс, этот метод мы описать не можем. Оставим этот метод пустым. Тем самым обозначим, что потомки должны реализовать этот метод.
# move — метод, который делает ход в игре. Тут мы вызываем метод ask, делаем выстрел по вражеской доске (метод Board.shot), отлавливаем исключения, и если они есть, пытаемся повторить ход. Метод должен возвращать True, если этому игроку нужен повторный ход (например если он выстрелом подбил корабль).
# Теперь нам остаётся унаследовать классы AI и User от Player и переопределить в них метод ask. Для AI это будет выбор случайной точка, а для User этот метод будет спрашивать координаты точки из консоли.

# После создаём наш главный класс — класс Game. Игра описывается параметрами:

# Игрок-пользователь, объект класса User.
# Доска пользователя.
# Игрок-компьютер, объект класса Ai.
# Доска компьютера.
# И имеет методы:

# random_board — метод генерирует случайную доску. Для этого мы просто пытаемся в случайные клетки изначально пустой доски расставлять корабли (в бесконечном цикле пытаемся поставить корабль в случайную доску, пока наша попытка не окажется успешной). Лучше расставлять сначала длинные корабли, а потом короткие. Если было сделано много (несколько тысяч) попыток установить корабль, но это не получилось, значит доска неудачная и на неё корабль уже не добавить. В таком случае нужно начать генерировать новую доску.
# greet — метод, который в консоли приветствует пользователя и рассказывает о формате ввода.
# loop — метод с самим игровым циклом. Там мы просто последовательно вызываем метод mode для игроков и делаем проверку, сколько живых кораблей осталось на досках, чтобы определить победу.
# start — запуск игры. Сначала вызываем greet, а потом loop.
# И останется просто создать экземпляр класса Game и вызвать метод start.

# По ходу написания кода полезно проверять свой прогресс, тестируя написанные классы по отдельности. Для этого можно моделировать различные ситуации, например, создать список кораблей, добавить их на доску и попробовать сделать выстрел в разные точки. Для проверки функционала класса не обязательно иметь весь написанный код.
import pandas as pd
from random import randint

class BoardException(Exception):
    pass

class BoardOutException(BoardException):
    def __str__(self):
        return "Выстрел попадает за пределы доски!"

class BoardWrongTargetException(BoardException):
    def __str__(self):
        return "Вы стреляли в эту клетку!"

class BoardWrongPlaceException(BoardException):
    pass

class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, diff):
        return self.x == diff.x and self.y == diff.y

    def __repr__(self):
        return f"Dot({self.x}, {self.y})"

# a = Dot(1, 4)
# b = Dot(1, 4)
# c = Dot(3, 6)
# print(a == c)

class Ship:
    def __init__(self, front, length, vertical = True):
        self.lenght = length
        self.front = front
        self.vertical = vertical
        self.hp = 1
    @property
    def dots(self):
        ship = []
        for i in range(self.lenght):
            cur_x = self.front.x
            cur_y = self.front.y
            # корабль имеет вертикальное направление
            if self.vertical:
                cur_y += i
            # корабль имеет горизонтальное направление
            else:
                cur_x += i
            ship.append(Dot(cur_x, cur_y))
        return ship
    # проверка на попадание
    def hit(self, shot):
        return shot in self.dots

# varyag = Ship(Dot(2,2), 3, 1)
# print(varyag.dots)


class Board:
    def __init__(self, hid = False, scope = 6):
        # параметр масштаба карты
        self.scope = scope
        # параметр видимости карты
        self.hid = hid

        # параметр для создания игрового поля
        self.map = [["o"]*scope for _ in range(scope)]
        # параметр отражающий список кораблей на карте
        self.ship_list = []
        # параметр количества пораженных кораблей
        self.ship_dmg = 0
        # параметр указывает на занятые места на карте
        self.occup = []
    # метод для печати карты и скрытия кораблей
    def __repr__(self):
        map_print = ""
        map_print += "  | 1 | 2 | 3 | 4 | 5 | 6 |"

        for i, row in enumerate(self.map):
            map_print += f"\n{i+1} | " + " | ".join(row) + " |"

        if self.hid:
            map_print = map_print.replace("■", "o")
        return map_print
    # метод проверяющий не была ли указана точка за границей карты
    def out_of_bounds(self, point):
        return not ((0 <= point.x < self.scope) and (0 <= point.y < self.scope))
        
            
    # метод рисующий контур вокруг кораблей
    def contour(self, ship, verb = False):
        around_area = [
            (-1,-1), (-1,0), (-1,1),
            (0,-1), (0,0), (0,1),
            (1,-1), (1,0), (1,1)
        ]
        for point in ship.dots:
            for p_x, p_y in around_area:
                cur = Dot(point.x + p_x, point.y + p_y)
                if not(self.out_of_bounds(cur)) or cur not in self.occup:
                    if verb:
                        self.map[cur.x][cur.y] = "."
                    self.occup.append(cur)
    # добавляем корабль на карту
    def add_ship(self, ship):
        for point in ship.dots:
            if self.out_of_bounds(point) or point in self.occup:
                raise BoardWrongPlaceException
            self.map[point.x][point.y] = "■"
            self.occup.append(point)
        self.ship_list.append(ship)
        self.contour(ship)

    # добавляем отметку выстрела на карту
    def shot(self, point):
        if self.out_of_bounds(point):
            raise BoardOutException()
        if point in self.occup:
            raise BoardWrongTargetException
        self.occup.append(point)

        for ship in self.ship_list:
            if ship.hit(point):
                ship.hp -= 1
                self.map[point.x][point.y] = "X"
                if ship.hp == 0:
                    self.ship_dmg += 1
                    self.contour(ship, verb = True)
                    print("Корабль потоплен!")
                    return False
                else:
                    print("Корабль поврежден!")
                    return True
        self.map[point.x][point.y] = "."
        print("Промах!")
        return False
    
    def begin(self):
        self.occur = []
# g = Board()
# g.add_ship(Ship(Dot(1, 2), 2, 0))
# print(g)
# f = Board()
# print(f)
# инициализация игрока 
class Player:
    def __init__(self, board, opponent):
        self.board = board
        self.opponent = opponent
    def ask(self):
        raise NotImplementedError()
    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.opponent.shot(target)
                return repeat
            except BoardException:
                print("Произошла ошибка!")
# инициализация искусственного интелекта 
class AI(Player):
    def ask(self):       
        point = Dot(randint(0, 5), randint(0, 5))
        print(f"Компьютер ходит: {point.x + 1}{point.y + 1}")
        return point
    

# класс для ввода координат цели
class User(Player):
    def ask(self):
        while True:
            coords = input("Введите координаты цели:").split()
            if len(coords) != 2:
                print("Введите две координаты!")
                continue

            x, y = coords

            if not (x.isdigit()) or not(y.isdigit()):
                print("Введите численные координаты!")
                continue
            
            x, y = int(x), int(y)
            return Dot(x - 1, y - 1)


class Game:
    def __init__(self, scope = 6):
        self.scope = scope
        player = self.random_board()
        comp = self.random_board()
        comp.hid = True
        
        self.ai = AI(comp, player)
        self.user = User(player, comp)

    def try_board(self):
        ship_lengths = [3, 2, 2, 1, 1, 1, 1]
        board = Board(scope = self.scope)
        attempts = 0
        for length in ship_lengths:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.scope), randint(0, self.scope)), length, randint(0,1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongPlaceException:
                    pass
        board.begin()
        return board
    
    def random_board(self):
        board = None
        while board is None:
            board = self.try_board()
        return board
       
# g = Game()
# g.scope = 6
# print(g.random_board())

    def greet(self):
        print("  Добро пожаловать в игру 'Морской бой'  ")
        print("-------------------")
        print(" формат ввода: x y ")
        print(" x - номер строки  ")
        print(" y - номер столбца ")
    
    
    def loop(self):
        num = 0
        while True:
            print("Доска пользователя:")
            print(self.user.board)
            print("Доска компьютера:")
            print(self.ai.board)

            if num % 2 == 0:
                print("Ход игрока!")
                repeat = self.user.move()
            else:
                print("Ход компьютера!")
                repeat = self.ai.move()
            if repeat:
                num -= 1
            
            if self.ai.board.count == 7:
                print("Игрок выиграл!")
                break
            
            if self.user.board.count == 7:
                print("Компьютер выиграл!")
                break
            num += 1
    def start(self):
        self.greet()
        self.loop()

f = Game()
f.start()