# Импорт библиотеки tkinter для работы с GUI
from tkinter import *
from tkinter import filedialog as fd


# Класс машины
class Car:
    # Конструктор, принимающий в себя необходимые поля
    def __init__(self, model, country, year, cost):
        self.model = model
        self.country = country
        self.year = int(year)
        self.cost = cost

    # Метод, возвращающий true если год выпуска не ранее срока
    def not_older(self, year):
        return self.year >= year


# Функция, которая считывает таблицу с данными
def read_database(filename):
    try:
        file = open(filename, encoding='UTF-8')
        file_lines = file.readlines()
        # Удаление заголовков
        file_lines.pop(0)
        processed_lines = []
        # Форматирование csv-файла
        for line in file_lines:
            processed_lines.append(line.replace('\n', '').rsplit(';'))
        file.close()
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
def get_cars_by_year(search_cars_by_year, year):
    filtered_cars = []
    for search_car in search_cars_by_year:
        if search_car.not_older(year):
            filtered_cars.append(search_car)
    return filtered_cars


# Функция закрытия программы
def close_program():
    exit()


# Функция, осуществляющая отрисовку поиска (рисует рез. поиска, либо отсутствие рез.)
def search_cars(search_frame, year):
    # Очистка виджетов перед отрисовкой
    for children in search_frame.winfo_children():
        children.destroy()
    try:
        # Получаем список машин, соответсвующих поисковому запросу
        searched_cars = get_cars_by_year(cars, int(year))
        if len(searched_cars) > 0:
            draw_cars_table(search_frame, searched_cars)
            # Считаем количество найденных и не найденных машин
            cars_qualified = len(searched_cars)
            cars_not_qualified = len(cars) - cars_qualified
            # Рисуем диаграмму
            draw_diagram(search_frame, cars_not_qualified, cars_qualified)
        # Если поиск не дал результатов, возварщаем соответсвующее окно
        else:
            draw_no_result(search_frame)
    except ValueError:
        draw_no_result(search_frame)


# Отрисовка таблицы - результат поискового запроса
def draw_cars_table(search_frame, draw_cars):
    search_result_frame = LabelFrame(search_frame, height=250, width=100, text='Результаты поиска:')
    search_result_frame.pack(side=LEFT)

    # Верхняя строка - заголовки
    model_key_label = Label(search_result_frame, text='Марка автомобиля')
    model_key_label.grid(row=0, column=0)
    country_key_label = Label(search_result_frame, text='Страна')
    country_key_label.grid(row=0, column=1)
    year_key_label = Label(search_result_frame, text='Год')
    year_key_label.grid(row=0, column=2)
    price_key_label = Label(search_result_frame, text='Стоимость')
    price_key_label.grid(row=0, column=3)

    # Для каждой машины отрисовываем поля с данными
    for index in range(len(draw_cars)):
        car_model_label = Label(search_result_frame, text=draw_cars[index].model)
        car_model_label.grid(row=index+1, column=0)
        car_country_label = Label(search_result_frame, text=draw_cars[index].country)
        car_country_label.grid(row=index + 1, column=1)
        car_year_label = Label(search_result_frame, text=draw_cars[index].year)
        car_year_label.grid(row=index + 1, column=2)
        car_cost_label = Label(search_result_frame, text=draw_cars[index].cost)
        car_cost_label.grid(row=index + 1, column=3)


# Функция, отрисовывающая окно, когда поиск не дал результатов
def draw_no_result(search_frame):
    search_result_frame = Frame(search_frame)
    search_result_frame.pack(side=BOTTOM)
    no_result_label = Label(search_result_frame, text='Поиск не дал результатов')
    no_result_label.pack(padx=100, pady=100)


