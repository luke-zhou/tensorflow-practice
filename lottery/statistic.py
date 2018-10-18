import pandas as pd 

def main():
    print('main')
    lottery_data = pd.read_csv('resource/Ozlotto-latest.csv')
    print(lottery_data)
    print(lottery_data.shape)

if  __name__  == '__main__':
    main()