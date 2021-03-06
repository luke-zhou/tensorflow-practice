from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from collections import Counter
import pandas as pd
import random
import tensorflow as tf
    
positive_data_file_name = 'data-set/rt-polarity.pos'
negative_data_file_name = 'data-set/rt-polarity.neg'

def load_data():

    words = sum(load_file(negative_data_file_name),[]) + sum(load_file(positive_data_file_name),[])
    
    features = generate_features(words)
    print('lenth of feature: {}'.format(len(features)))

    features_data = generate_features_data(features)

    training_features_data, test_features_data = split_train_n_test(features_data)

    features.append('tf_classification_type')
    # print(features)
    test_data_frame = pd.DataFrame(test_features_data, columns=features)
    traning_data_frame = pd.DataFrame(training_features_data, columns=features)

    # print(traning_data_frame.head())
    # print(traning_data_frame.keys())
    train_x, train_y = traning_data_frame, traning_data_frame.pop('tf_classification_type')
    test_x, test_y = test_data_frame, test_data_frame.pop('tf_classification_type')
    # print(train_y)
    return (train_x, train_y), (test_x, test_y)

def split_train_n_test(data, test_portion=0.1):
    data_size = len(data)
    random.shuffle(data)
    test_data_size = int(data_size*test_portion)
    test_data = data[:test_data_size]
    training_data = data[test_data_size:]
    return training_data, test_data

def generate_features_data(features):
    def review_to_feature_vector(words, type):
        feature_vector = [1 if feature in words else 0 for feature in features]
        feature_vector.append(type)
        return feature_vector
    
    features_data = [review_to_feature_vector(words_of_line, 0) for words_of_line in load_file(negative_data_file_name)] + [review_to_feature_vector(words_of_line, 1) for words_of_line in load_file(positive_data_file_name)]

    return features_data


def generate_features(words):
    total_word_num = len(words)
    words_count = Counter(words)
    features = [word for word in words_count if words_count[word]>total_word_num/10000 and words_count[word]<total_word_num/100]
    return features

def load_file(file_name):
    with open(file_name,'r') as f:
        tokenizer = RegexpTokenizer(r'[A-Za-z0-9.][A-Za-z0-9_.]*')
        lines = [line.lower() for line in f]
        words_of_lines = [tokenizer.tokenize(line) for line in lines]
        lemmatizer = WordNetLemmatizer()
        lemmatized_words = [[lemmatizer.lemmatize(word) for word in words] for words in words_of_lines]
        return lemmatized_words

def train_input_fn(features, labels, batch_size):
    """An input function for training"""
    # Convert the inputs to a Dataset.
    dataset = tf.data.Dataset.from_tensor_slices((dict(features), labels))

    # Shuffle, repeat, and batch the examples.
    buffer_size =int(len(features.index)*1.5)
    print('shuffle buffer size: {}'.format(buffer_size))
    dataset = dataset.shuffle(buffer_size).repeat().batch(batch_size)
    # Return the dataset.
    return dataset

def eval_input_fn(features, labels, batch_size):
    """An input function for evaluation or prediction"""
    features=dict(features)
    if labels is None:
        # No labels, use only features.
        inputs = features
    else:
        inputs = (features, labels)

    # Convert the inputs to a Dataset.
    dataset = tf.data.Dataset.from_tensor_slices(inputs)

    # Batch the examples
    assert batch_size is not None, "batch_size must not be None"
    dataset = dataset.batch(batch_size)

    # Return the dataset.
    return dataset
