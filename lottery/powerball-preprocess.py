import csv
from datetime import datetime

def preproces_powerball(csv_file):
    with open(csv_file, newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        next(csv_reader, None)
        results = [row for row in csv_reader]
        counts = [0 for i in range(21)]
        last_time = [0 for i in range(21)]

        with open('resource/preprocess-data-powerball.csv', 'w', newline='') as data_csv_file:
            data_file = csv.writer(data_csv_file, delimiter=',')
            data_file.writerow('this is header')
            for r in results:
                data_file.writerow([r[1]]+counts[1:]+last_time[1:]+[r[-1]])
                powerball = int(r[-1])
                counts[powerball] = counts[powerball]+1
                last_time = [0 if n==0 else n+1 for n in last_time]
                last_time[powerball] = 1
        data_csv_file.close()
        # print(results)
        # with open('resource/preprocess-data-'+test_number+'.csv', 'w', newline='') as data_csv_file:
        #     data_file = csv.writer(data_csv_file, delimiter=',')
        #     data_file.writerow(lotto_data.CSV_COLUMN_NAMES)
        #     counts = [ 0 for i in range(20)]

        #     for i in range(tracing_back_count, len(results)):
        #         row = [results[i][0]]
        #         row.extend(generate_date_entry(results[i][1]))

        #         # adding tracing back draws
        #         for j in range(10, 0, -1):
        #             row.extend(results[i-j][2:11])
        #         row.append(generate_result_category(test_number, results[i]))
        #         data_file.writerow(row)
        # data_csv_file.close()

def preproces_powerball_odd_even(csv_file):
    with open(csv_file, newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        next(csv_reader, None)
        results = [row for row in csv_reader]
        counts = [0 for i in range(2)]
        last_time = [0 for i in range(2)]
    csvfile.close()

    with open('resource/preprocess-data-powerball.csv', 'w', newline='') as data_csv_file:
        data_file = csv.writer(data_csv_file, delimiter=',')
        data_file.writerow([1,2,3,4,5,'result'])
        for r in results:
            powerball = int(r[-1])%2
            data_file.writerow([r[1]]+counts+last_time+[powerball])
            counts[powerball] = counts[powerball]+1
            last_time = [0 if n==0 else n+1 for n in last_time]
            last_time[powerball] = 1
    data_csv_file.close()

if __name__ == '__main__':
    # preproces_powerball('resource/powerball.csv')
    preproces_powerball_odd_even('resource/powerball.csv')
