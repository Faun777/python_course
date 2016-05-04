import scipy as scp
import numpy as np


def nazwa(tekst1, tekst2):
    print(tekst1, tekst2)
    myfunction()

def myfunction():
    a = 5.
    print()
    for i in range(1, 100):
        a = a + 1 / (np.sqrt(i))
    print("Moja liczba : " + str(a))
    print(str(i))


def listy():
    a = []
    # b = list[20]
    print(isinstance(a, list))
    # print(isinstance(b,list))
    # print(b)
    print(a)
    for i in range(0, 11):
        a.append(i)
    print(a)


def foryify():
    a = [100, scp.pi, scp.e, 'cos']
    for element in a:
        print(element)
    b = [i ** 2 for i in range(101)]
    print(b)


listy()
a = [1, 2, 3, 'cos', scp.pi, np.pi, np.pi - scp.pi]
print(a)
foryify()
