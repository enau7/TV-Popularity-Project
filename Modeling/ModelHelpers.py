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
    def __init__(self, select = None, na_include = []):
        self.select = select
        self.na_include = na_include
        pass
    
    def fit(self, X, y = None):
        return self
    
    def transform(self, X, y = None):
        a = self.select
        if self.select == None:
            a = X.columns
        for item in a:
            X.loc[:,item + "_isNA"] = X[item].apply(lambda x: 1 if pd.isna(x) or (x in self.na_include) else 0)
            X.loc[:,item] = X[item].apply(lambda x: 0 if pd.isna(x) or (x in self.na_include) else x)
        return X

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

if __name__ == "__main__":
    df = pd.DataFrame()
    df["Col1"] = [1,2,3,4,np.nan,5,6]
    print(NumericNAOneHotEncoder().transform(df))
    pass