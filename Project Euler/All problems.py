#! python3
# Project Euler Problems (projecteuler.net) by Mehmet Hatip

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

problem3()
