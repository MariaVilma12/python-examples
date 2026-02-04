the_numbers = {4, 8, 15, 16, 4, 23, 42, 16, 15, 4, 8}   # Sets ignores duplicates

for number in the_numbers:
    print(number)

the_numbers = {4, 8, 15, 16, 4, 23, 42, 16, 15, 4, 8}



###  Different program
list_of_numbers = list(the_numbers)
list_of_numbers.sort()

for number in list_of_numbers:
    print(number)