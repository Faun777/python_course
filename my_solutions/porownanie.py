import random
def porownaj(a):

    b = []
    print(a)
    for elem in a:
        flag = True
        for belem in b:
            if belem == elem:
                flag = False
                break
            else:
                flag = True
        if flag:
            b.append(elem)
    print(b)

def wytnij(a):
    print("start" + str(a))
    b = a
    for elem in a:
        for elem2 in a:
            if elem==elem2:
                b.remove(elem2)
                print("iteracja" + str(b))
    print("Koniec "+str(b))

def petlawhile():
    flag = True
    while flag:
        # print("Where are my dragons!!!?")
        wczytanie = int(input("Where are my dragons!!!?\t"))
        a = random.randint(1,10)
        # print(isinstance(wczytanie,int))
        # print(isinstance(a,int))
        if a == wczytanie:
            print("There are my dragons!!!")
            flag = False
        print("Some : "+str(a)+"\t"+str(wczytanie))
    pass
my_list = [1, 1, 2, 2, 3, 4, 5, 1, 5, 4, 3, 2, 'cos', 'cos', 'wiecej czegos']
# porownaj(my_list)
# wytnij(my_list)
petlawhile()