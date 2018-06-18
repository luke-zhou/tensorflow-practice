import lotto_data
import tensorflow as tf
import csv


def main(file_name, num):
    (train_x, train_y), (test_x, test_y) = lotto_data.load_data(file_name)
    # print(train_x)
    # print(train_y)
    my_feature_columns = []
    # print('x-key')
    # print(train_x.keys())
    for key in train_x.keys():
        if key == 'draw_number' or key == 'date' or key == 'date-year':
            my_feature_columns.append(
                tf.feature_column.numeric_column(key=key))
        elif key == 'date-month':
            feature_column = tf.feature_column.categorical_column_with_identity(
                key=key, num_buckets=13)
            my_feature_columns.append(
                tf.feature_column.indicator_column(feature_column))
        elif key == 'date-day':
            feature_column = tf.feature_column.categorical_column_with_identity(
                key=key, num_buckets=32)
            my_feature_columns.append(
                tf.feature_column.indicator_column(feature_column))
        else:
            feature_column = tf.feature_column.categorical_column_with_identity(
                key=key, num_buckets=46)
            my_feature_columns.append(
                tf.feature_column.indicator_column(feature_column))
    # print('feature')
    # print(my_feature_columns)
    # Build 2 hidden layer DNN with 10, 10 units respectively.
    classifier = tf.estimator.DNNClassifier(
        feature_columns=my_feature_columns,
        # Two hidden layers of 10 nodes each.
        hidden_units=[50, 25, 9],
        # The model must choose between 3 classes.
        n_classes=3)

    # Train the Model.
    classifier.train(
        input_fn=lambda: lotto_data.train_input_fn(train_x, train_y, 500),
        steps=5000)

    # Evaluate the model.
    eval_result = classifier.evaluate(
        input_fn=lambda: lotto_data.eval_input_fn(test_x, test_y, 50))
    print(file_name)
    print('Test set accuracy: {accuracy:0.3f}'.format(**eval_result))

    predict_x = {
        'draw_number': [1270],
        'date': [20180619],
        'date-year': [2018],
        'date-month': [6],
        'date-day':[19],
        'numb1-2': [11],
        'numb2-2': [30],
        'numb3-2': [45],
        'numb4-2': [18],
        'numb5-2': [33],
        'numb6-2': [37],
        'numb7-2': [23],
        'sup1-2': [6],
        'sup2-2': [3],
        'numb1-1': [22],
        'numb2-1': [2],
        'numb3-1': [31],
        'numb4-1': [38],
        'numb5-1': [12],
        'numb6-1': [7],
        'numb7-1': [45],
        'sup1-1': [11],
        'sup2-1': [29],
    }

    predictions = classifier.predict(input_fn=lambda: lotto_data.eval_input_fn(
        predict_x, labels=None, batch_size=50))

    template = ('Prediction is "{}" ({:.1f}%)')
    for prediction in predictions:
        print(prediction)
        class_id = prediction['class_ids'][0]
        probability = prediction['probabilities'][class_id]
        print(template.format(lotto_data.RESULTS[class_id], 100 * probability))
        print('')
        with open('output/result.csv', 'a', newline='') as data_csv_file:
            data_file = csv.writer(data_csv_file, delimiter=',')
            row = [num]
            row.extend(prediction['probabilities'])
            data_file.writerow(row)
        data_csv_file.close()

    # template = ('\nPrediction is "{}" ({:.1f}%), expected "{}"')
    # for pred_dict, expec in zip(predictions, expected):
    #     class_id = pred_dict['class_ids'][0]
    #     probability = pred_dict['probabilities'][class_id]

    #     print(template.format(lotto_data.RESULTS[class_id],
    #                           100 * probability, expec))


if __name__ == '__main__':
    for i in range(1, 46):
        main('resource/preprocess-data-'+str(i)+'.csv', i)
