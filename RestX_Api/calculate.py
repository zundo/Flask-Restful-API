# Python 3: Fibonacci series up to n
def fib():
    n = int(input("give first number to a : "))
    a, b = 0, 1
    while a < n:
        print(a, end=' ')
        a, b = b, a + b
    print()


fib()


def syracuse():
    a = int(input("give first number to a : "))
    if a == 0:
        print(str(a) + ' est un nombre nul')
        return a
    elif a == 1:
        print("Can not be calculated as it is equal to 1")
    while a > 1:
        if a % 2 == 0:
            a = int(a / 2)
        else:
            a = a * 3 + 1
        print(a, end=' ')


syracuse()
