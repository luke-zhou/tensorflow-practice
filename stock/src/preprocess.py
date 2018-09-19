import csv

tracing_back_count = 5

def preproces(file_name):
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        results = [row for row in csv_reader]
        for group in nGroup(results, tracing_back_count):
            if group is not None:
                print(group)

def nGroup(list, n):
    for i in range(len(list)):
        if i+n >= len(list):
            yield None
        else:
            result = list[i:i+n]
            yield result if isGroupValid(result) else None

def isGroupValid(list):
    return not any(any(e=='null' for e in r) for r in list)

if __name__ == '__main__':
    preproces('../data/test-data.csv')
