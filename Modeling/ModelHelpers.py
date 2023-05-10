import math
import numpy as np
from sklearn.linear_model import LinearRegression

def columnstartswith(columns, df):
    if type(columns) == str:
        columns = [columns]
    output = []
    for item in columns:
        output += list(df.columns[df.columns.str.startswith(item)])
    return output

class ColumnSelector():
    def __init__(self, columns, startswith = []):
        self.columns = columns
        self.startswith = startswith

    def fit(self, X, y = None):
        return self
    
    def transform(self, X):
        sw = columnstartswith(self.startswith, df = X)
        return X[self.columns + sw]
    
def ProportionScale(X, from_range = (0,100), inverse = False):
    scale = from_range[1] - from_range[0]
    if inverse:
        output = X*scale+from_range[0]
    else:
        output = (X-from_range[0])/scale
    return output

class BetaRegression(LinearRegression):

    ''' A fit-transform class extending a linear regression that performs a beta regression.
        Scale the response to have a specified range.
    '''

    def __init__(self, from_range = (0,1)):
        self.from_range = from_range
        super().__init__()

    def fit(self, X, y = None):
        y = np.asarray(y)
        y = ProportionScale(y,from_range=self.from_range)
        y = np.log(y / (1 - y))
        return super().fit(X, y)

    def predict(self, X):
        y = super().predict(X)
        y = 1 / (np.exp(-y) + 1)
        return ProportionScale(y,from_range=self.from_range,inverse=True)
