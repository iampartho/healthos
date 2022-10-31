import re


def number_verification(number):
    pattern = re.compile('(\+88|0088)?01\d{9}$')
    return pattern.match(number)


def verify_secondary_numbers(secondary_numbers):
    pattern = re.compile('(\+88|0088)?01\d{9}$')
    all_secondary_numbers = []
    for each_number in secondary_numbers:
        if pattern.match(each_number):
            all_secondary_numbers.append(each_number)
        else:
            continue
    return all_secondary_numbers
