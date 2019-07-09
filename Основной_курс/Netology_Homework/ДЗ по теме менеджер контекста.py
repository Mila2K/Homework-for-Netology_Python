import time
from datetime import datetime


class MyFile:

    def __init__(self, file_name):
        self.file_name = file_name
        self.start_time = time.time()

    def __enter__(self):
        self.cook_book = dict()
        self.cook_book = self.fill_cook_book()
        print('\n Время начала выполнения функции:', datetime.now(tz=None))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.time()
        print('\n Время окончания выполнения функции:', datetime.now(tz=None))
        print('\n Выполнение функции заняло %s секунд' % (self.end_time - self.start_time))

    def get_recipe_ingredient(self, str_add):
        if not (type(str_add) is str):
            raise Exception(f'Argument Exception {str_add} is not a string')
        str_dict = dict()
        listed_string = str_add.split('|')
        str_dict['ingredient_name'] = listed_string[0].lstrip(' ').rstrip(' ')
        str_dict['quantity'] = int(listed_string[1].lstrip(' ').rstrip(' '))
        str_dict['measure'] = listed_string[2].lstrip(' ').rstrip(' ')
        return str_dict

    def fill_cook_book(self):
        not_empty = True
        with open(self.file_name, mode='r', encoding='utf-8') as f:
            while not_empty:
                recipe_name = f.readline().strip()
                self.cook_book[recipe_name] = list()
                ingr_count = int(f.readline().strip())
                for ingr in range(0, ingr_count):
                    self.cook_book[recipe_name].append(self.get_recipe_ingredient(f.readline().strip()))
                blank = f.readline()
                if blank == '':
                    not_empty = False
        return self.cook_book

    def get_shop_list_by_dishes(self, dishes, person_count):
        shopping_list = dict()
        if not (type(dishes) is list):
            raise Exception(f'Argument Exception {dishes} is not a list')
        # all(elem in list1  for elem in list2)
        if not all(elem in self.cook_book.keys() for elem in dishes):
            print('Проверьте список рецептов!')
            return
        for recipe_name in dishes:
            ingr_list = self.cook_book[recipe_name]
            for ingr_item in ingr_list:
                ingr_name = ingr_item['ingredient_name']
                if ingr_name in shopping_list.keys():
                    shopping_list[ingr_name]['quantity'] += ingr_item['quantity'] * person_count
                else:
                    shopping_list[ingr_name] = dict()
                    shopping_list[ingr_name].update({'measure': ingr_item['measure']})
                    shopping_list[ingr_name].update({'quantity': ingr_item['quantity'] * person_count})
        print('\n Ваш список покупок: ', shopping_list)
        return shopping_list


def main():

    with MyFile('Recipes.txt') as f:
        f.get_shop_list_by_dishes(['Омлет', 'Фахитос'], 4)


    #
    # print('\n Книга рецептов: ', cook_book)
    #
    # get_shop_list_by_dishes(['Омлет', 'Фахитос'], 4, cook_book)
    #
    # end_time = time.time()
    #


main()
