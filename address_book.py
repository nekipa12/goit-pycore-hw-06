from collections import UserDict


class Field:
    """Базовий клас для полів запису."""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    """Ім'я контакту. Обов'язкове поле, порожнім бути не може."""

    def __init__(self, value):
        value = str(value).strip()
        if not value:
            raise ValueError("Name cannot be empty.")
        super().__init__(value)


class Phone(Field):
    """Номер телефону. Приймаємо тільки рядок рівно з 10 цифр."""

    def __init__(self, value):
        value = str(value).strip()
        if not (value.isdigit() and len(value) == 10):
            raise ValueError(
                f"Invalid phone number '{value}': "
                "must contain exactly 10 digits."
            )
        super().__init__(value)


class Record:
    """Запис у книзі контактів: ім'я та список телефонів."""

    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone: str):
        """Додає телефон до запису. Той самий номер двічі не додаємо."""
        if self.find_phone(phone) is not None:
            raise ValueError(f"Phone {phone} already exists.")
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str):
        """Видаляє телефон із запису."""
        phone_obj = self.find_phone(phone)
        if phone_obj is None:
            raise ValueError(f"Phone {phone} not found.")
        self.phones.remove(phone_obj)

    def edit_phone(self, old_phone: str, new_phone: str):
        """Замінює старий номер на новий."""
        phone_obj = self.find_phone(old_phone)
        if phone_obj is None:
            raise ValueError(f"Phone {old_phone} not found.")
        if new_phone != old_phone and self.find_phone(new_phone) is not None:
            raise ValueError(f"Phone {new_phone} already exists.")
        # якщо новий номер некоректний, Phone кине ValueError
        # і старий номер залишиться на місці
        new_phone_obj = Phone(new_phone)
        index = self.phones.index(phone_obj)
        self.phones[index] = new_phone_obj

    def find_phone(self, phone: str):
        """Повертає об'єкт Phone за номером або None, якщо такого немає."""
        for phone_obj in self.phones:
            if phone_obj.value == phone:
                return phone_obj
        return None

    def __str__(self):
        phones = "; ".join(p.value for p in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones}"


class AddressBook(UserDict):
    """Книга контактів. Ключ - ім'я контакту, значення - об'єкт Record."""

    def add_record(self, record: Record):
        """Додає запис до книги."""
        name = record.name.value
        if name in self.data:
            raise ValueError(f"Contact {name} already exists.")
        self.data[name] = record

    def find(self, name: str):
        """Повертає запис за ім'ям або None, якщо контакту немає."""
        return self.data.get(name)

    def delete(self, name: str):
        """Видаляє запис за ім'ям."""
        if name not in self.data:
            raise KeyError(f"Contact {name} not found.")
        del self.data[name]

    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())


if __name__ == "__main__":
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону в записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # John: 5555555555

    # Видалення запису Jane
    book.delete("Jane")
    print(book)  # у книзі лишився тільки John

    # Перевірка валідації: некоректний номер у запис не потрапляє
    try:
        john.add_phone("12345")
    except ValueError as error:
        print(f"Error: {error}")
    print(john)
