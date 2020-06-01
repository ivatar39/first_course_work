# Класс машины
class Car:
    # Конструктор, принимающий в себя необходимые поля
    def __init__(self, model, country, year, cost):
        self.model = model
        self.country = country
        self.year = year
        self.cost = cost

    # Метод, возвращающий true если год выпуска не ранее срока
    def not_older(self, year):
        return self.year >= year

    # Переопределённый метод, возвращающий объект в строковом виде
    def __str__(self):
        return "Модель - {}; Страна - {}; Год - {}; Цена - {}".format(self.model, self.country, self.year, self.cost)


# Функция, которая считывает таблицу с данными
def read_database():
    try:
        file = open(u'automobiles.csv', encoding='UTF-8')
        file_lines = file.readlines()
        # Удаление заголовков
        file_lines.pop(0)
        processed_lines = []
        for line in file_lines:
            processed_lines.append(line.replace('\n', '').rsplit(';'))
        return processed_lines
    except FileNotFoundError:
        print('Файл не найден')


# Функция, которая принимает список и возвращает список объектов-машин
def convert_lines_to_cars(lines):
    convert_cars = []
    for line in lines:
        convert_cars.append(Car(model=line[0], country=line[1], year=line[2], cost=line[3]))
    return convert_cars


# Функция, которая принимает список машин и возвращает список машин, не ранее указанного года
def get_cars_by_year(search_cars, year):
    filtered_cars = []
    for search_car in search_cars:
        if search_car.not_older(year):
            filtered_cars.append(search_car)
    return filtered_cars


# Программа
cars = convert_lines_to_cars(read_database())
for car in cars:
    print(car)
print('-'*55)

searched_cars = get_cars_by_year(cars, input('Введите год: '))
for searched_car in searched_cars:
    print(searched_car)
