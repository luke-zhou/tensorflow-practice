from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from collections import Counter

def main():
    words = [];
    words += load_file('data-set/rt-polarity.neg')
    words += load_file('data-set/rt-polarity.pos')
    
    features = generate_features(words)
    print(len(features))

    features_data = generate_features_date(features)

    print(len(features_data))
    #print(features_data[:1])

def generate_features_date(features):
    def review_to_feature_vector(review, type):
        lemmatizer = WordNetLemmatizer()
        words = [lemmatizer.lemmatize(word) for word in word_tokenize(review)]
        feature_vector = [1 if feature in words else 0 for feature in features]
        feature_vector.append(type)
        return feature_vector
    
    features_data =[]
    with open('data-set/rt-polarity.neg','r') as f:
        lines = [line.lower() for line in f]
        features_data += [review_to_feature_vector(line,0) for line in lines]
    with open('data-set/rt-polarity.pos','r') as f:
        lines = [line.lower() for line in f]
        features_data += [review_to_feature_vector(line,1) for line in lines]
    
    return features_data


def generate_features(words):
    total_word_num = len(words)
    words_count = Counter(words)
    features = [word for word in words_count if words_count[word]>total_word_num/10000 and words_count[word]<total_word_num/100]
    return features

def load_file(file_name):
    with open(file_name,'r') as f:
        lines = [line.lower() for line in f]
        words = sum([word_tokenize(line) for line in lines], [])
        lemmatizer = WordNetLemmatizer()
        lemmatized_words = [lemmatizer.lemmatize(word) for word in words]
        return lemmatized_words


if __name__ == '__main__':
    main()