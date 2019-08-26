class ClassContact:
    """Создать приложение телефонная книга. класс Contact имеет следующие поля:
        Имя, фамилия, телефонный номер - обязательные поля;
        избранный контакт - необязательное поле. По умолчанию False;
        Дополнительная информация(список дополнительных номеров, email, ссылки на соцсети) - необходимо использовать *args, **kwargs."""
    def __init__(self, str_first_name, str_last_name, str_number, *args, is_favorite=False, ** kwargs):
        self.str_first_name = str_first_name
        self.str_last_name = str_last_name
        self.str_number = str_number
        self.is_favorite = is_favorite
        if args:
            for arg in args:
                print(arg)
        if kwargs.items():
            for add_field, add_value in kwargs.items():
                print(add_field, '=', add_value)

    def add_contact(self):
        contacts_list = list()
        contacts_list.append(self)
        print(contacts_list[0])


class PhoneBook:
    """класс PhoneBook:
    Название телефонной книги - обязательное поле;
    Телефонная книга должна работать с классами Contact."""
    def __init__(self, str_title):
        self.str_title = str_title
        self.contacts_list = list()

    def add_contact(self, str_first_name, str_last_name, str_number, is_favorite=False):
        obj_contact = ClassContact(str_first_name, str_last_name, str_number)
        obj_contact.str_first_name = str_first_name
        print(obj_contact.str_first_name)
        obj_contact.str_last_name = str_last_name
        print(obj_contact.str_last_name)
        obj_contact.str_number = str_number
        print(obj_contact.str_number)
        obj_contact.is_favorite = is_favorite
        print(obj_contact.is_favorite)
        self.contacts_list.append(obj_contact)
        print(obj_contact)


ex = ClassContact('helen', 'hunt', '000', '00480935803', telegram='ololoo')
ex.add_contact()



