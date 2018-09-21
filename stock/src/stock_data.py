import pandas as pd
import tensorflow as tf

def load_data(file_name, y_name='result'):
    """Returns the lotto dataset as (train_x, train_y), (test_x, test_y)."""

    dataframe = pd.read_csv(
        file_name, names=generate_column_names(file_name), header=0).sample(frac=1)

    train, test = split_train_n_test(dataframe)

    train_x, train_y = train, train.pop(y_name)

    test_x, test_y = test, test.pop(y_name)

    return (train_x, train_y), (test_x, test_y)

def generate_column_names(file_name):
    feature_columns = ['f-'+str(i) for i in range(25)]
    return [*feature_columns, 'result']

def split_train_n_test(data, test_portion=0.1):
    data_size = len(data)
    test_data_size = int(data_size*test_portion)
    test_data = data[:test_data_size]
    training_data = data[test_data_size:]
    return training_data, test_data

def train_input_fn(features, labels, batch_size):
    """An input function for training"""
    # Convert the inputs to a Dataset.
    dataset = tf.data.Dataset.from_tensor_slices((dict(features), labels))

    # Shuffle, repeat, and batch the examples.
    dataset = dataset.shuffle(10000).repeat().batch(batch_size)

    # Return the dataset.
    return dataset


def eval_input_fn(features, labels, batch_size):
    """An input function for evaluation or prediction"""
    features = dict(features)
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
