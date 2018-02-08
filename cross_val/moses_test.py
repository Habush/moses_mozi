import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedShuffleSplit, cross_val_score, cross_val_predict
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.datasets import load_iris

from custom_estimator import MosesEstimator

#Csv file to dataframe
df = pd.read_csv("data/bin_truncated.csv")


strshuffle = StratifiedShuffleSplit(n_splits=3, test_size=0.3)


moses = MosesEstimator("-j 6")

# scores = cross_val_score(moses, dataset.values, dataset.case, cv=strshuffle, scoring="recall")
#
# print scores


def custom_cross_val(clf, X, y, cv):
    cm = None
    y_pred_overall = None
    y_test_overall = None
    for train_index, test_index in cv.split(X, y):
        X_train, X_test = X[train_index], X[test_index][:,1:]
        y_train, y_test = y[train_index], y[test_index]
        clf.fit(X_train)

        y_pred = clf.predict(X_test)

        if y_pred_overall is None:
            y_pred_overall = y_pred
            y_test_overall = y_test

        else:
            y_pred_overall = np.concatenate([y_pred_overall, y_pred])
            y_test_overall = np.concatenate([y_test_overall, y_test])


        curr_cm = confusion_matrix(y_test, y_pred)

        #sum the confusion matrix per fold
        if cm is None:
            cm = curr_cm
        else:
            cm += curr_cm

    print (classification_report(y_test_overall, y_pred_overall, digits=3))
    print (cm)


custom_cross_val(moses, df.values, df.case, strshuffle)