from oz_verify import verify_ticket
import oz_generator as generator
from statistics import mean, pstdev
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import time

def benchmark(size = 500):
    print("-"*20+" start calculating benchmark "+"-"*20)
    print("testing size is", size)
    test_data = load_data(size)

    test_block(test_data, "random select 45 sets in one ticket", "random_ticket", 45)
    test_block(test_data, "random select 45 sets for one number each in one ticket", "random_ticket_each")
    test_block(test_data, "random select 45 sets which has neighbour numbers in one ticket", "random_ticket_with_neighbout_num", 45)
    test_block(test_data, "random select 45 sets with lower average in one ticket", "random_ticket_with_lower_average", 45)
    test_block(test_data, "random select 45 sets with higher average in one ticket", "random_ticket_with_higher_average", 45)

def test_block(test_data, description, method, args=None):
    print("-"*70)

    print(description)
    result={"results":[]}
    for original_set in test_data:
        method_to_call = getattr(generator, method)
        if args is None:
            ticket = method_to_call()
        else:
            ticket = method_to_call(args)
        verify_result = verify_ticket(original_set, ticket)
        result["results"].append(summarize_verify_result(verify_result))
    display_summary(result)

def display_summary(result):
    average_lst=[result['average'] for result in result['results']]
    pstd_lst=[result['pstd'] for result in result['results']]
    win_time_lst=[result['win_time'] for result in result['results']] 
    win_price_lst=[result['win_price'] for result in result['results']] 

    result['average'] =(mean(average_lst), pstdev(average_lst))
    result['pstd'] =(mean(pstd_lst),pstdev(pstd_lst))
    result['win_time'] =(mean(win_time_lst), pstdev(win_time_lst))
    result['win_price'] =(mean(win_price_lst), pstdev(win_price_lst))
    print('average',result['average'])
    print('pstd',result['pstd'])
    print('win_time',result['win_time'])
    print('win_price',result['win_price'])

def summarize_verify_result(verify_result):
    result_stat={}
    result_stat['average']=verify_result['average_match_count']
    result_stat['pstd']=verify_result['pstd_match_count']
    result_stat['win_time']=verify_result['win_time']
    result_stat['win_price']=verify_result['win_price']
    return result_stat

def load_data(test_size):
    data_df = pd.read_csv('resource/Ozlotto-latest.csv')

    data = np.array(data_df)
    # drop draw no and date
    data = data[:,2:-2]
    print("data size",data.shape)

    _, test_features, _, _ = train_test_split(data, data, test_size = test_size/data.shape[0], random_state = int(time.time()))
    # print('Training Features Shape:', train_features.shape)
    # print('Training Labels Shape:', train_labels.shape)
    print('Testing Features Shape:', test_features.shape)
    # print('Testing Labels Shape:', test_labels.shape)
    return test_features


if __name__ =='__main__':
    benchmark()