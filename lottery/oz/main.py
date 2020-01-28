from probability import calculate
from math import factorial
import csv

def to_csv():
    f7=factorial(7)
    sample_size=5000
    for j in range(8, 21):
        results = []
        for i in range(10, 101, 10):
            result = calculate('system'+str(j), i, sample_size)
            results.append(result)

        with open('output/system-ticket-probability.csv', 'a', newline='') as csv_file:
            f = csv.writer(csv_file, delimiter=',')
            row = ['compare different ticket size of the same system ticket']
            f.writerow(row)
            row =['system'+str(j)]
            f.writerow(row)
            row = ['ticke size']+[i for i in range(10,101,10)]
            f.writerow(row)
            row = ['average prize']+[r['average_prize'] for r in results]
            f.writerow(row)
            row = ['pstd prize']+[r['pstd_prize'] for r in results]
            f.writerow(row)
            row = ['highest division']+[r['highest_division'] for r in results]
            f.writerow(row)
        csv_file.close()

if __name__ =='__main__':
    to_csv()