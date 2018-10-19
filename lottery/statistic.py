import pandas as pd 
import numpy as np

def main():
    print('main')
    lottery_df = pd.read_csv('resource/Ozlotto-latest.csv')
    # print(lottery_df)
    # print(lottery_df.shape)
    lottery_df.astype('int64')
    # print(lottery_df.dtypes)
    lottery_df = preprocess(lottery_df)
    # print(lottery_df.head(20))
    # print(lottery_df.dtypes)
    lottery_df = calculate_statistic(lottery_df)

def preprocess(df):
    for previous in range(1, 11):
        for i in range(1, 8):
            num_column_name = 'num{}'.format(i)
            df['p-{}-{}'.format(previous, num_column_name)] = df[num_column_name].shift(previous)
        for i in range(1, 3):
            sup_column_name = 'sup{}'.format(i)
            df['p-{}-{}'.format(previous, sup_column_name)] = df[sup_column_name].shift(previous)
        
    return df

def calculate_statistic(df):
    for previous in range(1, 11):
        column_name='appear_in_previous_{}'.format(previous)
        num_column_names = ['num{}'.format(i) for i in range(1, 8)]
        df[column_name] = check_previous_n_overlap_current(previous)

        np.NaN if df['p-{}-num1'.format(previoue)].isnull() else 1 if df['p-{}-num1'.format(previoue)] == df['num1'] else 0
        t_df=[df['p-{}-{}'.format(previous, num_column_name)] for num_column_name in num_column_names]
        print(t_df.head(20))
        print(t_df.shape)
    return df
def check_previous_n_overlap_current(previous):
    if df['p-{}-num1'.format(previoue)].isnull()

if  __name__  == '__main__':
    main()