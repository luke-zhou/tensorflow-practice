import csv

tracing_back_count = 5

def preproces(file_name):
    group_records =[]
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        results = [row for row in csv_reader]
        for group in nGroup(results, tracing_back_count+1):
            if group is not None:
                group_records.append(group)
    csv_file.close()
    # print(group_records)
    with open('../training_data/preprocess-'+ str(tracing_back_count) +'.csv', 'w', newline='') as output_csv_file:
        writer = csv.writer(output_csv_file, delimiter=',')
        for group in group_records:
            features =[]
            for i in range(tracing_back_count):
                nums = []
                for num in group[i]:
                    try:
                        v = float(num)
                        nums.append(v)
                    except ValueError:
                        pass
            features.extend(generate_features(nums))
            writer.writerow(features)

    output_csv_file.close()
def generate_features(list):  
    open = list[0]
    high = list[1]
    low = list[2]
    close = list[3]
    features =[]
    features.append(open-high)
    features.append(open-low)
    features.append(open-close)
    features.append(high-low)
    features.append(high-close)
    features.append(low-close)
    return [n/open for n in features]


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
