import csv

tracing_back_count = 5

def preproces(file_name):
    group_records =[]
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        #skip header 
        next(csv_reader, None)
        results = [row for row in csv_reader]
        for group in n_group(results, tracing_back_count+1):
            if group is not None:
                group_records.append(group)
    csv_file.close()
    # print(group_records)
    with open('../trainingdata/preprocess-'+ str(tracing_back_count*5) +'.csv', 'w', newline='') as output_csv_file:
        writer = csv.writer(output_csv_file, delimiter=',')
        for group in group_records:
            features = generate_features(group)
            result = generate_result(group[tracing_back_count]) 
            row = [*features, result]
            writer.writerow(row)

    output_csv_file.close()

## list example: [1999-01-03,23.443001,23.443001,22.776600,22.776600,22.776600,1050290]
def generate_result(list):
    return 1 if float(list[4]) > float(list[1]) else 0

## group example: [ [1,2,3,4,5,6], 
#                   [2,3,4,5,6,7],
#                   [3,4,5,6,7,8], 
#                   [8,9,10,11,12,13],
#                   [9,10,11,12,13,14], 
#                   [10,11,12,13,14,15]
#                   ]
def generate_features(group):  
    features =[]
    for i in range(tracing_back_count):
        nums = []
        for num in group[i]:
            try:
                v = float(num)
                nums.append(v)
            except ValueError:
                pass
        if i == 0:
            first_open, first_volumn = nums[0], nums[5]

        open = nums[0]
        high = nums[1]
        low = nums[2]
        close = nums[3]
        feature_sect =[open, high, low, close]

        features.extend([n/first_open for n in feature_sect])
        features.append(nums[5]/first_volumn)
    return features



def n_group(list, n):
    for i in range(len(list)):
        if i+n >= len(list):
            yield None
        else:
            result = list[i:i+n]
            yield result if is_group_valid(result) else None

def is_group_valid(list):
    return not any(any(e=='null' or e =='0' for e in r) for r in list)

if __name__ == '__main__':
    # preproces('../data/test-data.csv')
    preproces('../data/cba-data.csv')
