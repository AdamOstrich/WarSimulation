import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from distfit import distfit

zwroty_us, zwroty_ch = [], []
dl_calosci = 0

przykladowaRzeczywistaWojnaUSA = []
przykladowaRzeczywistaWojnaChina = []

for i in range(1, 21):
    df = pd.read_csv('przebieg_wojny_kol_'+str(i)+'.csv', delimiter=';')
    data_us = np.array(df['USA'])
    data_ch = np.array(df['China'])
    dl_calosci += len(data_us)
    if i == 2:
        przykladowaRzeczywistaWojnaUSA = data_us
        przykladowaRzeczywistaWojnaChina = data_ch
    for i in range(len(data_us) - 1):
        zwroty_us.append((data_us[i + 1] - data_us[i]))
        zwroty_ch.append((data_ch[i + 1] - data_ch[i]))
    plt.plot(data_us)
    # plt.show()
    plt.clf()


for i in range(len(zwroty_us)):
    if np.isnan(zwroty_us[i]):
        zwroty_us[i] = 0
    if np.isnan(zwroty_ch[i]):
        zwroty_ch[i] = 0

for i in range(len(zwroty_us)):
    if zwroty_us[i] > 660000:
        zwroty_us[i] = 660000
    if zwroty_ch[i] > 470000:
        zwroty_ch[i] = 470000

zwroty_us = np.array(zwroty_us)
zwroty_us = zwroty_us[zwroty_us != 0.0]

zwroty_ch = np.array(zwroty_ch)
zwroty_ch = zwroty_ch[zwroty_ch != 0.0]

# dist_us = distfit()
# model_us = dist_us.fit_transform(zwroty_us)

# dist_us.plot()
plt.hist(zwroty_us, density=True, bins=20)
plt.title('Histogram zwrotów USA')
plt.legend()
# plt.show()

plt.clf()

# dist_ch = distfit()
# model_ch = dist_ch.fit_transform(zwroty_ch)

# dist_ch.plot()
plt.hist(zwroty_ch, density=True, bins=20)
plt.title('Histogram zwrotów Chin')
plt.legend()
# plt.show()

wzrost_us = 5000 + 10*8000 + 50*4000 + 15*25000
wzrost_ch = 15000 + 10*6500 + 50*2400 + 15*18000

print(wzrost_us, wzrost_ch, 1 / ((len(zwroty_us)/20) / (dl_calosci/20)))

proces_us = [46110000]
proces_ch = [30170000]

straty_us = []
straty_ch = []

for i in zwroty_us:
    if i < 0: straty_us.append(-i)

for i in zwroty_ch:
    if i < 0: straty_ch.append(-i)

plt.clf()

straty_us, straty_ch = np.array(straty_us), np.array(straty_ch)

dist_us = distfit()
model_us = dist_us.fit_transform(straty_us)
# dist_us.plot()
# plt.hist(straty_us, density=True)
# plt.title("Histogram strat USA")
# plt.legend()
# # plt.show()
#
# plt.clf()
#
dist_ch = distfit()
model_ch = dist_ch.fit_transform(straty_ch)
# dist_ch.plot()
# plt.hist(straty_ch, density=True)
# plt.title("Histogram strat China")
# plt.legend()
# plt.show()

def generowanie_strat_usa(n):
    # X = np.random.pareto(1, size=n)
    # return X * 200000
    X = np.random.exponential(1, size=n) * 1308290

    return X


def generowanie_strat_china(n):
    # X = np.random.pareto(1, size=n)
    # return X * 150000
    X = np.random.exponential(1, size=n) * 610648
    return X

def czas_na_spadek():
    return np.mean(np.random.exponential(scale=3.6, size=1000))

def czy_pierwsza(number):
    if number < 2:
        return False
    for i in range(2, int(number ** 0.5) + 1):
        if number % i == 0:
            return False
    return True

def liczby_pierwsze(n):
    prime_numbers = []
    count = 0
    number = 2
    while count < n:
        if czy_pierwsza(number):
            prime_numbers.append(number)
            count += 1
        number += 1
    return prime_numbers

#print(generowanie_strat_usa(), generowanie_strat_usa())
print(np.mean(straty_us))

#print(generowanie_strat_china(), generowanie_strat_china())
print(np.mean(straty_ch))

print(czas_na_spadek())

def symulacja(n=2000):
    ilosc_strat = int(n / czas_na_spadek())
    # momenty_strat = sorted(np.random.random(size=ilosc_strat) * n)
    liczby_pier = liczby_pierwsze(ilosc_strat)
    dlugosc_strat = max(liczby_pier)
    momenty_strat_wszystkie = sorted(np.random.random(size=dlugosc_strat) * n)
    momenty_strat = []
    print(len(momenty_strat_wszystkie), dlugosc_strat)
    for i in liczby_pier:
        momenty_strat.append(momenty_strat_wszystkie[i - 1])
    straty_us = generowanie_strat_usa(ilosc_strat)
    straty_ch = generowanie_strat_china(ilosc_strat)
    t = np.arange(0, n, 0.01)
    y_us = []
    y_ch = []
    x = []
    index_momentu_straty = 0
    value_us = 46110000
    value_ch = 30170000
    for dt in t:
        if dt >= momenty_strat[index_momentu_straty]:
            value_us -= straty_us[index_momentu_straty]
            value_ch -= straty_ch[index_momentu_straty]
            if index_momentu_straty < len(momenty_strat) - 1:
                index_momentu_straty += 1
        if dt % 50 == 49:
            value_us += 660000
        y_us.append(value_us)
        y_ch.append(value_ch)
        x.append(dt)

        if value_us < 0 or value_ch < 0: break

    return x, y_us, y_ch


plt.clf()

plt.subplot(1, 2, 1)
x_us, y_us, y_ch = symulacja()
plt.plot(x_us, y_us, label='USA')
plt.plot(x_us, y_ch, label='Chiny')
plt.legend()
plt.title('Przykładowa realizacja naszego procesu')

plt.subplot(1, 2, 2)
plt.plot(przykladowaRzeczywistaWojnaUSA, label='USA')
plt.plot(przykladowaRzeczywistaWojnaChina, label='Chiny')
plt.legend()
plt.title('Przykładowa realizacja naszej symulacji (gry)')
plt.show()

plt.clf()

for i in range(1000):
    x_us, y_us, y_ch = symulacja()
    x_us, y_us, y_ch = np.array(x_us), np.array(y_us), np.array(y_ch)
    plt.plot(2*x_us, y_us)
plt.title('1000 symulacji naszego procesu dla USA')
plt.show()

plt.clf()

for i in range(1000):
    x_us, y_us, y_ch = symulacja()
    x_us, y_us, y_ch = np.array(x_us), np.array(y_us), np.array(y_ch)
    plt.plot(2*x_us, y_ch)
plt.title('1000 symulacji naszego procesu dla Chin')
plt.show()

