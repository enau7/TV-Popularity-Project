from shiny import App, render, reactive, ui, run_app

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
largest_folder = abs_path[:largest_folder_index]

tv_df_filename = largest_folder + "/Data/data/streaming_titles_final.csv"
score_df_filename = largest_folder + "/Data/data/director_scores.csv"
model_filename = largest_folder + "/Modeling/models/beta_regression.joblib"

tv_df = pd.read_csv(tv_df_filename)
score_df = pd.read_csv(score_df_filename)
dir_av_score_dict = dict(zip(score_df["director"],score_df["dir_average_score"]))
model = joblib.load(model_filename)

genres = tv_df.columns[tv_df.columns.str.startswith('genre.')]
directors = dir_av_score_dict.keys()
countries = supersplit(tv_df['country'])
pretty_genre = lambda x: x[6:].replace("_"," ")
genre_dict = dict(zip([pretty_genre(x) for x in genres],genres))

## STREAMLIT PORTION

import streamlit as st
'Would you like to make a Movie or TV Show?'
movie = st.checkbox('Movie')
show = st.checkbox('Show')

mediatype = None
if movie:
    mediatype = "Movie"
if show:
    mediatype = "Show"

if movie or show:
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
        'Select your cast members',
        ['Charlie Day', 'Alexandra Daddario','Tom Cruise', 'Jason Segel', 'Ryan Reynolds'])

        st.write('You selected:', cast_select)
    else:
                score_cast  = st.slider(
    "Average Score of the Cast?", 0, 100, 50)

