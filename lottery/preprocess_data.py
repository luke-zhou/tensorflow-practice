import csv

def preproces(csv_file, test_num):
    test_number = str(test_num)
    with open(csv_file, newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        results=[row for row in csv_reader]
        # print(results)
        with open('resource/preprocess-data-'+test_number+'.csv', 'w', newline='') as data_csv_file:
            data_file = csv.writer(data_csv_file, delimiter=',')

            for i in range(1, len(results)):
                row =[results[i][0], results[i][1]]
                for j in range(2, 11):
                    row.append(results[i-1][j])
                
                if test_number in results[i]:
                    index = results[i].index(test_number)
                    if index >=2 and index <=8:
                        row.append('2')
                    else:
                        row.append('1')
                else:
                    row.append('0')
                data_file.writerow(row)
        data_csv_file.close()   

if __name__ == '__main__':
    for i in range(1,46):
        preproces('resource/Ozlotto-latest.csv', i)