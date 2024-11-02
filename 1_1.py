# 1 Электронная почта
class EmailMasker:
    def __init__(self, mask_char="x"):
        self.mask_char = mask_char  # Символ для экранирования

    def mask(self, email):
        name, domain = email.split("@")  # Разделяем почтовый ящик на имя и домен
        masked_name = self.mask_char * len(name)  # Замещаем символы в имени почтового ящика
        return f"{masked_name}@{domain}"  # Возвращаем экранированный email


# Создаем объект класса с символом маскирования "x"
email_masker = EmailMasker()
masked_email = email_masker.mask("test@test.com")
print(masked_email)  # Ожидаемый результат: xxxx@test.com

# Создаем объект класса с символом маскирования "*"
email_masker_star = EmailMasker("*")
masked_email_star = email_masker_star.mask("davewalker@mail.com")
print(masked_email_star)  # Ожидаемый результат: ********@mail.com


# 2 Номер телефона
class PhoneNumberMasker:
    def __init__(self, mask_char="x", mask_length=3):
        self.mask_char = mask_char  # Символ для экранирования
        self.mask_length = mask_length  # Количество символов для маскирования

    def mask(self, phone_number):
        normalized_number = " ".join(phone_number.split())  # Убираем лишние пробелы
        visible_part = normalized_number[:-self.mask_length]  # Видимая часть
        masked_part = self.mask_char * self.mask_length  # Маскированная часть
        return f"{visible_part}{masked_part}"


# Создаем объект класса с символом маскирования "x" и длиной маскирования 3
phone_masker = PhoneNumberMasker()
masked_phone = phone_masker.mask("+7 694 201 337")
print(masked_phone)  # Ожидаемый результат: +7 694 201 xxx

# Создаем объект класса с символом маскирования "*" и длиной маскирования 5
phone_masker_custom = PhoneNumberMasker("*", 5)
masked_phone_custom = phone_masker_custom.mask("++7 694 201 337")
print(masked_phone_custom)  # Ожидаемый результат: +7 694 2** ***


# 3 Skype
class SkypeMasker:
    def __init__(self, mask_char="x"):
        self.mask_char = mask_char  # Символ для экранирования

    def mask(self, skype_string):
        # Проверяем, является ли строка HTML-ссылкой
        if "href=\"skype:" in skype_string:
            # Разделяем строку на части и заменяем логин на 'xxx' без изменения остального текста
            prefix, skype_id = skype_string.split("href=\"skype:")[0:2]
            skype_id, suffix = skype_id.split("?call\">", 1)
            masked_id = f"{self.mask_char * 3}"  # Экранируем логин как 'xxx'
            return f'{prefix}href="skype:{masked_id}?call">{suffix}'

        # Для обычного логина Skype в формате 'skype:логин'
        if skype_string.startswith("skype:"):
            return f"skype:{self.mask_char * 3}"  # Экранируем логин как 'xxx'

        # Если формат строки не распознан, возвращаем оригинальную строку
        return skype_string


# Создаем объект класса с символом маскирования "x"
skype_masker = SkypeMasker()

# Маскируем логин Skype в обычной строке
masked_skype = skype_masker.mask("skype:alex.max")
print(masked_skype)  # Ожидаемый результат: skype:xxx

# Маскируем логин Skype в HTML-ссылке
masked_skype_link = skype_masker.mask('<a href="skype:alex.max?call">skype</a>')
print(masked_skype_link)  # Ожидаемый результат: <a href="skype:xxx?call">skype</a>
