class ClassContact:
    """Создать приложение телефонная книга. класс Contact имеет следующие поля:
        Имя, фамилия, телефонный номер - обязательные поля;
        избранный контакт - необязательное поле. По умолчанию False;
        Дополнительная информация(список дополнительных номеров, email, ссылки на соцсети) - необходимо использовать *args, **kwargs."""
    def __init__(self, str_first_name, str_last_name, str_number, is_favorite, *args, ** kwargs):
        self.str_first_name = str_first_name
        self.str_last_name = str_last_name
        self.str_number = str_number
        self.is_favorite = is_favorite
        self.phones_list = list()
        self.additional_fields = dict()
        if args:
            for arg in args:
                self.phones_list.append(arg)
        if kwargs.items():
            for add_field, add_value in kwargs.items():
                self.additional_fields[add_field] = add_value

    def __str__(self):
        favourite_rus = 'нет'
        if self.is_favorite:
            favourite_rus = 'да'
        str_phones = ''
        for phone in self.phones_list:
            str_phones += f"{phone}, "
        str_additional_fields = ''
        for k, v in self.additional_fields.items():
            str_additional_fields += f"\t{k} : {v} \n"
        return f"Имя: {self.str_first_name} \nФамилия: {self.str_last_name} \nТелефон: {self.str_number} \n" \
               f"В избранных: {favourite_rus} \nДополнительная информация: {str_phones} \n{str_additional_fields}"


class PhoneBook:
    """класс PhoneBook:
    Название телефонной книги - обязательное поле;
    Телефонная книга должна работать с классами Contact."""
    def __init__(self, str_title):
        self.str_title = str_title
        self.contacts_list = list()

    def add_contact(self, str_first_name, str_last_name, str_number, *args, is_favorite=False, **kwargs):
        obj_contact = ClassContact(str_first_name, str_last_name, str_number, is_favorite, *args, **kwargs)
        self.contacts_list.append(obj_contact)
        print(obj_contact)

    def print_contact_list(self):
        for contact in self.contacts_list:
            print(contact)

    def print_contact(self, str_first_name, str_last_name):
        is_found = False
        for contact in self.contacts_list:
            if str_first_name == contact.str_first_name and str_last_name == contact.str_last_name:
                print(contact)
                is_found = True
        if not is_found:
            print('Проверьте правильность ввода имени и фамилии')

    def remove_contact(self, str_number):
        is_found = False
        temp_list = self.contacts_list
        for contact in temp_list:
            if str_number == contact.str_number:
                print(f"\nДанный контакт был удалён: \n{contact}")
                temp_list.remove(contact)
                print('\nДанные контакты остались в записной книжке: \n')
                for item in temp_list:
                    print(item)
                is_found = True
        if not is_found:
            print('Проверьте правильность введённого номера телефона')

    def find_fav(self, is_favourite=False):
        is_found = False
        for contact in self.contacts_list:
            if is_favourite != contact.is_favorite:
                print(f"\nИзбранный контакт: \n{contact}")
                is_found = True
        if not is_found:
            print('В телефонной книге нет избранных номеров')


pb = PhoneBook('phonebook')
pb.add_contact('helen', 'hunt', '001', '002', telegram='ioikj', vk='klklk')
pb.add_contact('oleg', 'abc', '002', '566', '677', is_favorite=True, telegram='ioikkl', vk='klkuyk')
# pb.print_contact_list()
# pb.remove_contact('001')
# pb.find_fav()
# pb.print_contact_list()



