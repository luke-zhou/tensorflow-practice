import lotto_data
import tensorflow as tf
import csv
from datetime import datetime


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

    predict_x = build_predict_features()

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


def build_predict_features():
    draw_data = [[1261, 20180417, 43, 20, 7, 27, 36, 11, 23, 18, 26],
                 [1262, 20180424, 7, 45, 39, 4, 16, 27, 29, 40, 24],
                 [1263, 20180501, 15, 11, 9, 19, 27, 8, 36, 5, 29],
                 [1264, 20180508, 41, 45, 27, 31, 29, 9, 43, 16, 6],
                 [1265, 20180515, 41, 3, 12, 13, 6, 40, 29, 4, 39],
                 [1266, 20180522, 2, 13, 39, 45, 19, 12, 31, 24, 41],
                 [1267, 20180529, 13, 21, 44, 1, 8, 12, 9, 38, 10],
                 [1268, 20180605, 11, 30, 45, 18, 33, 37, 23, 6, 3],
                 [1269, 20180612, 22, 2, 31, 38, 12, 7, 45, 11, 29],
                 [1270, 20180619, 20, 18, 26, 35, 10, 22, 16, 25, 34]]
    predict_feature = {
        'draw_number': [1271],
        'date': [20180625],
    }
    draw_datetime = datetime.strptime(
        str(predict_feature['date'][0]), '%Y%m%d')
    draw_date = draw_datetime.date()
    predict_feature['date-year'] = [draw_date.year]
    predict_feature['date-month'] = [draw_date.month]
    predict_feature['date-day'] = [draw_date.day]
    for i in range(0, len(draw_data)):
        for j in range(1, 8):
            predict_feature['num'+str(j)+'-'+str(10-i)] = [draw_data[i][j+1]]
        for j in range(1, 3):
            predict_feature['sup'+str(j)+'-'+str(10-i)] = [draw_data[i][j+8]]

    return predict_feature


def loop_all(arg):
    for i in range(1, 46):
        main('resource/preprocess-data-'+str(i)+'.csv', i)


if __name__ == '__main__':
    # for i in range(1, 46):
    #     main('resource/preprocess-data-'+str(i)+'.csv', i)

    tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run(loop_all, ['>', 'console-output.txt'])
