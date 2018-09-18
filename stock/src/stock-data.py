def load_data(file_name, y_name='result'):
    """Returns the lotto dataset as (train_x, train_y), (test_x, test_y)."""
    csv_file_path = file_name

    dataframe = pd.read_csv(
        csv_file_path, names=CSV_COLUMN_NAMES, header=0).sample(frac=1)

    train, test = split_train_n_test(dataframe)

    train_x, train_y = train, train.pop(y_name)

    test_x, test_y = test, test.pop(y_name)

    return (train_x, train_y), (test_x, test_y)