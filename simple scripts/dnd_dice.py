#! python3
# Mehmet Hatip

import regex, random

def main():

    message = ('Enter dice roll in format \'xdy\' where ' +
    'x is number of die (1-100) and y is sides per dice (2-200): ')

    while True:
        text = input(message)
        try:
            re = regex.search(r'([1-9](\d{1,2})?)d([1-9]([0-9]{1,2})?)', text)
            num_die, sides = re.group(1), re.group(3)
            num_die, sides = int(num_die), int(sides)
            if num_die < 1 or num_die > 100:
                continue
            elif sides < 2 or sides > 200:
                continue
            tosses = []
            for dice in range(num_die):
                tosses.append(random.randint(1, sides))
            print(f'{sum(tosses)}: ', end='')
            for toss in tosses:
                print(f'{toss} ', end='')
            print()
        except:
            continue

if __name__ == '__main__':
    main()
