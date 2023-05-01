import pandas as pd
import joblib

tv_df = pd.read_csv(r"C:\Users\Colton\Documents\GitHub\TV-Popularity-Project\Data\data\streaming_titles_clean.csv")

lm = joblib.load(r"C:\Users\Colton\Documents\GitHub\TV-Popularity-Project\Modeling\models\linear_regression.joblib")

model_input = tv_df.iloc[:0,:].copy()

model_input.loc[0] = False
model_input["genre.Action"] = True
model_input.fillna(0)

print(lm.predict(model_input)[0])
