import random
import names
import pycountry
import pandas as pd
import xlsxwriter
import os

quantidade = int(os.environ['QUANTIDADE'])

class Deus(object):
    def crie_pessoas(self):
        idade = []
        nome = []
        pais = []
        for i in range(1, quantidade):
                idade.append(random.randint(20, 70)) 
                nome.append(names.get_first_name())
                pais.append(random.choices(list(pycountry.countries))[0].name)

        pessoas = {'nome': nome, 'idade': idade, 'pais': pais}
            
        df = pd.DataFrame(pessoas)
        df.to_excel('./planilha.xlsx', header = False, index = False)

deus = Deus()
deus.crie_pessoas()