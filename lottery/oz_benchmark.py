from oz_verify import verify_ticket
import oz_generator as generator
from statistics import mean, pstdev
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import time
from oz_rules import rules, random_select_rule

def benchmark(size = 500):
    print("-"*20+" start calculating benchmark "+"-"*20)
    print("testing size is", size)
    test_data = load_data(size)

    test_block(test_data, [random_select_rule()])

    # for rule in rules():
    #     test_block(test_data, [rule])

    for x in rules():
        for y in rules():
            if x["description"] != y["description"]:
                result_x = test_block(test_data, [x])
                result_y = test_block(test_data, [y])
                result = test_block(test_data, [x, y])
                if is_result_good(result, result_x, result_y):
                    display_summary(result)

def is_result_good(result, result_x, result_y):
    if result["results"]:
        items=['average', 'pstd', 'win_time', 'win_price']
        return any([result[item][0] >= (max(result_x[item][0], result_y[item][0])*1.1) for item in items])
    else:
        return False

def test_block(test_data, rules):
    print("-"*70)

    if len(rules)>1:
        print([rule["description"] for rule in rules])
    result={"results":[]}
    for original_set in test_data:
        conditions = [rule["condition"] for rule in rules]
        prefills = [rule["prefill"] for rule in rules]
        ticket = generator.generate_ticket(45, conditions, prefills)
        if ticket:
            verify_result = verify_ticket(original_set, ticket)
            result["results"].append(summarize_verify_result(verify_result))

    if result["results"]: 
        average_lst=[result['average'] for result in result['results']]
        pstd_lst=[result['pstd'] for result in result['results']]
        win_time_lst=[result['win_time'] for result in result['results']] 
        win_price_lst=[result['win_price'] for result in result['results']] 
        result['average'] =(mean(average_lst), pstdev(average_lst))
        result['pstd'] =(mean(pstd_lst),pstdev(pstd_lst))
        result['win_time'] =(mean(win_time_lst), pstdev(win_time_lst))
        result['win_price'] =(mean(win_price_lst), pstdev(win_price_lst))
    # display_summary(result)
    return result

def display_summary(result):
    if result["results"]:
        print('average',result['average'])
        print('pstd',result['pstd'])
        print('win_time',result['win_time'])
        print('win_price',result['win_price'])
    else:
        print("Can't generate besed on these conditions")

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