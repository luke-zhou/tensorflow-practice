import csv
from datetime import datetime
from functools import reduce

tracing_back_count = 10


def preproces_one_num(csv_file, test_num):
    test_number = str(test_num)
    with open(csv_file, newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        results = [row for row in csv_reader]
        # print(results)
        with open('resource/preprocess-data-'+test_number+'.csv', 'w', newline='') as data_csv_file:
            data_file = csv.writer(data_csv_file, delimiter=',')
            data_file.writerow(lotto_data.CSV_COLUMN_NAMES)

            for i in range(tracing_back_count, len(results)):
                row = [results[i][0]]
                row.extend(generate_date_entry(results[i][1]))

                # adding tracing back draws
                for j in range(10, 0, -1):
                    row.extend(results[i-j][2:11])
                row.append(generate_result_category(test_number, results[i]))
                data_file.writerow(row)
        data_csv_file.close()


def generate_date_entry(date_str):
    entries = [date_str]
    draw_datetime = datetime.strptime(date_str, '%Y%m%d')
    draw_date = draw_datetime.date()
    entries.append(draw_date.year)
    entries.append(draw_date.month)
    entries.append(draw_date.day)
    return entries


def generate_result_category(test_num, result_list):
    if test_num in result_list:
        index = result_list.index(test_num)
        if index >= 2 and index <= 8:
            return '2'
        else:
            return '1'
    else:
        return '0'


def preproces(file_name):
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        results = [row for row in csv_reader]
        print(results)

def nGroup(list, n):
    for i in range(len(list)):
        if i+n >= len(list):
            yield None
        else:
            result = list[i:i+n]
            hasNone = reduce((lambda x,y: x or y), map((lambda x: x is None),result))
            yield None if hasNone else result


if __name__ == '__main__':
    preproces('../data/test-data.csv')
