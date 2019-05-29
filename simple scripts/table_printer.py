import pprint

tableData = [['apples', 'oranges', 'cherries', 'banana', 'pineapple'],
             ['Alice', 'Bob', 'Carol', 'David', 'Charlie'],
             ['dogs', 'cats', 'moose', 'goose', 'rats']]
lenData = []
i = 0

for element in tableData:
    lenData.append([])
    for item in element:
        lenData[i].append(len(item))
    lenData[i].sort(reverse=True)
    lenData[i] = lenData[i][0]
    i += 1


for i in range(len(tableData[0])):
    for j in range(len(tableData)):
        print(tableData[j][i].rjust(lenData[j]), end=' ')
    print()
