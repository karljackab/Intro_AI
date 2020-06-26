import csv

def parse_iris():
    data = [['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'y']]
    with open('iris.data', 'r') as f:
        for row in f.readlines():
            row = row.split(',')
            row[-1] = row[-1].strip()
            if row[-1] == 'Iris-setosa':
                row[-1] = 0
            elif row[-1] == 'Iris-versicolor':
                row[-1] = 1
            elif row[-1] == 'Iris-virginica':
                row[-1] = 2
            else:
                continue
            row = list(map(lambda x: float(x), row))
            row[-1] = int(row[-1])
            data.append(row)
    with open('iris.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(data)

def parse_wine():
    data = [['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'I', 'K', 'L', 'y']]
    with open('wine.data', 'r') as f:
        for row in f.readlines():
            row = row.split(',')
            row[-1] = row[-1].strip()
            row.append(row[0])
            row = list(map(lambda x: float(x), row))
            row[-1] = int(row[-1])
            data.append(row)
    with open('wine.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(data)

def parse_ionosphere():
    data = []
    data.append(list(range(34)))
    data[-1].append('y')
    with open('ionosphere.data', 'r') as f:
        for row in f.readlines():
            row = row.split(',')
            row[-1] = row[-1].strip()
            if row[-1] == 'g':
                row[-1] = 1
            elif row[-1] == 'b':
                row[-1] = 0
            else:
                continue
            row = list(map(lambda x: float(x), row))
            row[-1] = int(row[-1])
            data.append(row)
    with open('ionosphere.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(data)

parse_ionosphere()