# Функция отрисовки диаграммы - кол-во найденных авто
def draw_diagram(search_frame, num_cars_search_not_qualified, num_cars_search_qualified):
    diagram_frame = LabelFrame(search_frame, width=30, text='Диаграмма')
    diagram_frame.pack(side=RIGHT, padx=14)
    max_height = 10
    not_qualified_color = 'dodger blue'
    qualified_color = 'firebrick1'
    # Отрисовка легенды
    diagram_legend_frame = LabelFrame(diagram_frame, text='Легенда')
    diagram_legend_frame.pack(side=BOTTOM, padx=4, pady=4)
    # Отрисовка легенды "не соотв. поиску"
    legend_not_qualified_frame = Frame(diagram_legend_frame)
    legend_not_qualified_color_frame = Frame(legend_not_qualified_frame, bg=not_qualified_color, width=5, height=5)
    legend_not_qualified_color_frame.pack(side=LEFT)
    legend_not_qualified_label = Label(legend_not_qualified_frame, text='Не соответствует результатам поиска')
    legend_not_qualified_label.pack(side=RIGHT)
    legend_not_qualified_frame.pack(side=TOP, padx=1, pady=1, anchor=NW)
    # Отрисовка легенды "соотв. поиску"
    legend_qualified_frame = Frame(diagram_legend_frame)
    legend_qualified_color_frame = Frame(legend_qualified_frame, bg=qualified_color, width=5, height=5)
    legend_qualified_color_frame.pack(side=LEFT)
    legend_qualified_label = Label(legend_qualified_frame, text='Соответствует результатам поиска')
    legend_qualified_label.pack(side=RIGHT)
    legend_qualified_frame.pack(side=BOTTOM, padx=1, pady=1, anchor=SW)

    # Спец. случай если поисковый запрос вернул все авто
    if num_cars_search_not_qualified == 0:
        qualified_diagram = Label(diagram_frame, width=1, height=max_height, bg=qualified_color,
                                  text=num_cars_search_qualified)
        qualified_diagram.pack(side=RIGHT, anchor=SE, padx=5)
    # Спец. случай если поисковый запрос вернул 0 авто
    elif num_cars_search_qualified == 0:
        not_qualified_diagram = Label(diagram_frame, width=1, height=max_height, bg=not_qualified_color,
                                      text=num_cars_search_not_qualified)
        not_qualified_diagram.pack(side=LEFT, anchor=SW, padx=5)
    # Иначе - с помощью коэффициента высчитываем соотношение кол-во найденных и не найденных авто
    else:
        num_overall = num_cars_search_not_qualified + num_cars_search_qualified
        not_qualified_height = (num_cars_search_not_qualified / num_overall) * max_height
        qualified_height = (num_cars_search_qualified / num_overall) * max_height

        not_qualified_diagram = Label(diagram_frame, width=1, height=int(not_qualified_height), bg=not_qualified_color,
                                      text=num_cars_search_not_qualified)
        not_qualified_diagram.pack(side=LEFT, anchor=SW, padx=5)

        qualified_diagram = Label(diagram_frame, width=1, height=int(qualified_height), bg=qualified_color,
                                  text=num_cars_search_qualified)
        qualified_diagram.pack(side=RIGHT, anchor=SE, padx=5)


# Запуск главной программы
def start_program():
    # Программа
    def accept_file():
        file_name = input_file_entry.get()
        global cars
        cars = convert_lines_to_cars(read_database(file_name))

    # Поиск пути в проводнике
    def search_file():
        file_name = fd.askopenfilename()
        # Замена поля ввода
        input_file_entry.delete(0, END)
        input_file_entry.insert(0, file_name)

        global cars
        cars = convert_lines_to_cars(read_database(file_name))

    main_window = Toplevel(root)
    main_window.minsize(width=400, height=300)
    # Главный фрэйм приложения
    app_frame = Frame(main_window)
    app_frame.pack()
    # Фрейм ввода файла
    input_file_frame = Frame(app_frame)
    input_file_frame.pack(side=TOP, pady=10)
    input_file_text_label = Label(input_file_frame, text='Введите путь к файлу:')
    input_file_text_label.pack(side=TOP)
    input_file_entry = Entry(input_file_frame, width=100)
    input_file_entry.pack(side=LEFT)
    accept_file_button = Button(input_file_frame, text='Готово', height=1,
                                command=lambda: accept_file())
    accept_file_button.pack(side=RIGHT)
    search_file_button = Button(input_file_frame, text='Обзор', height=1,
                                command=lambda: search_file())
    search_file_button.pack(side=RIGHT)

    # Фрейм для результатов поиска
    search_place_frame = Frame(app_frame, height=100)
    search_place_frame.pack(side=BOTTOM, padx=30, pady=30)

    # Фрейм ввода года
    input_year_frame = Frame(app_frame)
    input_year_frame.pack(side=TOP, pady=10)
    input_year_text_label = Label(input_year_frame, text='Введите год:')
    input_year_text_label.pack(side=TOP)
    input_year_entry = Entry(input_year_frame, width=30)
    input_year_entry.pack(side=LEFT)
    search_button = Button(input_year_frame, text='Поиск', height=1,
                           command=lambda: search_cars(search_place_frame, input_year_entry.get()))
    search_button.pack(side=RIGHT)


# Главное Приложение, запуск стартового экрана
root = Tk()
cars = []

root.title('Тема 7. Получение сведений об авто')
# Фрэйм-шапка приложения
app_bar_frame = Frame(root, bg='SteelBlue1')
app_bar_frame.pack(side=TOP)
close_button = Button(app_bar_frame, text='Завершение работы', width=30, height=5, command=lambda: close_program())
close_button.pack(side=RIGHT, expand=1, anchor=SE)
student_text_label = Label(app_bar_frame, text='19-ИЭ-2 Таранов И.А.', bg='SteelBlue1')
student_text_label.pack(side=TOP)
start_button = Button(app_bar_frame, text='Начало', width=30, height=5, command=lambda: start_program())
start_button.pack(side=LEFT, expand=1, anchor=SW)

# Главный цикл
root.mainloop()
