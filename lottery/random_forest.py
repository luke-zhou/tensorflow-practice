import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import export_graphviz
import pydot
import json
import sys

def main():
    data_df = pd.read_csv('resource/oz-latest-df-1-data.csv')
    data_df = pd.get_dummies(data_df)
    result =data_df.head(5)
    print('head-5:\n', result)
    print('The shape of our features is:', data_df.shape)

    # drop the draw no column
    data_df = data_df.drop(data_df.columns[0], axis=1)

    # drop the prediction feature
    predict_features = data_df.iloc[(len(data_df)-1)]
    # only keep feature data ,remove the fake result data
    predict_features = predict_features.loc[:'p-10-45']
    data_df = data_df.drop(len(data_df)-1)

    # # Labels are the values we want to predict
    # labels = [np.array(features['current-'+str(i)]) for i in range(1,46)]
    # # print(labels)
    # [print(features['current-'+str(i)].describe()) for i in range(1, 46)]
    # labels = preprocess_label(labels)
    # print(labels)
    # Remove the labels from the features
    # axis 1 refers to the columns
    # label_columns = ['current-'+str(i) for i in range(1, 46)]
    # features = features.drop(label_columns, axis = 1)
    
    # print(features.shape)
    # # features = drop_less_importance(features)
    # # Saving feature names for later use
    # feature_list = list(features.columns)
    # print(feature_list)
    # # Convert to numpy array
    # # features = np.array(features)
    # # print(features)
    result_dict={}
    for i in range(1, 46):
        predict_label, predict_accurate, feature_list = training_for(data_df, i, predict_features)
        result_dict[i]={'label':predict_label, 'accurate': predict_accurate, 'features': feature_list}

    with open('resource/oz-latest-predict-result.json', 'w') as f:
        json.dump(result_dict, f)
    f.close

    # # Pull out one tree from the forest
    # tree = rf.estimators_[5]
    # # Export the image to a dot file
    # export_graphviz(tree, out_file = 'tree.dot', feature_names = feature_list, rounded = True, precision = 1)
    # # Use dot file to create a graph
    # (graph, ) = pydot.graph_from_dot_file('tree.dot')
    # # Write graph to a png file
    # graph.write_png('../data/tree.png')

def training_for(data_df, i, predict_features):
    less_important_column =[]
    keep_going =3
    
    balanced_data_df = balanced_dataset(data_df, i)
    
    while keep_going>0:
        feature_list, features, labels = seperate_features_label(balanced_data_df, i, less_important_column)

        # Split the data into training and testing sets
        train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size = 0.20, random_state = len(feature_list))

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
        rf = RandomForestClassifier(n_estimators = (128+(450-len(feature_list))), random_state = 37, class_weight='balanced')
        # Train the model on training data
        rf.fit(train_features, train_labels)

        # Use the forest's predict method on the test data
        evaluations = rf.predict(test_features)
        # print(predictions)
        # Calculate the absolute errors
        errors = evaluations == test_labels
        count = [1 for e in errors if e]
        accurate = len(count)/len(errors)
        # print(str(i), ': ', accurate)

        # # Print out the mean absolute error (mae)
        # print('Mean Absolute Error:', round(np.mean(errors), 2))
        # # print(errors)
        # print('baseline accurate: ', np.count_nonzero(errors==0)/len(errors))

        # Get numerical feature importances
        importances = list(rf.feature_importances_)
        # List of tuples with variable and importance
        feature_importances = [(feature, round(importance, 3)) for feature, importance in zip(feature_list, importances)]
        # Sort the feature importances by most important first
        feature_importances = sorted(feature_importances, key = lambda x: x[1], reverse = True)
        # Print out the feature and importances 
        # [print('Variable: {:20} Importance: {}'.format(*pair)) for pair in feature_importances]
        if feature_importances[-1][1]*3<feature_importances[0][1]:
            sys.stdout.write("*")
            sys.stdout.flush()
            # print('feature_list_size: ', len(feature_list))
            # print("accurate: ", accurate)
            # print('Variable: {:20} Importance: {}'.format(*feature_importances[0]))
            # print('Variable: {:20} Importance: {}'.format(*feature_importances[-1]))
            less_important_column.append(feature_importances[-1][0])
            keep_going=3
        else:
            print("accurate: ", accurate)
            keep_going -=1

    
    print("\n", i, " : ", feature_list)
    print(i, " : ", accurate)
    # prediction
    prediction_label = rf.predict(np.array(predict_features[feature_list]).reshape(1, -1))
    print(i, prediction_label)
    return str(prediction_label.flat[0]), accurate, feature_list



def seperate_features_label(data_df, num, avoid_column):
    column_tuples = [(p,i) for p in range(1,11) for i in range(1, 46)]
    columns = ['p-{}-{}'.format(p, i) for (p,i) in column_tuples]
    columns = list(set(columns)-set(avoid_column))
    features = np.array(data_df[columns])
    labels = np.array(data_df['current-{}'.format(num)])

    return columns, features, labels

def balanced_dataset(data_df, num):
    appear_df = data_df[data_df['current-{}'.format(num)] == True]
    non_appear_df = data_df[data_df['current-{}'.format(num)] == False]
    # print('appear: ', appear_df.shape)
    # print('not appear: ', non_appear_df.shape)
    sample_non_appear_df = non_appear_df.sample(n=appear_df.shape[0])

    combined_df =  appear_df.append(sample_non_appear_df)
    combined_df = combined_df.sample(frac=1).reset_index(drop=True)
    print('combined: ', combined_df.shape)
    # print('combined head \n', combined_df['current-{}'.format(num)].head())
    return combined_df

if __name__=='__main__':
    main()