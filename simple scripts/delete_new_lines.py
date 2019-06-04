#! python3
# Mehmet Hatip

def main():
    fname = "text.txt"
    new_list = []
    with open(fname) as fin:
        for line in fin:
            stripped = line.strip()
            if (stripped.endswith('.') or stripped.endswith('?') or
                stripped.endswith(':') or stripped.endswith('~') or
                stripped.endswith('!')):
    
                new_list.append(stripped.strip('~') + '\n')
            elif stripped != '':
                new_list.append(stripped + ' ')
    print(''.join(new_list))

if __name__ == '__main__':
    main()