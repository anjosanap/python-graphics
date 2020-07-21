import plotly.express as px
import pandas as pd
import random
from faker import Faker

salary_wom = []
salary_men = []
fnames = []

fake = Faker()

def salary():
    return random.randint(845, 100000)

def names():
    return fake.name()

for i in range(0, 80):
    salary_wom.append(salary())
    salary_men.append(salary())
    fnames.append(names())

n_fake = len(fnames)

df = pd.DataFrame(dict(nome= fnames*2, salario=salary_men + salary_wom, genero=["homem"]*n_fake + ["Mulher"]*n_fake))

fig = px.scatter(df, x="salario", y="nome", color="genero",
                 title="Salarios Homens e Mulheres",
                 labels={"salario":"Salario Anual"})

fig.show()