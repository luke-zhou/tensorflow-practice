from probability import calculate
from math import factorial
import csv

def to_csv():
    f7=factorial(7)
    sample_size=5000
    for j in range(8, 21):
        ticket_size = int(factorial(j)/(f7*factorial(j-7)))
        results = []
        benchmark_results=[]
        range_up_bound = max(2,14-j)
        print('range_up_bound: '+str(range_up_bound))
        for i in range(1, range_up_bound):
            result = calculate('system'+str(j), i*10, sample_size)
            results.append(result)

        for i in range(1, range_up_bound):
            result = calculate('simple', i*10*ticket_size, sample_size)
            benchmark_results.append(result)

        with open('output/system-ticket-probability.csv', 'a', newline='') as csv_file:
            f = csv.writer(csv_file, delimiter=',')
            row =['system'+str(j)]
            f.writerow(row)
            row = ['ticke size']+[i for i in range(10,101,10)]
            f.writerow(row)
            row = ['average prize']+[r['average_prize'] for r in results]
            f.writerow(row)
            row = ['benchmark average prize']+[r['average_prize'] for r in benchmark_results]
            f.writerow(row)
            row = ['pstd prize']+[r['pstd_prize'] for r in results]
            f.writerow(row)
            row = ['benchmark pstd prize']+[r['pstd_prize'] for r in benchmark_results]
            f.writerow(row)
            row = ['highest division']+[r['highest_division'] for r in results]
            f.writerow(row)
            row = ['benchmark highest_division']+[r['highest_division'] for r in benchmark_results]
            f.writerow(row)
            row = ['total_jackpot']+[r['total_jackpot'] for r in results]
            f.writerow(row)
            row = ['benchmark total_jackpot']+[r['total_jackpot'] for r in benchmark_results]
            f.writerow(row)
            row = ['jackpot_rate']+[r['jackpot_rate'] for r in results]
            f.writerow(row)
            row = ['benchmark jackpot_rate']+[r['jackpot_rate'] for r in benchmark_results]
            f.writerow(row)
            row = ['samples_with_jackpot']+[r['samples_with_jackpot'] for r in results]
            f.writerow(row)
            row = ['benchmark samples_with_jackpot']+[r['samples_with_jackpot'] for r in benchmark_results]
            f.writerow(row)
            row = ['samples_with_jackpot_rate']+[r['samples_with_jackpot_rate'] for r in results]
            f.writerow(row)
            row = ['benchmark samples_with_jackpot_rate']+[r['samples_with_jackpot_rate'] for r in benchmark_results]
            f.writerow(row)
        csv_file.close()

if __name__ =='__main__':
    to_csv()