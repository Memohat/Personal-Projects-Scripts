#! python3
# Project Euler Problems (projecteuler.net) by Mehmet Hatip
import regex, sys, logging, math, pyperclip

def product(mylist):
    total = 1
    for i in mylist:
        total *= i
    assert total != 1, "Product is 1"
    return total


def answer(num):
    print(f'Answer: {num}')
    pyperclip.copy(num)
    print('Copied to clipboard')

def problem1():
    # Sum of multiples of 3 and/or 5 btw 1 and 1000
    print(sum(i for i in range(1000) if i % 3 ==0 or i % 5 == 0))

def problem2():
    # Sum of even numbers in fibonacci sequence starting with 1,2,3,5...
    sequence = [1,2]
    counter = 0
    x = 0
    while True:
        x = sequence[counter] +  sequence[counter+1]
        if x >= 4000000:
            break
        else:
            sequence.append(x)
            counter += 1


    print(sum(i for i in sequence if i % 2 == 0))
    print(sequence)

def problem3():
    # largest prime factor of 600851475143
    num = 600851475143
    factors = []
    i = 2
    while num > 1:
        if num % i == 0:
            num /= i
            factors.append(i)

            print(f"{num} after division by {i}")
        i += 1
    print(factors)

def problem4():
    # Largest palindrome from product of two 3 digit numbers
    multiplier = 900
    nums = {}
    for j in range(multiplier, 1000):
        for i in range(2,1000):
            num = j*i
            str_num = str(num)
            if str_num[::-1] == str_num:
                nums[num] = f'{j} * {i}'
    print(f'{sorted(nums)[-1]} = {nums.get(sorted(nums)[-1])}')

def problem5():
    # smallest positive number that is evenly divisible by numbers from 1 to 20
    num = 2520
    for i in range(20,9,-1):
        for j in range(1, i+1):
            if num % i == 0:
                break
            elif num * j % i == 0:
                print(f'Multiplied {num} by {j} to get ', end='')
                num *=j
                print(f'{num}')

def problem6():
    # difference between the sum of the squares of
    # the first 100 natural numbers and the square of the sum

    sum_of_squares = sum(i**2 for i in range(101))
    square_of_sum = (sum(i for i in range(101)))**2
    answer = -(sum_of_squares - square_of_sum)
    print(answer)
    pyperclip.copy(answer)

def problem7():
    # prime number list generator

    primes = [2]
    i = 2
    while True:
        for prime in primes:
            if i % prime != 0 and prime == primes[-1]:
                primes.append(i)
                print(f'{i} added to primes')
            elif i % prime != 0:
                continue
            break
        i += 1
        if len(primes) >= 10001:
            break
    answer(primes[10000])

def problem8():
    # thirteen adjacent digits in the number that have the greatest product
    num = """
    73167176531330624919225119674426574742355349194934
    96983520312774506326239578318016984801869478851843
    85861560789112949495459501737958331952853208805511
    12540698747158523863050715693290963295227443043557
    66896648950445244523161731856403098711121722383113
    62229893423380308135336276614282806444486645238749
    30358907296290491560440772390713810515859307960866
    70172427121883998797908792274921901699720888093776
    65727333001053367881220235421809751254540594752243
    52584907711670556013604839586446706324415722155397
    53697817977846174064955149290862569321978468622482
    83972241375657056057490261407972968652414535100474
    82166370484403199890008895243450658541227588666881
    16427171479924442928230863465674813919123162824586
    17866458359124566529476545682848912883142607690042
    24219022671055626321111109370544217506941658960408
    07198403850962455444362981230987879927244284909188
    84580156166097919133875499200524063689912560717606
    05886116467109405077541002256983155200055935729725
    71636269561882670428252483600823257530420752963450
    """
    products = []
    num = regex.sub(r'\s', '', num)
    i = 0
    j = 13
    while True:
        digits = list(map(int, num[i:j]))
        print(digits)
        products.append(product(digits))
        i += 1
        j += 1
        if j >= len(num):
            break
    answer(sorted(products)[-1])

def problem9():
    # Pythagorean triplet for which a + b + c = 1000
    triplet_list = []
    c = 5
    while True:
        for a in range(1,c):
            b = math.sqrt((c ** 2) - (a ** 2))
            if int(b) == b and a**2 + b**2 == c**2:
                a, b, c = int(a), int(b), int(c)
                triplet_list.append((a,b,c))
                print(f'Pythagorean Triple: {a} {b} {c}, Sum: {a+b+c}')
                if a + b + c == 1000:
                    answer(product([a,b,c]))
                    break
        if a + b + c == 1000:
            break
        c += 1



def main():
    logging.basicConfig()
    message = 'Enter number of problem (e to exit): '
    num = sys.argv[1] if len(sys.argv) > 1 else input(message)
    while True:
        exits = ['e','exit']
        if num in exits:
            break
        try:
            if not regex.search(r'^\d+$', num):
                raise ValueError
            eval(f'problem{num}()')
        except Exception as e:
            print(e)
        num = 'e'#input(message)


if __name__ == '__main__':
    main()
