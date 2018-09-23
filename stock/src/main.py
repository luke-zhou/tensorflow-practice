import tensorflow as tf
import stock_data

def main(args):
    (train_x, train_y), (test_x, test_y) = stock_data.load_data('../trainingdata/preprocess-25.csv')

    feature_columns = [tf.feature_column.numeric_column(key=key) for key in train_x.keys()]

    classifier = tf.estimator.DNNClassifier(
        feature_columns=feature_columns,
        # Two hidden layers of 10 nodes each.
        hidden_units=[25, 5],
        # The model must choose between 3 classes.
        n_classes=2)
        
    # Train the Model.
    classifier.train(
        input_fn=lambda: stock_data.train_input_fn(train_x, train_y, 500),
        steps=1000)

    # Evaluate the model.
    eval_result = classifier.evaluate(
        input_fn=lambda: stock_data.eval_input_fn(test_x, test_y, 50))
    print('Test set accuracy: {accuracy:0.3f}'.format(**eval_result))

if __name__=='__main__':
    tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run(main)