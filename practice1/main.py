import review_data
import tensorflow as tf

def main():

    # Fetch the data
    (train_x, train_y), (test_x, test_y) = review_data.load_data()

    # Feature columns describe how to use the input.
    my_feature_columns = []
    for key in train_x.keys():
        my_feature_columns.append(tf.feature_column.numeric_column(key=key))

    # Build 2 hidden layer DNN with 10, 10 units respectively.
    classifier = tf.estimator.DNNClassifier(
        feature_columns=my_feature_columns,
        # Two hidden layers of 10 nodes each.
        hidden_units=[10, 10],
        # The model must choose between 3 classes.
        n_classes=2)

    # Train the Model.
    classifier.train(
        input_fn=lambda:review_data.train_input_fn(train_x, train_y,
                                                 70),
        steps=100)

    # Evaluate the model.
    eval_result = classifier.evaluate(
        input_fn=lambda:review_data.eval_input_fn(test_x, test_y,
                                                5))

    print('\nTest set accuracy: {accuracy:0.3f}\n'.format(**eval_result))

    # Generate predictions from the model
    # expected = ['Setosa', 'Versicolor', 'Virginica']
    # predict_x = {
    #     'SepalLength': [5.1, 5.9, 6.9],
    #     'SepalWidth': [3.3, 3.0, 3.1],
    #     'PetalLength': [1.7, 4.2, 5.4],
    #     'PetalWidth': [0.5, 1.5, 2.1],
    # }


    # predictions = classifier.predict(
    #     input_fn=lambda:iris_data.eval_input_fn(predict_x,
    #                                             labels=None,
    #                                             batch_size=args.batch_size))
                                                  
    # for pred_dict, expec in zip(predictions, expected):
    #     template = ('\nPrediction is "{}" ({:.1f}%), expected "{}"')

    #     class_id = pred_dict['class_ids'][0]
    #     print(pred_dict['class_ids'])
    #     probability = pred_dict['probabilities'][class_id]

    #     print(template.format(iris_data.SPECIES[class_id],
    #                           100 * probability, expec))

if __name__ == '__main__':
    main()