from oz_verify import verify_ticket
import oz_generator as generator
from statistics import mean, pstdev
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import time
from oz_rules import existing_rules, random_select_rule, impossible_combine, new_rules
import random
import time


millis = int(round(time.time() * 1000))
random.seed(a = millis)

def benchmark(size = 500):
    print("-"*20+" start calculating benchmark "+"-"*20)
    print("testing size is", size)

    data = load_data()

    test_data = random.sample(data, size)

    baseline = test_block(test_data, [random_select_rule()])
    display_summary(baseline)
    print(baseline)

    # for rule in rules():
    #     test_block(test_data, [rule])
    rule_lst = existing_rules()
    new_rule_lst = new_rules()
    skip_combine = impossible_combine()
    # statistics_benchmark(rule_lst, data, size)
    # generator_benchmark(new_rule_lst, rule_lst, skip_combine, data, size)

    # survive_test(rule_lst, data, size)

def split_data(data, size):
    random.shuffle(data)
    train = data[:size] 
    test = data[size:]
    # print(len(train))
    # print(len(test))
    return train, test

def survive_test(rules, data, size):
    ticket = generator.random_ticket(10000)
    print("-"*70)
    print("ticket size", len(ticket))
    ticket_left=[]
    for nums in ticket:
        under_rules=[]
        for rule in rules:
            if rule['condition'](nums):
                under_rules.append(rule)
        train, test = split_data(data, size)
        match_count = display_statistic(train, under_rules)
        if random.randint(0,len(data)) <= match_count:
            ticket_left.append(nums)

    print(len(ticket_left))
    ticket_final = random.sample(ticket_left, 45)
    print(len(ticket_final))
    result={"results":[]}
    for original_set in test:
        verify_result = verify_ticket(original_set, ticket_final)
        result["results"].append(summarize_verify_result(verify_result))
    average_lst=[result['average'] for result in result['results']]
    pstd_lst=[result['pstd'] for result in result['results']]
    win_time_lst=[result['win_time'] for result in result['results']] 
    win_price_lst=[result['win_price'] for result in result['results']] 
    result['average'] =(mean(average_lst), pstdev(average_lst))
    result['pstd'] =(mean(pstd_lst),pstdev(pstd_lst))
    result['win_time'] =(mean(win_time_lst), pstdev(win_time_lst))
    result['win_price'] =(mean(win_price_lst), pstdev(win_price_lst))
    display_summary(result)
    print(result)

def statistics_benchmark(rules, data, size):
    for rule in rules:
        display_statistic(data, [rule])
    
    for x in rules:
        for y in rules:
           display_statistic(data, [x, y]) 

def display_statistic(data, rules):
    # print("-"*70)
    # print([rule["description"] for rule in rules])
    meet_count = len([1 for nums in data if all([rule['condition'](nums) for rule in rules])])
    # print("meet condition", str(meet_count)+"/"+str(len(data)))  
    return meet_count

def generator_benchmark(new_rule_lst, rule_lst, skip_combine, data, size):
    for x in new_rule_lst:
        for y in rule_lst:
            if (x["description"], y["description"]) not in skip_combine:
                test_data = random.sample(data, size)
                result_x = test_block(test_data, [x])
                result_y = test_block(test_data, [y])
                result = test_block(test_data, [x, y])
                if not result["results"]:
                    print("Can't generate besed on these conditions")

                if is_result_good(result, result_x, result_y):
                    display_summary(result)
                    verify_good_result(x, y, data, size)

def verify_good_result(rule_x, rule_y, data, size):
    good_result_count =0
    for _ in range(10):
        test_data = random.sample(data, size)
        result_x = test_block(test_data, [rule_x])
        result_y = test_block(test_data, [rule_y])
        result = test_block(test_data, [rule_x, rule_y], False)
        if is_result_good(result, result_x, result_y):
            good_result_count+=1
    print(str(good_result_count), "out of 10 is good result")

def is_result_good(result, result_x, result_y):
    if result["results"]:
        items=['average', 'pstd', 'win_time', 'win_price']
        return any([result[item][0] >= (max(result_x[item][0], result_y[item][0])*1.1) for item in items])
    else:
        return False

def test_block(test_data, rules, display_desc=True):
    if len(rules)>1 and display_desc:
        print("-"*70)
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
    display_summary(result)
    return result

def display_summary(result):
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

def load_data():
    data_df = pd.read_csv('resource/Ozlotto-latest.csv')

    data = np.array(data_df)
    # drop draw no and date
    data = data[:,2:-2]
    print("data size",data.shape)
    return list(data)

if __name__ =='__main__':
    benchmark()