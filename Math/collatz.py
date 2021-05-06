def collatz(n):
    while n > 1:
        print(n, end=' ')
        if (n % 2):
            # n é ímpar
            n = 3*n + 1
        else:
            # n é par
            n = n//2
    print(1, end='')
 
 
n = int(input('Coloque o valor de n: '))
print('Sequência: ', end='')
collatz(n)