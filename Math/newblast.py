import time 
from multiprocessing import Pool
import itertools
def fact(n):
    if n==1:
        return 1
    else:
        a=n*fact(n-1)
        return a

def divid(start ,end):
    m=1
    for i in range(start,end+1):
        m=m*i
    return m

pool=Pool()

a=time.time()
res=fact(100)
print (res)
print ("Time spent calculating factorial",(time.time()-a)*60)

a=time.time()
L = pool.starmap(divid,[(1,25),(26,50),(51,75),(76,100)] )

m=1
for i in list(L):
    m=m*i
print ("Result is",m)

print("Time spent calculating factorial using multiprocessing",(time.time()-a)*60)
