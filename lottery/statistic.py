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
    # print(lottery_df.dtypes)
    lottery_df = preprocess(lottery_df)
    lottery_df = generate_tickets(lottery_df)
    # print(lottery_df['p-1-num1'])
    # print(lottery_df.head())
    # print(lottery_df.shape)
    lottery_df.to_csv('resource/oz-latest-df.csv')
    lottery_df = calculate_statistic(lottery_df)
    # print(lottery_df.mean())
    lottery_df.mean().to_csv('resource/oz-latest-df-mean.csv')
    # lottery_df.plot()
    # plt.show()
    lottery_df = check_win(lottery_df)
    lottery_df.loc[:, 'random-ticket-win':].to_csv('resource/oz-latest-df-win-result.csv')
    lottery_df.loc[:, 'random-ticket-win':].describe().to_csv('resource/oz-latest-df-win-result-describe.csv')

def check_win(df):
    ticket_column =['random-ticket', 
    'low-appearing-rate-nums-12-remove-ticket',
    'low-appearing-rate-nums-6-remove-ticket',
    'low-appearing-rate-num-each-10-remove-ticket',
    'low-appearing-rate-num-each-7-remove-ticket'
    ]
    for index, row in df.iterrows():
        for column in ticket_column:
            right_nums = set(row[column]) & set(row['current'])
            df.at[index, column+'-win'] = 1 if right_nums else 0
            df.at[index, column+'-win-count'] = len(right_nums)
    
    return df


def preprocess(df):
    for previous in range(1, 11):
        for i in range(1, 8):
            num_column_name = 'num{}'.format(i)
            df['p-{}-{}'.format(previous, num_column_name)] = df[num_column_name].shift(previous)
        for i in range(1, 3):
            sup_column_name = 'sup{}'.format(i)
            df['p-{}-{}'.format(previous, sup_column_name)] = df[sup_column_name].shift(previous)

    df = df.dropna(how='any').astype('int64')

    for previous in range(1, 11):
        df['p-{}'.format(previous)]=np.full((len(df),), 0)
        df['p-{}'.format(previous)] = df['p-{}'.format(previous)].apply(lambda x : [])
        for i in range(1, 8):
            num_column_name = 'num{}'.format(i)
            df['p-{}'.format(previous)] += df['p-{}-{}'.format(previous, num_column_name)].apply(lambda x: [x])
    df['current']=np.full((len(df),), 0)
    df['current'] = df['current'].apply(lambda x : [])
    for i in range(1, 8):
        num_column_name = 'num{}'.format(i)
        df['current'] += df[num_column_name].apply(lambda x: [x])    
    
    df['random'] = df.index.map(generate_random_ticket)

    return df

