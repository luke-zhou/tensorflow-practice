from gensim.models import Word2Vec

def main():
    sentence=[['Neeraj','Boy'],['Sarwan','is'],['good','boy']]

    #training word2vec on 3 sentences
    model = Word2Vec(sentence, min_count=1,size=2,workers=1)

    #using the model
    #The new trained model can be used similar to the pre-trained ones.

    #printing similarity index
    print(model.similarity('Boy', 'boy'))

    print(model)
    print(model.predict_output_word(['Neeraj','Boy']))

if __name__=='__main__':
    main()

