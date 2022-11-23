import unicodedata

def clean_name(name):

    name = name.lower()
    trans_tab = dict.fromkeys(map(ord, u'\u0301\u0308'), None)
    name = unicodedata.normalize('NFKC', unicodedata.normalize('NFKD', name).translate(trans_tab))
    name = name.replace(' ','_')
    name = name.replace('ñ','n')
    name = name.replace('#','no')

    # cambiar numero a letra si el primer caracter es un número
    try:
        number = int(name[0])
    
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

        string_of_number = switcher.get(number,"")

        if(number>=1 or number <=9):
            name = name[1:]
            name = string_of_number + name

    except:
        pass

    return name


def rename_colum(dframe):
    f = open("titles.txt","w+")
    for column in dframe.columns:
        dframe.rename(columns={
            column:clean_name(column)
        },inplace=True)
        f.write(clean_name(column))
        f.write('\n')
