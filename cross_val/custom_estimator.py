from sklearn.base import BaseEstimator
from moses.pymoses import moses
import numpy as np

class MosesEstimator(BaseEstimator):
    def __init__(self, args=None):
        self.args = args
        self.moses = moses()

    def fit(self, X, y=None):
        if self.args is not None:
            output = self.moses.run(X, args=self.args, python=True)

        else:
            output = self.moses.run(X, python=True)

        self.models_ = output

        return self

    def predict(self, X):
        tests, models = len(X), len(self.models_)
        res = np.ndarray(shape=(tests, models), dtype=float)
        for i in range(tests):
            for j in range(models):
                res[i][j] = self.models_[j].eval(X[i])

        return self._majority_vote(res)

    def _majority_vote(self, arr):
        u, indices = np.unique(arr, return_inverse=True)
        axis = 1
        return u[np.argmax(np.apply_along_axis(np.bincount, axis, indices.reshape(arr.shape), None, np.max(indices) + 1), axis=axis)]