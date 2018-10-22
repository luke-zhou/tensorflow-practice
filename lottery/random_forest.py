import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import export_graphviz
import pydot

def main():
    features = pd.read_csv('resource/oz-latest-df-1-data.csv')
    features = pd.get_dummies(features)
    result =features.head(5)
    print(result)
    print('The shape of our features is:', features.shape)

    features = features.drop(features.columns[0], axis=1)
    print(features.tail())
    predict_features = features.iloc[(len(features)-1)]
    print(predict_features)
    predict_features = predict_features.loc[:, :'p-10-45']
    print(predict_Features)
    features = features.drop(len(features)-1)
    print(features.tail())

    # Labels are the values we want to predict
    labels = [np.array(features['current-'+str(i)]) for i in range(1,46)]
    # print(labels)
    [print(features['current-'+str(i)].describe()) for i in range(1, 46)]
    # labels = preprocess_label(labels)
    # print(labels)
    # Remove the labels from the features
    # axis 1 refers to the columns
    label_columns = ['current-'+str(i) for i in range(1, 46)]
    features = features.drop(label_columns, axis = 1)
    
    print(features.shape)
    # features = drop_less_importance(features)
    # Saving feature names for later use
    feature_list = list(features.columns)
    print(feature_list)
    # Convert to numpy array
    features = np.array(features)
    # print(features)

    for i in range(1):
        # Split the data into training and testing sets
        train_features, test_features, train_labels, test_labels = train_test_split(features, labels[i], test_size = 0.25, random_state = 37)

        # print('Training Features Shape:', train_features.shape)
        # print('Training Labels Shape:', train_labels.shape)
        # print('Testing Features Shape:', test_features.shape)
        # print('Testing Labels Shape:', test_labels.shape)

        # print(type(test_features))

        # baseline_preds = np.random.randint(3,size=(216,))
        # # baseline_preds = np.random.randint(5,size=(216,))+1
        # # print(type(baseline_preds))
        # # print(baseline_preds)
        # # # Baseline errors, and display average baseline error
        # baseline_errors = abs(baseline_preds - test_labels)
        # print('Average baseline error: ', round(np.mean(baseline_errors), 2))
        # print('baseline accurate: ', np.count_nonzero(baseline_errors==0)/len(baseline_errors))
        # Average baseline error: 1.5 degrees.

        # Instantiate model with 1000 decision trees
        rf = RandomForestClassifier(n_estimators = 1000, random_state = 37, class_weight='balanced')
        # Train the model on training data
        rf.fit(train_features, train_labels)


        # Use the forest's predict method on the test data
        predictions = rf.predict(test_features)
        # print(predictions)
        # Calculate the absolute errors
        errors = predictions == test_labels
        count = [1 for e in errors if e]
        print(len(count)/len(errors))
        # # Print out the mean absolute error (mae)
        # print('Mean Absolute Error:', round(np.mean(errors), 2))
        # # print(errors)
        # print('baseline accurate: ', np.count_nonzero(errors==0)/len(errors))


    # # Pull out one tree from the forest
    # tree = rf.estimators_[5]
    # # Export the image to a dot file
    # export_graphviz(tree, out_file = 'tree.dot', feature_names = feature_list, rounded = True, precision = 1)
    # # Use dot file to create a graph
    # (graph, ) = pydot.graph_from_dot_file('tree.dot')
    # # Write graph to a png file
    # graph.write_png('../data/tree.png')

    # # Get numerical feature importances
    # importances = list(rf.feature_importances_)
    # # List of tuples with variable and importance
    # feature_importances = [(feature, round(importance, 3)) for feature, importance in zip(feature_list, importances)]
    # # Sort the feature importances by most important first
    # feature_importances = sorted(feature_importances, key = lambda x: x[1], reverse = True)
    # # Print out the feature and importances 
    # [print('Variable: {:20} Importance: {}'.format(*pair)) for pair in feature_importances]

