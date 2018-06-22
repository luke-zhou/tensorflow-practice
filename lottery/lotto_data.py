import pandas as pd
import tensorflow as tf

CSV_COLUMN_NAMES = ['draw_number', 'date', 'date-year', 'date-month', 'date-day',
                    'numb1-x', 'numb2-x', 'numb3-x', 'numb4-x', 'numb5-x', 'numb6-x', 'numb7-x', 'sup1-x', 'sup2-x',
                    'numb1-9', 'numb2-9', 'numb3-9', 'numb4-9', 'numb5-9', 'numb6-9', 'numb7-9', 'sup1-9', 'sup2-9',
                    'numb1-8', 'numb2-8', 'numb3-8', 'numb4-8', 'numb5-8', 'numb6-8', 'numb7-8', 'sup1-8', 'sup2-8',
                    'numb1-7', 'numb2-7', 'numb3-7', 'numb4-7', 'numb5-7', 'numb6-7', 'numb7-7', 'sup1-7', 'sup2-7',
                    'numb1-6', 'numb2-6', 'numb3-6', 'numb4-6', 'numb5-6', 'numb6-6', 'numb7-6', 'sup1-6', 'sup2-6',
                    'numb1-5', 'numb2-5', 'numb3-5', 'numb4-5', 'numb5-5', 'numb6-5', 'numb7-5', 'sup1-5', 'sup2-5',
                    'numb1-4', 'numb2-4', 'numb3-4', 'numb4-4', 'numb5-4', 'numb6-4', 'numb7-4', 'sup1-4', 'sup2-4',
                    'numb1-3', 'numb2-3', 'numb3-3', 'numb4-3', 'numb5-3', 'numb6-3', 'numb7-3', 'sup1-3', 'sup2-3',
                    'numb1-2', 'numb2-2', 'numb3-2', 'numb4-2', 'numb5-2', 'numb6-2', 'numb7-2', 'sup1-2', 'sup2-2',
                    'numb1-1', 'numb2-1', 'numb3-1', 'numb4-1', 'numb5-1', 'numb6-1', 'numb7-1', 'sup1-1', 'sup2-1',
                    'result']
RESULTS = ['Not There', 'Supply', 'Number']


def load_data(file_name, y_name='result'):
    """Returns the lotto dataset as (train_x, train_y), (test_x, test_y)."""
    csv_file_path = file_name

    dataframe = pd.read_csv(
        csv_file_path, names=CSV_COLUMN_NAMES, header=0).sample(frac=1)

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
