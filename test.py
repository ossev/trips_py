import os


def probar():
    word = '5sdfsdfg'

    number = int(word[0])

    switcher = {
        1: 'primer',
        2: 'segundo',
        3: 'tercer',
        4: 'cuarto',
        5: 'quinto',
        6: 'sexto',
        7: 'septimo',
        8: 'octavo',
        9: 'noveno'
    }

    string_of_number = switcher.get(number,"_")

    if(number>=1 or number <=9):
        word = word[1:]
        word = string_of_number + word
    print(f'{word}')

if __name__ == '__main__':
    probar()