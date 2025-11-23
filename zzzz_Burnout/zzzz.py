import pickle
import pandas as pd
from sklearn.preprocessing import LabelEncoder
X_val = pd.read_csv("test.csv")

X_val.drop(['Employee ID', 'Date of Joining', 'Date of Joining'], axis=1, inplace=True)

cat_features = ['Gender', 'Company Type', 'WFH Setup Available']
for cat in cat_features:
  le = LabelEncoder()
  X_val[cat] = le.fit_transform(X_val[cat])

model = pickle.load(open("model_file.pkl", "rb"))

y_preds = model.predict(X_val)

hmm = y_preds.argmax()


print(y_preds[:5])   # use slicing, not .head(), because y_preds is a NumPy array

X_val["predicted"] = y_preds
print(X_val.head())


print(X_val.iloc[hmm])