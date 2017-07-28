from sklearn.ensemble import RandomForestClassifier
from os import listdir
from os.path import isfile, join
from os import listdir
from os.path import isfile, join
import itertools
from sklearn import preprocessing
import numpy as np
from sklearn.preprocessing import OneHotEncoder

def foo(x):
    ar = x.split(",")
    if ar[2].strip() == 'pos':
        return 1
    return 0

def pris(x):
    ar = x.split(",")
    return [ar[0].strip(), ar[1].strip()]

def module_check(test_path, train_path, treshhold):
    mypath = test_path
    onlyfiles2 = [f for f in listdir(mypath) if isfile(join(mypath, f)) and str(f)[-8:] == "opin.txt"]
    mypath = train_path
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f)) and str(f)[-8:] == "opin.txt"]
    lines2 = []
    for file in onlyfiles2:
        lines2.extend(line.rstrip('\n') for line in open('test/' + file) if len(line.rstrip('\n')) > 2)
    lines = []
    for file in onlyfiles:
        lines.extend(line.rstrip('\n') for line in open('train/' + file) if len(line.rstrip('\n')) > 2)
    y = list(map(foo, lines))
    data = list(map(pris, lines))
    y_test = list(map(foo, lines2))
    data_test = list(map(pris, lines2))
    array2 = list(itertools.chain(*data))
    array2_test = list(itertools.chain(*data_test))
    le = preprocessing.LabelEncoder()
    le.fit(array2 + array2_test)
    a = le.transform(array2)
    a_test = le.transform(array2_test)
    data = np.array(a).reshape(-1, 2)
    data_test = np.array(a_test).reshape(-1, 2)
    enc = OneHotEncoder()
    enc.fit(np.vstack((data, data_test)))
    data = enc.transform(data).toarray()
    data_test = enc.transform(data_test).toarray()
    model = RandomForestClassifier(n_estimators=50)
    model.fit(data, y)    #, cv=3, scoring='accuracy').mean()
    Array = []
    for name in array2_test:
        Array.append(name not in array2)
    ind_not_inc = (np.array(Array).reshape((-1, 2))[:, 1] + np.array(Array).reshape((-1, 2))[:, 0])
    ind = (np.abs(model.predict_proba(data_test)[:, 0] - model.predict_proba(data_test)[:, 1]) > treshhold)*(model.predict(data_test) != y_test)
    return ind*ind_not_inc
