from collections import UserDict
import datetime as dt
from datetime import datetime as dtdt
from functools import wraps
import pickle

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
		pass

class Phone(Field):
    def __init__(self, value):
        super().__init__(value) 
        self.__value = None
        self.value = value

    @property
    def value(self):
         return self.__value
    
    @value.setter
    def value(self, value):
        if len(value) == 10 and value.isdigit():
            self.__value = value
        else:
            raise ValueError("Wrong phone")
class Birthday(Field):
    def __init__(self, value):
        try:
            self.date = dtdt.strptime(value, "%d.%m.%Y").date()
            super().__init__(value)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
    
    def add_phone(self, phone_number):
        self.phones.append(Phone(phone_number))
    def remove_phone(self, phone_number):
        self.phones = (i for i in self.phones if str(i) != phone_number)
    def edit_phone(self, old_phone, new_phone):
        for i, phone in enumerate(self.phones):
            if str(phone) == old_phone:
                self.phones[i] = Phone(new_phone)
    def find_phone(self, phone):
        for i in self.phones:
            if str(i) == phone:
                return phone
    def add_birthday(self, birthday):
         self.birthday = Birthday(birthday)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday}"

class AddressBook(UserDict):
    def add_record(self, record):
         self.data[record.name.value] = record
    def find(self, name):
         return self.data.get(name)
    def delete(self, name):
         del self.data[name]
    def get_upcoming_birthdays(self):
        tdate = dtdt.today().date()
        birthdays = []
        for record in self.data.values():
            if record.birthday:
                bdate = record.birthday.date
                year_now = tdate.year
                bdate_this_year = bdate.replace(year=year_now)
                week_day = bdate_this_year.isoweekday()
                days_between = (bdate_this_year - tdate).days
                if 0 <= days_between < 7:
                    if week_day < 6:
                        birthdays.append({"name": record.name.value, 'congratulation_date': bdate_this_year.strftime("%d.%m.%Y")})
                    else:
                        if (bdate_this_year + dt.timedelta(days=(7-week_day))).isoweekday() == 1:
                            new_date = (bdate_this_year + dt.timedelta(days=(7-week_day)))
                            birthdays.append({'name': record.name.value, 'congratulation_date': new_date.strftime("%d.%m.%Y")})
                        elif (bdate_this_year + dt.timedelta(days=(8-week_day))).isoweekday() == 1:
                            new_date = (bdate_this_year + dt.timedelta(days=(8-week_day)))
                            birthdays.append({'name': record.name.value, 'congratulation_date': new_date.strftime("%d.%m.%Y")})
        return birthdays
def input_error(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Enter correct phone and name or birthday have invalid date format. Use DD.MM.YYYY"
        except IndexError:
            return "Enter the argument for the command"
        except KeyError:
            return "Enter correct user name from contacts"
    return inner
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args
@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)                             
    return message
@input_error
def change_phone(args, book: AddressBook):
    name, phone, new_phone, *_ = args
    record = book.find(name)
    record.edit_phone(phone, new_phone)
    return "Phone was changed"
@input_error
def show_phone(args, book):
    name, *_ = args
    return str(book[name]) 
def show_all(book: AddressBook): 
    all_contacts = []
    for name, record in book.items():
        all_contacts.append(str(record))
    for contact in all_contacts:
        print(contact)
@input_error
def add_birthday(args, book: AddressBook):                  
    name, date, *_ = args                                 
    record = book.find(name)
    if record:
        record.add_birthday(date)
        message = "Birthday added"
    else:
        record = Record(name)
        record.add_birthday(date)
        book.add_record(record)
        message = "Contact added"
    return message
@input_error
def show_birthday(args, book: AddressBook):
    name, *_ = args
    return str(book[name].birthday)
def birthdays(book: AddressBook):
    return book.get_upcoming_birthdays()
def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()
@input_error
def main():
    book = load_data()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            show_all(book)
        elif command == "change":
            print(change_phone(args, book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(book))
        else:
            print("Invalid command.")
    save_data(book)

if __name__ == "__main__":
    main()