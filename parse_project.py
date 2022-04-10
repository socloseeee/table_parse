import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
from prettytable import PrettyTable


def parse_table():
    url = 'https://bim-proektstroy.ru/%d0%be%d0%bd%d0%bb%d0%b0%d0%b9%d0%bd-%d1%81%d0%bf%d1%80%d0%b0%d0%b2%d0%be%d1%87%d0%bd%d0%b8%d0%ba-%d0%ba%d0%bb%d0%b8%d0%bc%d0%b0%d1%82%d0%b8%d1%87%d0%b5%d1%81%d0%ba%d0%b8%d1%85-%d1%80%d0%b0%d0%b9/'
    page = requests.get(url)

    soup = BeautifulSoup(page.text, 'lxml')

    table1 = soup.find('table', id='tablepress-5')

    headers = []
    for i in table1.find_all('th'):
        title = i.text
        headers.append(title)

    mydata = pd.DataFrame(columns=headers)


    for j in table1.find_all('tr')[1:]:
        row_data = j.find_all('td')
        row = [i.text for i in row_data]
        length = len(mydata)
        mydata.loc[length] = row

    # Export to csv
    mydata.to_csv('data.csv', index=False)


def beautiful_table(head, values):
    columns = len(head)  # Подсчитаем кол-во столбцов на будущее.
    table = PrettyTable(head)  # Определяем таблицу.
    # Cкопируем список td, на случай если он будет использоваться в коде дальше.
    td_data = values[:]  # Входим в цикл который заполняет нашу таблицу. Цикл будет выполняться до тех пор пока
    # у нас не кончатся данные для заполнения строк таблицы (список td_data).
    while td_data:
        table.add_row(td_data[:columns])  # Используя срез добавляем первые три элементов в строку (columns = 3).
        td_data = td_data[columns:]  # Используя срез переопределяем td_data так, чтобы он
        table.hrules = 1
        # больше не содержал первых 3 элементов.

    print(table)  # Печатаем таблицу


def algorythm(budget, city):
    technologies = {
                    'Кирпич': 'Штукатурка - 5 мм \n'
                              'Кирпичная кладка-250 мм\n'
                              'Утепление минватой - 100 мм \n'
                              'Воздушный зазор - 20 мм'
                              'Облицовка фасада кирпичом - 120 мм \n'
                              'Итого: 495 мм',
                    'Пеноблок': 'Штукатурка - 5 мм \n'
                                'Пеноблок - 200 мм \n'
                                'Утепление минватой - 100 мм \n'
                                'Воздушный зазор - 20 мм\n'
                                'Облицовка фасада кирпичом - 120 мм\n'
                                'Итого: 445 мм',
                    'Деревянный каркас': 'Обшивка с внут. стороны ГКЛ+ГВЛ - 25 мм\n'
                                         'Каркас с заполнением минватой - 150 мм\n'
                                         'обрешётка - 44 мм\n'
                                         'фиброцементные панели под кирпич- 15 мм \n'
                                         'Итого: 234 мм',
                    'Бетон': 'Штукатурка - 5 мм \n'
                             'Бетонная стена - 250 мм \n'
                             'Утепление минватой - 100 мм \n'
                             'Вентилируемый фасад - 50 мм \n'
                             'Итого: 405 мм'
                    }

    humidity = '-'
    td = []

    input = open('data.csv', 'rt', encoding='UTF-8')
    for row in csv.reader(input):
        if city in row[0]:
            td.append(row)
            degrees = [el for el in row[3].split(' ') if el.isdigit() or '-' in el]
            degree = degrees[0] if len(degrees) == 1 else degrees[1]
            if humidity == '-':
                humidity = row[-1]
    humidity = humidity if humidity != '-' else 'Незначительный уровень влажности'

    td_new = []
    for elem in td:
        for el in elem:
            td_new.append(el)
    th = [elem for elem in pd.read_csv('data.csv', nrows=1).columns]

    beautiful_table(th, td_new)

    if budget < 20000000:
        if int(degree) < -14:
            material = 'Деревянный каркас'
        else:
            if humidity != '-':
                material = 'Бетон'
            else:
                material = 'Кирпич Пеноблок'.split()
    else:
        if humidity != '-':
            material = 'Бетон'
        else:
            material = 'Кирпич Пеноблок'.split()
            if (budget // 21700) > 5500:
                material = 'Бетон Пеноблок'.split()

    #material = 'Бетон Пеноблок'.split()
    #print(material)

    if len(material) != 2:
        if material == 'Бетон':
            square = budget // 16500
        elif material == 'Деревянный каркас':
            square = budget // 15200
        elif material == 'Кирпич':
            square = budget // 21700
        else:
            square = budget // 19000
        square = str(square)
    else:
        square = []
        if 'Бетон' in material:
            square.append(budget // 21700)
            square.append(budget // 19000)
        else:
            square.append(budget // 16500)
            square.append(budget // 19000)

    if len(square) != 2 or int(square) < 100:
        square = int(square)
        if 2500 >= square > 1000:
            stage = 5
        elif 4000 >= square > 2500:
            stage = 9
        elif 5800 >= square > 4000:
            stage = 12
        elif 8000 >= square > 5800:
            stage = 16
        elif 17000 >= square > 8000:
            stage = 22
        elif square > 17000:
            stage = 30
        else:
            stage = '1 - 4'
        stage = str(stage)
    else:
        stage = []
        for elem in square:
            elem = int(elem)
            if elem > 1000:
                stage.append(5)
            elif elem > 2500:
                stage.append(9)
            elif elem > 4000:
                stage.append(12)
            elif elem > 5800:
                stage.append(16)
            elif elem > 8000:
                stage.append(22)
            elif elem > 17000:
                stage.append(30)
            else:
                stage.append('1 - 4')

    if len(stage) != 2 or str(stage[0]).isdigit():
        th = ('Площадь', 'Этажи', 'Технологии', 'Материал')
        td = [square, stage, material, technologies[material]]
    else:
        th = ('Площадь', 'Этажи', 'Технологии', 'Материал')
        td = []
        for i in range(2):
            td.append(square[i])
            td.append(stage[i])
            td.append(material[i])
            td.append(technologies[material[i]])

    beautiful_table(th, td)


def city():
    city = ''
    while len(city) <= 4:
        city = input('Введите название города или области (Минимум 4 буквы!) > ')
        if len(city) > 4:
            break
        print('Некорректный ввод!')
    return city


def budget():
    while True:
        budget = ''
        budget = input('Введите бюджет > ')
        if budget.isdigit():
            break
        print('Некорректный ввод!')
    return int(budget)


if __name__ == "__main__":
    parse_table()
    algorythm(budget(), city())