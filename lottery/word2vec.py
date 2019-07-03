from gensim.models import Word2Vec
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import time
from oz_verify import verify_ticket
from statistics import mean, pstdev

def main():
    train_features, test_features = load_data(50)
    train_features_str =[[str(num) for num in row]for row in train_features]
 
    #training word2vec on 3 sentences
    model = Word2Vec(train_features_str, window=7, min_count=1, size=5, sg=0, negative=1)

    #using the model
    #The new trained model can be used similar to the pre-trained ones.

    # #printing similarity index
    # print(model.similarity('1', '2'))

    print(model)

    result={"results":[]}
    for test_set in test_features:
        ticket =[]
        for i in range(1,46):
            filled =set([str(i)])
            while len(filled)<7:
                predicts = model.predict_output_word(list(filled))
                for predict in predicts:
                    if predict[0] not in filled:
                        filled.add(predict[0])
                        break
            ticket.append(sorted( [int(num) for num in filled]))

        verify_result= verify_ticket(test_set, ticket)
        result_stat={}
        result_stat['average']=verify_result['average_match_count']
        result_stat['pstd']=verify_result['pstd_match_count']
        result_stat['win_time']=verify_result['win_time']
        result_stat['win_price']=verify_result['win_price']
        result["results"].append(result_stat)
    
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
    

def load_data(test_size):
    data_df = pd.read_csv('resource/Ozlotto-latest.csv')

    data = np.array(data_df)
    # drop draw no and date
    data = data[:,2:-2]
    print("data size",data.shape)

    train_features, test_features, _, _ = train_test_split(data, data, test_size = test_size/data.shape[0], random_state = int(time.time()))
    print('Training Features Shape:', train_features.shape)
    # print('Training Labels Shape:', train_labels.shape)
    print('Testing Features Shape:', test_features.shape)
    # print('Testing Labels Shape:', test_labels.shape)
    return train_features, test_features

if __name__=='__main__':
    main()

