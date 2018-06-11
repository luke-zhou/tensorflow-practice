import pandas as pd
import tensorflow as tf

CSV_COLUMN_NAMES = ['draw_number','date','num1','numb2','numb3','numb4','numb5','numb6','numb7','sup1','sup2','result']
RESULTS = ['0', '1', '2']

def load_data(y_name='result'):
    """Returns the lotto dataset as (train_x, train_y), (test_x, test_y)."""
    csv_file_path = 'resource/preprocess-data-2.csv'

    dataframe = pd.read_csv(csv_file_path, names=CSV_COLUMN_NAMES, header=0).sample(frac=1)

    train, test = split_train_n_test(dataframe)
    
    train_x, train_y = train, train.pop(y_name)

    test_x, test_y = test, test.pop(y_name)

    return (train_x, train_y), (test_x, test_y)

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
    dataset = dataset.shuffle(1000).repeat().batch(batch_size)

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


# The remainder of this file contains a simple example of a csv parser,
#     implemented using a the `Dataset` class.

# `tf.parse_csv` sets the types of the outputs to match the examples given in
#     the `record_defaults` argument.
CSV_TYPES = [[0.0], [0.0], [0.0], [0.0], [0]]

def _parse_line(line):
    # Decode the line into its fields
    fields = tf.decode_csv(line, record_defaults=CSV_TYPES)

    # Pack the result into a dictionary
    features = dict(zip(CSV_COLUMN_NAMES, fields))

    # Separate the label from the features
    label = features.pop('Species')

    return features, label


def csv_input_fn(csv_path, batch_size):
    # Create a dataset containing the text lines.
    dataset = tf.data.TextLineDataset(csv_path).skip(1)

    # Parse each line.
    dataset = dataset.map(_parse_line)

    # Shuffle, repeat, and batch the examples.
    dataset = dataset.shuffle(1000).repeat().batch(batch_size)

    # Return the dataset.
    return dataset
