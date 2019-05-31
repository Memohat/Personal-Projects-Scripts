#! python3
# Mehmet Hatip

import os, re

def main():
    items = []
    for i in os.listdir():
        if i.endswith('.py') and i != os.path.basename(__file__):
            items.append(i)
    for item in items:
        text = None
        with open(item) as fin:
            text = fin.readlines()
        text = ['    ' + i for i in text]
        print(item + ' edited')
        os.remove(item)
        with open(item, 'w') as fout:
            fout.write("""#! python3\n# Mehmet Hatip\n\ndef main():\n""")
            fout.writelines(text)
            fout.write("""\nif __name__ == '__main__':\n    main()""")

if __name__ == '__main__':
    main()
