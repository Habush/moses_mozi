__author_ = 'Xabush Semrie'

import numpy as np

import pandas as pd
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import StratifiedShuffleSplit

# from custom_estimator import MosesEstimator

#Csv file to dataframe
df = pd.read_csv("data/bin_truncated.csv")

print(df.columns.values)
print(df.shape)

strshuffle = StratifiedShuffleSplit(n_splits=3, test_size=0.3)

#
# moses = MosesEstimator("-j 6")



def custom_cross_val(X, y, cv):
    cm = None
    y_pred_overall = None
    y_test_overall = None
    for train_index, test_index in cv.split(X, y):
        X_train, X_test = X[train_index], X[test_index]
        # print(X_train)
        y_train, y_test = y[train_index], y[test_index]
        print(y_test.iloc[0])
        # clf.fit(X_train)

    #     y_pred = clf.predict(X_test)
    #
    #     if y_pred_overall is None:
    #         y_pred_overall = y_pred
    #         y_test_overall = y_test
    #
    #     else:
    #         y_pred_overall = np.concatenate([y_pred_overall, y_pred])
    #         y_test_overall = np.concatenate([y_test_overall, y_test])
    #
    #
    #     curr_cm = confusion_matrix(y_test, y_pred)
    #
    #     #sum the confusion matrix per fold
    #     if cm is None:
    #         cm = curr_cm
    #     else:
    #         cm += curr_cm
    #
    # print (classification_report(y_test_overall, y_pred_overall, digits=3))
    # print (cm)


custom_cross_val( df.values, df.case, strshuffle)