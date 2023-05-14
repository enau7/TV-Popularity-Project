import math
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import ElasticNet
from sklearn.base import BaseEstimator

def columnstartswith(columns, df):
    if type(columns) == str:
        columns = [columns]
    output = []
    for item in columns:
        output += list(df.columns[df.columns.str.startswith(item)])
    return output
    
def ProportionScale(X, from_range = (0,100), inverse = False):
    scale = from_range[1] - from_range[0]
    if inverse:
        output = X*scale+from_range[0]
    else:
        output = (X-from_range[0])/scale
    return output

class ColumnSelector(BaseEstimator):
    def __init__(self, columns):
        self.columns = columns

    def fit(self, X, y = None):
        return self

    def transform(self, X, y=None):
        return X[self.columns]
    
class NumericNAOneHotEncoder(BaseEstimator):
    def __init__(self):
        pass
    
    def fit(self, X, y = None):
        return self
    
    def transform(self, X, y = None):
        for item in X.columns:
            X[item + "_isNA"] = X[item].apply(lambda x: 1 if pd.isna(x) else 0)
            X[item] = X[item].apply(lambda x: 0 if pd.isna(x) else x)
        return X.to_numpy()

class Printer(BaseEstimator):
    def __init__(self):
        pass

    def fit(self, X, y = None):
        return self
    
    def transform(self, X, y = None):
        print(X)
        return X

class BetaRegression(LinearRegression):

    ''' A fit-transform class extending a linear regression that performs a beta regression.
        Scale the response to have a specified range.
    '''

    def __init__(self, scale = 1, from_range = (0,1)):
        self.from_range = from_range
        self.scale = scale
        super().__init__()

    def fit(self, X, y = None):
        y = np.asarray(y)
        y = ProportionScale(y,from_range=self.from_range)
        y = np.log(y*self.scale / (1 - y*self.scale))
        return super().fit(X, y)

    def predict(self, X):
        y = super().predict(X)
        y = 1 / (np.exp(-y/self.scale) + 1)
        return ProportionScale(y,from_range=self.from_range,inverse=True)
