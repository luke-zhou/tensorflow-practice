import lotto_data
import tensorflow as tf
import csv


def main(file_name, num):
    # file_name = 'resource/preprocess-data-1.csv'
    # num = 1
    print(file_name)
    (train_x, train_y), (test_x, test_y) = lotto_data.load_data(file_name)
    # print(train_x)
    # print(train_y)
    my_feature_columns = []
    # print('x-key')
    # print(train_x.keys())
    for key in train_x.keys():
        if key == 'draw_number' or key == 'date':
            my_feature_columns.append(
                tf.feature_column.numeric_column(key=key))
        elif key == 'date-year':
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
            my_feature_columns.append(
                tf.feature_column.numeric_column(key=key))
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
        steps=1000)

    # Evaluate the model.
    eval_result = classifier.evaluate(
        input_fn=lambda: lotto_data.eval_input_fn(test_x, test_y, 50))
    print(file_name)
    print('Test set accuracy: {accuracy:0.3f}'.format(**eval_result))

    predict_x = {
        'draw_number': [1269],
        'date': [20180612],
        'date-year': [2018],
        'date-month': [6],
        'date-day': [12],
        'numb1-x': [2],
        'numb2-x': [42],
        'numb3-x': [37],
        'numb4-x': [24],
        'numb5-x': [13],
        'numb6-x': [26],
        'numb7-x': [36],
        'sup1-x': [44],
        'sup2-x': [14],
        'numb1-9': [31],
        'numb2-9': [25],
        'numb3-9': [3],
        'numb4-9': [23],
        'numb5-9': [17],
        'numb6-9': [40],
        'numb7-9': [15],
        'sup1-9': [16],
        'sup2-9': [26],
        'numb1-8': [43],
        'numb2-8': [20],
        'numb3-8': [7],
        'numb4-8': [27],
        'numb5-8': [36],
        'numb6-8': [11],
        'numb7-8': [23],
        'sup1-8': [18],
        'sup2-8': [26],
        'numb1-7': [7],
        'numb2-7': [45],
        'numb3-7': [39],
        'numb4-7': [4],
        'numb5-7': [16],
        'numb6-7': [27],
        'numb7-7': [29],
        'sup1-7': [40],
        'sup2-7': [24],
        'numb1-6': [15],
        'numb2-6': [11],
        'numb3-6': [9],
        'numb4-6': [19],
        'numb5-6': [27],
        'numb6-6': [8],
        'numb7-6': [36],
        'sup1-6': [5],
        'sup2-6': [29],
        'numb1-5': [41],
        'numb2-5': [45],
        'numb3-5': [27],
        'numb4-5': [31],
        'numb5-5': [29],
        'numb6-5': [9],
        'numb7-5': [43],
        'sup1-5': [16],
        'sup2-5': [6],
        'numb1-4': [41],
        'numb2-4': [3],
        'numb3-4': [12],
        'numb4-4': [13],
        'numb5-4': [6],
        'numb6-4': [40],
        'numb7-4': [29],
        'sup1-4': [4],
        'sup2-4': [39],
        'numb1-3': [2],
        'numb2-3': [13],
        'numb3-3': [39],
        'numb4-3': [45],
        'numb5-3': [19],
        'numb6-3': [12],
        'numb7-3': [31],
        'sup1-3': [24],
        'sup2-3': [41],
        'numb1-2': [13],
        'numb2-2': [21],
        'numb3-2': [44],
        'numb4-2': [1],
        'numb5-2': [8],
        'numb6-2': [12],
        'numb7-2': [9],
        'sup1-2': [38],
        'sup2-2': [10],
        'numb1-1': [11],
        'numb2-1': [30],
        'numb3-1': [45],
        'numb4-1': [18],
        'numb5-1': [33],
        'numb6-1': [37],
        'numb7-1': [23],
        'sup1-1': [6],
        'sup2-1': [3],
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


def loop_all(arg):
    for i in range(1, 46):
        main('resource/preprocess-data-'+str(i)+'.csv', i)


if __name__ == '__main__':
    for i in range(1, 46):
        main('resource/preprocess-data-'+str(i)+'.csv', i)

    # tf.logging.set_verbosity(tf.logging.INFO)
    # tf.app.run(loop_all, ['>', 'console-output.txt'])
