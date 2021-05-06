import random
list = []


def generator(rmin, rmax):
    for i in range(10):
        r = random.randint(rmin, rmax)
        if r not in list:
            list.append(r)


print(list)
