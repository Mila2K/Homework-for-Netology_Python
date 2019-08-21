import datetime
import os


def param_decor(param):
    def decor(old_function):
        def new_function(*args, **kwargs):
            data = old_function(*args, ** kwargs)
            arguments = args
            with open(param, 'w', encoding='utf-8') as file:
                file.write('\n Дата и время вызова функции: ')
                file.write(str(datetime.datetime.now()))
                file.write('\n Аргументы функции: ')
                file.write(str(arguments))
                file.write('\n Результат функции: ')
                file.write(str(data))
        return new_function
    return decor


def get_recipe_ingredient(str_add):
    if not (type(str_add) is str):
         raise Exception(f'Argument Exception {str_add} is not a string')
    str_dict = dict()
    listed_string = str_add.split('|')
    str_dict['ingredient_name'] = listed_string[0].lstrip(' ').rstrip(' ')
    str_dict['quantity'] = int(listed_string[1].lstrip(' ').rstrip(' '))
    str_dict['measure'] = listed_string[2].lstrip(' ').rstrip(' ')
    return str_dict


def fill_cook_book():
    cook_book = dict()
    not_empty = True
    with open('Recipes.txt', 'r',  encoding='utf-8') as f:
        while not_empty:
            recipe_name = f.readline().strip()
            cook_book[recipe_name] = list()
            ingr_count = int(f.readline().strip())
            for ingr in range(0, ingr_count):
                cook_book[recipe_name].append(get_recipe_ingredient(f.readline().strip()))
            blank = f.readline()
            if blank == '':
                not_empty = False
    return cook_book


@param_decor(param=os.path.join('C:\\_fforhw\\res', 'decorators.txt'))
def get_shop_list_by_dishes(dishes, person_count, cook_book):
    shopping_list = dict()
    if not (type(dishes) is list):
        raise Exception(f'Argument Exception {dishes} is not a list')
    # all(elem in list1  for elem in list2)
    if not all(elem in cook_book.keys() for elem in dishes):
        print('Проверьте список рецептов!')
        return
    for recipe_name in dishes:
        ingr_list = cook_book[recipe_name]
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
    cook_book = fill_cook_book()
    print('\n Книга рецептов: ', cook_book)
    get_shop_list_by_dishes(['Омлет', 'Фахитос'], 4, cook_book)


main()