def generate_tickets(df):
    # random as baseline
    df['random-ticket'] = df.index.map(generate_random_ticket)

    # remove nums by appearing rate 12
    low_appearing_rate_nums_12 =[  (3,4), (9,7), (9,4),
                                (9,5), (7,2), (1,5),
                                (6,6), (9,3), (1,7),
                                (2,1), (6,3), (10,1)
                                ]
    df['low-appearing-rate-nums-12'] = df.index.map(lambda x : [])
    for (p,i) in low_appearing_rate_nums_12:
        column_name = 'p-{}-num{}'.format(p, i)
        df['low-appearing-rate-nums-12'] += df[column_name].apply(lambda x: [x])
    df['low-appearing-rate-nums-12-remove-ticket'] = df['low-appearing-rate-nums-12'].map(generate_tickets_without_nums)
    # print(df['low-appearing-rate-nums-12-remove-ticket'])    

    # remove nums by appearing rate 6
    low_appearing_rate_nums_6 =[  (3,4), (9,7), (9,4),
                                (9,5), (7,2), (1,5)
                                ]
    df['low-appearing-rate-nums-6'] = df.index.map(lambda x : [])
    for (p,i) in low_appearing_rate_nums_6:
        column_name = 'p-{}-num{}'.format(p, i)
        df['low-appearing-rate-nums-6'] += df[column_name].apply(lambda x: [x])
    df['low-appearing-rate-nums-6-remove-ticket'] = df['low-appearing-rate-nums-6'].map(generate_tickets_without_nums)
   
    # remove lowest apperaing rate num in each draw 10
    low_appearing_rate_num_each_10 = [
        (1,7), (2,1), (3,4), (4,1), (5,7),
        (6,6), (7,2), (8,4), (9,7), (10,1)
    ]
    df['low-appearing-rate-num-each-10'] = df.index.map(lambda x : [])
    for (p,i) in low_appearing_rate_num_each_10:
        column_name = 'p-{}-num{}'.format(p, i)
        df['low-appearing-rate-num-each-10'] += df[column_name].apply(lambda x: [x])
    df['low-appearing-rate-num-each-10-remove-ticket'] = df['low-appearing-rate-num-each-10'].map(generate_tickets_without_nums)


    # remove lowest apperaing rate num in each draw 7
    low_appearing_rate_num_each_7 = [
        (1,7), (2,1), (3,4), 
        (6,6), (7,2), (9,7), (10,1)
    ]
    df['low-appearing-rate-num-each-7'] = df.index.map(lambda x : [])
    for (p,i) in low_appearing_rate_num_each_7:
        column_name = 'p-{}-num{}'.format(p, i)
        df['low-appearing-rate-num-each-7'] += df[column_name].apply(lambda x: [x])
    df['low-appearing-rate-num-each-7-remove-ticket'] = df['low-appearing-rate-num-each-7'].map(generate_tickets_without_nums)

    return df

def generate_tickets_without_nums(nums):
    nums.extend([10,42])
    ticket = set()
    while (len(ticket)<7):
        num = np.random.randint(1, 45 + 1)
        if num not in nums:
            ticket.add(num)
    
    return list(ticket)



def calculate_statistic(df):
    for index, row in df.iterrows():
        
        random_sames = set(row['random']) & set(row['current'])
        df.at[index, 'base-line-appear'] = 0 if not random_sames else 1
        df.at[index, 'base-line-appear-count'] = len(random_sames)

        for previous in range(1, 11):
            for i in range(1, 8):
                column_name = 'p-{}-num{}'.format(previous, i)
                df.at[index, column_name+'-appear']= 1 if row[column_name] in row['current'] else 0



        for previous in range(1, 11):
            previous_nums = set()
            previous_common = set()
            for i in range(1, previous+1):
                previous_common |= previous_nums & set(row['p-{}'.format(i)])
                previous_nums |= set(row['p-{}'.format(i)])

            same_nums = [e for e in row['current'] if e in previous_nums]
            same_nums_previous_common =  set(row['current']) & previous_common
            df.at[index,'p-{}-appear'.format(previous)] = 0 if not same_nums else 1
            df.at[index,'p-{}-appear-count'.format(previous)] = len(same_nums)
            df.at[index,'p-{}-exclude-count'.format(previous)] = len(previous_nums)
            df.at[index, 'p-{}-previous-common-appear'.format(previous)] = 0 if not same_nums_previous_common else 1
            df.at[index, 'p-{}-previous-common-appear-count'.format(previous)] = len(same_nums_previous_common)
            df.at[index, 'p-{}-previous-common-exclude-count'.format(previous)] = len(previous_common)
            same_nums_one_previous_only = set(row['p-{}'.format(previous)]) & set(row['current'])
            df.at[index,'p-{}-only-appear'.format(previous)] = 0 if not same_nums_one_previous_only else 1
            df.at[index,'p-{}-only-appear-count'.format(previous)] = len(same_nums_one_previous_only)
            df.at[index,'p-{}-only-exclude-count'.format(previous)] = len(row['p-{}'.format(previous)])
        
    
    return df

def generate_random_ticket(any):
    ticket = set()
    while (len(ticket)<7):
        ticket.add(np.random.randint(1, 45 + 1))
    
    return list(ticket)

def map_to_9_gong(list1):
    nine_gong = [2,9,4,7,5,3,6,1,8]
    return [(a*b)%45+1 for a,b in zip(list1,nine_gong)]
    

if  __name__  == '__main__':
    main()
