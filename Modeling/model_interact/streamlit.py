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
cast_score_df_filename = largest_folder + "/Data/data/cast_scores.csv"

tv_df = pd.read_csv(tv_df_filename)
dir_score_df = pd.read_csv(dir_score_df_filename)
cast_score_df = pd.read_csv(cast_score_df_filename)
dir_av_score_dict = dict(zip(dir_score_df["director"],dir_score_df["dir_average_score"]))
cast_av_score_dict = dict(zip(cast_score_df["cast"],cast_score_df["cast_average_score"]))


st.write(model)

genres = tv_df.columns[tv_df.columns.str.startswith('genre.')]
directors = dir_av_score_dict.keys()
cast_members = cast_av_score_dict.keys()
countries = supersplit(tv_df['country'])
pretty_genre = lambda x: x[6:].replace("_"," ")
genre_dict = dict(zip([pretty_genre(x) for x in genres],genres))

# STREAMLIT PORTION

mediatype = st.radio(label = 'Would you like to make a movie or tv show?', options=["Movie","TV Show"])

st.write('Select the genre of your {}.'.format(mediatype.lower()))

option = st.selectbox(
    'Genre of media:',
    sorted(genre_dict.keys()),
    label_visibility="hidden")

model_name = st.selectbox('Pick the Model:',
    ['beta_regression','decision_tree','knn','random_forest'])
'Would you like to assign a director or give an average score?'
director = st.checkbox('Director')
if director:
    dir_select = st.selectbox(
    'Select a Director',
    directors)
    score_director = dir_av_score_dict[dir_select]
    st.write('{} has an average score of {}.'.format(dir_select, round(score_director)))
else: 
    score_director  = st.slider(
"Average Score of the Director?", 0, 100, 50)
cast = st.checkbox('Cast')
if cast: 
    'Select your cast members.'

    cast_select = st.multiselect(
    'Select your cast members',cast_members, label_visibility='hidden')

    score_cast = np.mean([cast_av_score_dict[k] for k in cast_select])
    
    st.write('{} have an average score of {}'.format(cast_select,score_cast))
else:
    score_cast  = st.slider(
"Average Score of the Cast?", 0, 100, 50)
    
advanced = st.checkbox("Advanced options")

rating = "PG-13"
country = "United States"
duration = np.nan
year = 2023

if advanced:
    rating = st.selectbox("Select the audience rating:",
                 sorted(list(set(tv_df["rating"]).difference(set([np.nan]))))
    )
    country = st.selectbox("Select the country of production:",
                 sorted(list(set(tv_df["country"]).difference(set([np.nan]))))
    )
    if mediatype == "Movie":
        duration = st.slider("Choose the duration of the movie:", min_value = 10, max_value = 180, value = 90, step = 1)
    else:
        duration = st.number_input("Choose the number of seasons for the show:", min_value = 1, max_value = 15, value = 1, step = 1)
            
    year = st.slider("Choose the release year:", min_value = 1900, max_value = 2050, value = 2023, step = 1)
## MODEL STUFF

model_input = tv_df[list(set(tv_df.columns).difference(set(["score"])))].loc[:0].copy()

model_input["title"] = "My Movie"
model_input["type"] = mediatype
model_input["duration"] = duration
model_input["cast_average_score"] = score_cast
model_input["dir_average_score"] = score_director
model_input["rating"] = rating
model_input["country"] = country
model_input["release_year"] = year
model_input[ModelHelpers.columnstartswith("genre",df=tv_df)] = False
model_input[genre_dict[option]] = True
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
model_filename = largest_folder + "/Modeling/models/{}.joblib".format(model_name)
model = joblib.load(largest_folder + model_filename)
pred = model.predict(model_input)[0]

st.write(f"Your {mediatype.lower()} has a predicted score of:")
st.header(round(pred,2))

