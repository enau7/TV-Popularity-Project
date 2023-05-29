import streamlit as st

import pandas as pd
import numpy as np
import joblib
import sklearn
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import ModelHelpers

def flatten(arr):
    output = []
    for item in arr:
        for k in item:
            output.append(k)
    return output

def supersplit(arr, minlength = 4):
    output = [str(k).split(",") for k in list(set(arr))]
    output = flatten(output)
    output = [k for k in output if len(k) >= minlength]
    output = [k for k in output if k[0].isalpha()]
    output = sorted(output)
    return output

abs_path = os.path.dirname(__file__)#.replace("\\",'/')
tvpop = "TV-Popularity-Project"
largest_folder_index = abs_path.find(tvpop)+len(tvpop)
if abs_path.find(tvpop) == -1:
    largest_folder_index = abs_path.find(tvpop.lower())+len(tvpop)
largest_folder = abs_path[:largest_folder_index]

tv_df_filename = largest_folder + "/Data/data/streaming_titles_final.csv"
dir_score_df_filename = largest_folder + "/Data/data/director_scores.csv"
model_filename = largest_folder + "/Modeling/models/beta_regression.joblib"
cast_score_df_filename = largest_folder + "/Data/data/cast_scores.csv"

tv_df = pd.read_csv(tv_df_filename)
dir_score_df = pd.read_csv(dir_score_df_filename)
cast_score_df = pd.read_csv(cast_score_df_filename)
dir_av_score_dict = dict(zip(dir_score_df["director"],dir_score_df["dir_average_score"]))
cast_av_score_dict = dict(zip(cast_score_df["cast"],cast_score_df["cast_average_score"]))
model = joblib.load(model_filename)

st.write(model)

genres = tv_df.columns[tv_df.columns.str.startswith('genre.')]
directors = dir_av_score_dict.keys()
cast_members = cast_av_score_dict.keys()
countries = supersplit(tv_df['country'])
pretty_genre = lambda x: x[6:].replace("_"," ")
genre_dict = dict(zip([pretty_genre(x) for x in genres],genres))

# STREAMLIT PORTION

mediatype = st.radio(label = 'Would you like to make a Movie or TV Show?', options=["Movie","TV Show"])

option = st.selectbox(
'Select the genre of your {}.'.format(mediatype.lower()),
sorted(genre_dict.keys()))
'Would you like to assign a director or give an average score?'
director = st.checkbox('Director')
if director:
    dir_select = st.selectbox(
    'Select a Director',
    directors)
    st.write('You selected:', dir_select,'as your director')
else: 
    score_director  = st.slider(
"Average Score of the Director?", 0, 100, 50)
cast = st.checkbox('Cast')
if cast: 
    'Select your cast members.'
    cast_select = st.multiselect(
    'Select your cast members',cast_members)

    st.write('You selected:', cast_select)
else:
            score_cast  = st.slider(
"Average Score of the Cast?", 0, 100, 50)
            
## MODEL STUFF

model_input = tv_df[list(set(tv_df.columns).difference(set(["score"])))].loc[:0].copy()

# model_input["title"] = "My Movie"
# model_input["type"] = mediatype
# model_input["duration"] = np.nan
# model_input["cast_average_score"] = 50
# model_input["rating"] =  "NR"
# model_input["country"] = np.nan
# model_input["release_year"] = 2023
# model_input[ModelHelpers.columnstartswith("genre",df=tv_df)] = False
# return str(model_input[list(set(model_input.columns).difference(set(["title",
#                                                                      "type",
#                                                                      "dir_average_score",
#                                                                      "cast",
#                                                                      "Number_MoviesShows_dir",
#                                                                      "Number_MoviesShows_cast",
#                                                                      "director",
#                                                                      "rating",
#                                                                      "description",
#                                                                      "cast_average_score",
#                                                                      "imdbid",
#                                                                      "release_year",
#                                                                      "country",
#                                                                      "duration",
#                                                                      ]+ModelHelpers.columnstartswith("genre",df=tv_df))))])

# model_input[genre_dict[option]] = True

# dirav = 0
# if director:
#     dirav = dir_av_score_dict[dir_select]
# else:
#     dirav = score_director

# model_input["dir_average_score"] = dirav

pred = model.predict(model_input)[0]

st.write(f"Your movie has a predicted score of:")
st.header(round(pred,2))