def drop_less_importance(df):
    not_important=[
        'p-1-12',
        'p-1-24',
        'p-1-27',
        'p-2-6',
        'p-2-9',
        'p-2-10',
        'p-2-14',
        'p-2-27',
        'p-2-36',
        'p-2-38',
        'p-2-41',
        'p-3-10',
        'p-3-12',
        'p-3-38',
        'p-4-6',
        'p-4-17',
        'p-4-22',
        'p-4-23',
        'p-4-40',
        'p-4-41',
        'p-5-23',
        'p-5-24',
        'p-6-4',
        'p-6-11',
        'p-6-26',
        'p-6-27',
        'p-6-29',
        'p-6-41',
        'p-7-20',
        'p-7-38',
        'p-8-11',
        'p-8-26',
        'p-8-37',
        'p-9-1',
        'p-9-10',
        'p-9-17',
        'p-9-18',
        'p-9-40',
        'p-9-41',
        'p-10-15',
        'p-10-24',
        'p-1-35',
        'p-3-30',
        'p-4-14',
        'p-4-42',
        'p-7-21',
        'p-1-9',
        'p-3-6',
        'p-4-45',
        'p-7-31',
        'p-1-40',
        'p-2-35',
        'p-8-14',
        'p-1-4',
        'p-1-5',
        'p-1-6',
        'p-1-8',
        'p-1-10',
        'p-1-11',
        'p-1-16',
        'p-1-17',
        'p-1-18',
        'p-1-19',
        'p-1-20',
        'p-1-21',
        'p-1-22',
        'p-1-23',
        'p-1-25',
        'p-1-26',
        'p-1-29',
        'p-1-30',
        'p-1-31',
        'p-1-37',
        'p-1-38',
        'p-1-39',
        'p-1-41',
        'p-1-42',
        'p-1-44',
        'p-2-1',
        'p-2-3',
        'p-2-5',
        'p-2-8',
        'p-2-11',
        'p-2-13',
        'p-2-15',
        'p-2-16',
        'p-2-17',
        'p-2-18',
        'p-2-19',
        'p-2-20',
        'p-2-21',
        'p-2-24',
        'p-2-25',
        'p-2-26',
        'p-2-28',
        'p-2-31',
        'p-2-32',
        'p-2-33',
        'p-2-34',
        'p-2-37',
        'p-2-39',
        'p-2-40',
        'p-2-42',
        'p-2-43',
        'p-2-45',
        'p-3-1',
        'p-3-2',
        'p-3-4',
        'p-3-5',
        'p-3-7',
        'p-3-8',
        'p-3-9',
        'p-3-13',
        'p-3-14',
        'p-3-15',
        'p-3-16',
        'p-3-18',
        'p-3-19',
        'p-3-20',
        'p-3-24',
        'p-3-26',
        'p-3-29',
        'p-3-32',
        'p-3-33',
        'p-3-36',
        'p-3-40',
        'p-3-41',
        'p-3-43',
        'p-3-45',
        'p-4-1',
        'p-4-2',
        'p-4-3',
        'p-4-4',
        'p-4-5',
        'p-4-7',
        'p-4-8',
        'p-4-9',
        'p-4-12',
        'p-4-13',
        'p-4-15',
        'p-4-16',
        'p-4-18',
        'p-4-19',
        'p-4-20',
        'p-4-21',
        'p-4-24',
        'p-4-26',
        'p-4-27',
        'p-4-28',
        'p-4-30',
        'p-4-31',
        'p-4-32',
        'p-4-34',
        'p-4-35',
        'p-4-37',
        'p-4-38',
        'p-4-39',
        'p-4-43',
        'p-4-44',
        'p-5-1',
        'p-5-2',
        'p-5-3',
        'p-5-4',
        'p-5-5',
        'p-5-6',
        'p-5-7',
        'p-5-9',
        'p-5-10',
        'p-5-11',
        'p-5-13',
        'p-5-14',
        'p-5-15',
        'p-5-18',
        'p-5-19',
        'p-5-21',
        'p-5-25',
        'p-5-27',
        'p-5-28',
        'p-5-30',
        'p-5-38',
        'p-5-41',
        'p-5-42',
        'p-5-43',
        'p-5-44',
        'p-5-45',
        'p-6-5',
        'p-6-6',
        'p-6-7',
        'p-6-9',
        'p-6-10',
        'p-6-12',
        'p-6-13',
        'p-6-14',
        'p-6-17',
        'p-6-18',
        'p-6-19',
        'p-6-20',
        'p-6-23',
        'p-6-25',
        'p-6-28',
        'p-6-30',
        'p-6-31',
        'p-6-32',
        'p-6-33',
        'p-6-35',
        'p-6-37',
        'p-6-38',
        'p-6-39',
        'p-6-40',
        'p-6-43',
        'p-6-45',
        'p-7-2',
        'p-7-4',
        'p-7-6',
        'p-7-10',
        'p-7-11',
        'p-7-12',
        'p-7-13',
        'p-7-15',
        'p-7-17',
        'p-7-18',
        'p-7-22',
        'p-7-24',
        'p-7-26',
        'p-7-27',
        'p-7-28',
        'p-7-29',
        'p-7-30',
        'p-7-32',
        'p-7-33',
        'p-7-35',
        'p-7-36',
        'p-7-39',
        'p-7-43',
        'p-7-44',
        'p-8-1',
        'p-8-2',
        'p-8-3',
        'p-8-4',
        'p-8-5',
        'p-8-6',
        'p-8-8',
        'p-8-9',
        'p-8-10',
        'p-8-12',
        'p-8-13',
        'p-8-15',
        'p-8-16',
        'p-8-17',
        'p-8-18',
        'p-8-19',
        'p-8-20',
        'p-8-21',
        'p-8-22',
        'p-8-23',
        'p-8-24',
        'p-8-25',
        'p-8-27',
        'p-8-29',
        'p-8-32',
        'p-8-33',
        'p-8-34',
        'p-8-35',
        'p-8-36',
        'p-8-38',
        'p-8-40',
        'p-8-41',
        'p-8-42',
        'p-8-44',
        'p-8-45',
        'p-9-2',
        'p-9-3',
        'p-9-5',
        'p-9-6',
        'p-9-7',
        'p-9-8',
        'p-9-9',
        'p-9-11',
        'p-9-13',
        'p-9-15',
        'p-9-19',
        'p-9-22',
        'p-9-23',
        'p-9-26',
        'p-9-27',
        'p-9-28',
        'p-9-29',
        'p-9-30',
        'p-9-32',
        'p-9-34',
        'p-9-36',
        'p-9-37',
        'p-9-38',
        'p-9-39',
        'p-9-42',
        'p-9-43',
        'p-9-45',
        'p-10-1',
        'p-10-3',
        'p-10-4',
        'p-10-5',
        'p-10-6',
        'p-10-7',
        'p-10-8',
        'p-10-9',
        'p-10-11',
        'p-10-12',
        'p-10-13',
        'p-10-16',
        'p-10-17',
        'p-10-18',
        'p-10-20',
        'p-10-22',
        'p-10-26',
        'p-10-27',
        'p-10-28',
        'p-10-31',
        'p-10-32',
        'p-10-34',
        'p-10-37',
        'p-10-38',
        'p-10-39',
        'p-10-40',
        'p-10-42',
        'p-10-44',
        'p-10-45',
        'p-2-23',
        'p-7-9',
        'p-1-2',
'p-1-7',
'p-1-13',
'p-1-33',
'p-1-34',
'p-1-43',
'p-2-2',
'p-2-7',
'p-2-29',
'p-2-44',
'p-3-3',
'p-3-17',
'p-3-21',
'p-3-22',
'p-3-23',
'p-3-25',
'p-3-27',
'p-3-28',
'p-3-39',
'p-3-42',
'p-4-10',
'p-4-29',
'p-4-33',
'p-5-8',
'p-5-12',
'p-5-16',
'p-5-26',
'p-5-39',
'p-6-8',
'p-6-16',
'p-6-22',
'p-7-8',
'p-7-34',
'p-7-42',
'p-8-7',
'p-8-28',
'p-8-39',
'p-8-43',
'p-9-12',
'p-9-20',
'p-9-21',
'p-9-25',
'p-9-33',
'p-10-2',
'p-10-19',
'p-10-23',
'p-10-33',
'p-10-36',
'p-1-14',
'p-1-45',
'p-2-4',
'p-5-40',
'p-6-3',
'p-6-36',
'p-7-14',
'p-7-40',
'p-7-41',
'p-9-16',
'p-10-14',
'p-10-29',
'p-10-30',
'p-10-41',
'p-10-10',
'p-1-3',
'p-1-15',
'p-1-36',
'p-2-12',
'p-3-37',
'p-4-11',
'p-5-17',
'p-5-20',
'p-5-36',
'p-6-21',
'p-6-44',
'p-7-25',
'p-8-31',
'p-9-14',
'p-9-31',
'p-10-43',
'p-5-33',
'p-6-24',
'p-7-23',
'p-9-35',
'p-3-11',
'p-3-34',
'p-5-31',
'p-7-5',
'p-7-16',
    ]
    return df.drop(not_important, axis=1)

if __name__=='__main__':
    main()