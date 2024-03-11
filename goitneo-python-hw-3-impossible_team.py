from datetime import datetime, timedelta, date
from collections import defaultdict
import json

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Name cannot be empty")
        super().__init__(value)

class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Invalid phone number")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise ValueError("Invalid date format. Please use DD.MM.YYYY.")
        super().__init__(value)

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        if not phone.isdigit() or len(phone) != 10:
            raise ValueError("Invalid phone number")
        self.phones.append(Phone(phone))

    def add_birthday(self, birthday):
        try:
            self.birthday = Birthday(birthday)
        except ValueError as e:
            return str(e)

class AddressBook:
    def __init__(self):
        self.data = {}

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        if name in self.data:
            return self.data[name]
        return f"Record {name} not found"

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return f"Record {name} deleted"
        return f"Record {name} not found"

    def get_birthdays_per_week(self):
        current_date = date.today()
        next_week = current_date + timedelta(days=7)
        upcoming_birthdays = []
        for name, record in self.data.items():
            if record.birthday:
                bday = datetime.strptime(record.birthday.value, '%d.%m.%Y').date().replace(year=current_date.year)
                if current_date <= bday < next_week:
                    upcoming_birthdays.append(record)
        return upcoming_birthdays

    def serialize(self, filename):
        with open(filename, 'w') as file:
            data = {'data': self.data}
            json.dump(data, file)

    def deserialize(self, filename):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                self.data = data['data']
        except FileNotFoundError:
            self.data = {}

if __name__ == "__main__":
    book = AddressBook()

    # Load data from a file (if available)
    try:
        book.deserialize('addressbook.json')
    except FileNotFoundError:
        pass

    while True:
        command = input("Enter a command: ").strip().lower()
        if command == 'add':
            name = input("Enter the name: ")
            phone = input("Enter the phone number: ")
            contact = Record(name)
            contact.add_phone(phone)
            book.add_record(contact)
        elif command == 'change':
            name = input("Enter the name: ")
            phone = input("Enter the new phone number: ")
            contact = book.find(name)
            if contact:
                contact.add_phone(phone)
            else:
                print(f"Contact {name} not found.")
        elif command == 'phone':
            name = input("Enter the name: ")
            contact = book.find(name)
            if contact:
                if contact.phones:
                    print(f"Phone numbers for {name}:")
                    for phone in contact.phones:
                        print(phone)
                else:
                    print(f"No phone numbers for {name}.")
            else:
                print(f"Contact {name} not found.")
        elif command == 'all':
            if book.data:
                print("All contacts:")
                for name, record in book.data.items():
                    print(f"{record.name}:")
                    if record.phones:
                        for phone in record.phones:
                            print(f"  Phone: {phone}")
                    if record.birthday:
                        print(f"  Birthday: {record.birthday}")
            else:
                print("No contacts available.")
        elif command == 'add-birthday':
            name = input("Enter the name: ")
            birthday = input("Enter the birthday (in DD.MM.YYYY format): ")
            contact = book.find(name)
            if contact:
                result = contact.add_birthday(birthday)
                print(result)
            else:
                print(f"Contact {name} not found.")
        elif command == 'show-birthday':
            name = input("Enter the name: ")
            contact = book.find(name)
            if contact and contact.birthday:
                print(f"Birthday for {name}: {contact.birthday}")
            else:
                print(f"Birthday for {name} not found.")
        elif command == 'birthdays':
            upcoming_birthdays = book.get_birthdays_per_week()
            if upcoming_birthdays:
                print("Upcoming birthdays:")
                for record in upcoming_birthdays:
                    print(f"{record.name}: {record.birthday}")
            else:
                print("No upcoming birthdays.")
        elif command == 'hello':
            print("Hello!")
        elif command == 'close' or command == 'exit':
            book.serialize('addressbook.json')
            print("Exiting...")
            break
