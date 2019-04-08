import pandas as pd 
import numpy as np
# import matplotlib
# matplotlib.use('TkAgg')
# import matplotlib.pyplot as plt
import time

def main():
    print('main')
    np.random.seed(int(time.time()))
    lottery_df = pd.read_csv('resource/Ozlotto-latest.csv')
    # print(lottery_df)
    print(lottery_df.shape)
    print(lottery_df.describe())

    for i in range(1, 8):
        column = 'num'+str(i)
        print(column)
        # print(lottery_df[column])
        lottery_df[column+'%3'] = lottery_df[column]%3
        lottery_df[column+'/3'] = ((lottery_df[column]-1)/15).apply(np.int64)
        
        histogram_mod = generate_histogram(lottery_df, column+'%3')
        histogram_divide = generate_histogram(lottery_df, column+'/3')
        potential_nums = get_potential_num(histogram_mod, histogram_divide)
        potential_excludes = get_potential_excludes(histogram_mod, histogram_divide)
        print(column)
        print('potential_nums', potential_nums)
        print('potential_excludes', potential_excludes)
        # print(lottery_df[column+'%3'])
        # print(lottery_df[column+'/3'])

    for i in range(1, 3):
        column = 'sup'+str(i)
        print(column)

        # print(lottery_df[column])
        lottery_df[column+'%3'] = lottery_df[column]%3
        lottery_df[column+'/3'] = ((lottery_df[column]-1)/15).apply(np.int64)
        
        histogram_mod = generate_histogram(lottery_df, column+'%3')
        histogram_divide = generate_histogram(lottery_df, column+'/3')
        potential_nums = get_potential_num(histogram_mod, histogram_divide)
        potential_excludes = get_potential_excludes(histogram_mod, histogram_divide)
        print(column)
        print('potential_nums', potential_nums)
        print('potential_excludes', potential_excludes)


        # print(lottery_df[column+'%3'])
        # print(lottery_df[column+'/3'])
    
    lottery_df.to_csv('resource/oz-latest-statistic.csv')

def generate_histogram(df, column, bins=[0, 1, 2, 3]):
    histogram= np.histogram(np.array(df[column]), bins)
    print(column)
    print(histogram)
    return histogram

def get_potential_num(histogram_mod, histogram_divide):
    bin_mod = get_bin_for_largest_value(histogram_mod)
    bin_divide = get_bin_for_largest_value(histogram_divide)
    print('largest bins', bin_mod, bin_divide)
    return [i for i in range(1,46) if i%3 == bin_mod and int((i-1)/15)==bin_divide]

def get_potential_excludes(histogram_mod, histogram_divide):
    bin_mod = get_bin_for_smallest_value(histogram_mod)
    bin_divide = get_bin_for_smallest_value(histogram_divide)
    print('smallest bins', bin_mod, bin_divide)
    return [i for i in range(1,46) if i%3 == bin_mod or int((i-1)/15)==bin_divide]

def get_bin_for_largest_value(histogram):
    his, bins = histogram
    largest_index = 0
    for i in range(1, len(his)):
        if his[i]> his[largest_index]:
            largest_index = i
        
    return bins[largest_index]

def get_bin_for_smallest_value(histogram):
    his, bins = histogram
    smallest_index = 0
    for i in range(1, len(his)):
        if his[i] < his[smallest_index]:
            smallest_index = i
        
    return bins[smallest_index]

if  __name__  == '__main__':
    main()
