import csv
import random
import time

def benchmark_test(csv_file):
    millis = int(round(time.time() * 1000))
    print(csv_file)
    random.seed(a = millis)
    with open(csv_file, newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        data=[row for row in csv_reader]
        results = [row[11] for row in data]
        count_for_0 = results.count('0')
        count_for_1 = results.count('1')
        count_for_2 = results.count('2')
        print(count_for_0, count_for_1, count_for_2)
        correct_prediction = 0
        correct_prediction_for_0 = 0
        correct_prediction_for_1 = 0
        correct_prediction_for_2 = 0
        for result in results:
            random_num = random.randint(1, len(results))
            if random_num<=count_for_0:
                predict = '0'
            elif random_num<=count_for_0+count_for_1:
                predict = '1'
            else:
                predict = '2'
            if predict == result:
                if predict =='0':
                    correct_prediction_for_0+=1
                elif predict =='1':
                    correct_prediction_for_1+=1
                else:
                    correct_prediction_for_2+=1
            
        # print("for 0: "+str(correct_prediction_for_0))
        # print(correct_prediction_for_0/count_for_0)
        # print("for 1: "+str(correct_prediction_for_1))
        # print(correct_prediction_for_1/count_for_1)
        # print("for 2: "+str(correct_prediction_for_2))
        # print(correct_prediction_for_2/count_for_2)
        correct_prediction = correct_prediction_for_0+correct_prediction_for_1+correct_prediction_for_2
        print("for all: "+str(correct_prediction))
        print(correct_prediction/len(results))


if __name__ == '__main__':
    for i in range(1,46):
        benchmark_test('resource/preprocess-data-'+str(i)+'.csv')