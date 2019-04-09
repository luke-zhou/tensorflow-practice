import pandas as pd 
import numpy as np
# import matplotlib
# matplotlib.use('TkAgg')
# import matplotlib.pyplot as plt
import time

def main():
    print('main')
    lottery_df = pd.read_csv('resource/Ozlotto-latest.csv')
    result = calculate_latest_result(lottery_df)
    # print(result)
    display_result(result)

def generate_histogram(df, column, bins=[0, 1, 2, 3]):
    histogram= np.histogram(np.array(df[column]), bins)
    # print(column)
    # print(histogram)
    return histogram

def get_potential_num(histogram_mod, histogram_divide):
    bin_mod = get_bin_for_largest_value(histogram_mod)
    bin_divide = get_bin_for_largest_value(histogram_divide)
    # print('largest bins', bin_mod, bin_divide)
    return [i for i in range(1,46) if i%3 == bin_mod and int((i-1)/15)==bin_divide]

def get_potential_excludes(histogram_mod, histogram_divide):
    bin_mod = get_bin_for_smallest_value(histogram_mod)
    bin_divide = get_bin_for_smallest_value(histogram_divide)
    # print('smallest bins', bin_mod, bin_divide)
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

def calculate_latest_result(lottery_df):
    # print(lottery_df)
    # print(lottery_df.shape)
    # print(lottery_df.describe())
    result = {}

    for i in range(1, 8):
        column = 'num'+str(i)
        # print(column)
        # print(lottery_df[column])
        lottery_df[column+'%3'] = lottery_df[column]%3
        lottery_df[column+'/3'] = ((lottery_df[column]-1)/15).apply(np.int64)
        
        histogram_mod = generate_histogram(lottery_df, column+'%3')
        histogram_divide = generate_histogram(lottery_df, column+'/3')
        potential_nums = get_potential_num(histogram_mod, histogram_divide)
        potential_excludes = get_potential_excludes(histogram_mod, histogram_divide)
        result[column] = {
            'histogram_mod': histogram_mod,
            'histogram_divide': histogram_divide,
            'potential_nums': potential_nums,
            'potential_excludes': potential_excludes
        }
        # print(column)
        # print('potential_nums', potential_nums)
        # print('potential_excludes', potential_excludes)
        # print(lottery_df[column+'%3'])
        # print(lottery_df[column+'/3'])

    for i in range(1, 3):
        column = 'sup'+str(i)
        # print(column)

        # print(lottery_df[column])
        lottery_df[column+'%3'] = lottery_df[column]%3
        lottery_df[column+'/3'] = ((lottery_df[column]-1)/15).apply(np.int64)
        
        histogram_mod = generate_histogram(lottery_df, column+'%3')
        histogram_divide = generate_histogram(lottery_df, column+'/3')
        potential_nums = get_potential_num(histogram_mod, histogram_divide)
        potential_excludes = get_potential_excludes(histogram_mod, histogram_divide)
        result[column] = {
            'histogram_mod': histogram_mod,
            'histogram_divide': histogram_divide,
            'potential_nums': potential_nums,
            'potential_excludes': potential_excludes
        }
        # print(column)
        # print('potential_nums', potential_nums)
        # print('potential_excludes', potential_excludes)


        # print(lottery_df[column+'%3'])
        # print(lottery_df[column+'/3'])
    return result

def display_result(result):
    for key, value in result.items():
        print(key)
        for sub_key, sub_value in value.items():
            print(sub_key, sub_value)

def verify(num):
    lottery_df = pd.read_csv('resource/Ozlotto-latest.csv')
    for i in range(num):
        last_draw = lottery_df.iloc[-1]
        # print(last_draw)
        # print(last_draw.index)
        # print(last_draw.name)
        lottery_df = lottery_df.drop([last_draw.name])
        # print(lottery_df.describe())
        # print(lottery_df.tail(5))
        result = calculate_latest_result(lottery_df)
        include_score = calculate_include_score(last_draw, result)
        exclude_score = calculate_exclude_score(last_draw, result)
        print(last_draw['draw_number'], include_score, exclude_score)    

def calculate_include_score(draw, statistic):
    # print(draw)
    nums = np.array(draw.drop(['draw_number','date']))
    # print(nums)
    result = [num in includes for num, includes in zip(nums, [value['potential_nums'] for value in statistic.values()])]
    # print(result)
    return len(list(filter(lambda x: x, result)))

def calculate_exclude_score(draw, statistic):
    # print(draw)
    nums = np.array(draw.drop(['draw_number','date']))
    # print(nums)
    result = [num in excludes for num, excludes in zip(nums, [value['potential_excludes'] for value in statistic.values()])]
    # print(result)
    return len(list(filter(lambda x: x, result)))

if  __name__  == '__main__':
    # verify(20)
    main()
