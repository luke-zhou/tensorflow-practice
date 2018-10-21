import pandas as pd 
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

def main():
    print('main')
    lottery_df = pd.read_csv('resource/Ozlotto-latest.csv')
    # print(lottery_df)
    print(lottery_df.shape)
    # print(lottery_df.dtypes)
    lottery_df = preprocess(lottery_df)
    print(lottery_df['p-1-num1'])
    print(lottery_df.head())
    print(lottery_df.shape)
    lottery_df.to_csv('resource/oz-latest-df.csv')
    lottery_df = calculate_statistic(lottery_df)
    print(lottery_df.mean())
    lottery_df.mean().to_csv('resource/oz-latest-df-mean.csv')
    # lottery_df.plot()
    # plt.show()




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
    
    df['random'] = df.index.map(generate_one_ticket)

    for previous in range(1, 11):
         df['p-{}-9-gong'.format(previous)]= df['p-{}'.format(previous)].map(map_to_9_gong)
    
    return df

def calculate_statistic(df):
    for index, row in df.iterrows():
        
        random_sames = set(row['random']) & set(row['current'])
        df.at[index, 'base-line-appear'] = 0 if not random_sames else 1
        df.at[index, 'base-line-appear-count'] = len(random_sames)


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

def generate_one_ticket(any):
    ticket = set()
    while (len(ticket)<7):
        ticket.add(np.random.random_integers(45))
    
    return list(ticket)

def map_to_9_gong(list1):
    nine_gong = [2,9,4,7,5,3,6,1,8]
    return [(a*b)%45+1 for a,b in zip(list1,nine_gong)]
    

if  __name__  == '__main__':
    main()
