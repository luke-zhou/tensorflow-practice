import lotto_data
import tensorflow as tf

def main():
    (train_x, train_y), (test_x, test_y) = lotto_data.load_data();

    my_feature_columns = []
    for key in train_x.keys():
        my_feature_columns.append(tf.feature_column.numeric_column(key=key))

    # Build 2 hidden layer DNN with 10, 10 units respectively.
    classifier = tf.estimator.DNNClassifier(
        feature_columns=my_feature_columns,
        # Two hidden layers of 10 nodes each.
        hidden_units=[50, 25, 9],
        # The model must choose between 3 classes.
        n_classes=3)

    # Train the Model.
    classifier.train(
        input_fn=lambda:lotto_data.train_input_fn(train_x, train_y,500),
        steps=5000)
        
    # Evaluate the model.
    eval_result = classifier.evaluate(
        input_fn=lambda:lotto_data.eval_input_fn(test_x, test_y, 50))
    
    print('\nTest set accuracy: {accuracy:0.3f}\n'.format(**eval_result))
    
    
if __name__ == '__main__':
    for i in range(10):
        main()