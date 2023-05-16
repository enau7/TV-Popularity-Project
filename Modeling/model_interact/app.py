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

app_ui = ui.page_fluid(
    ui.h1("Movie/Show Builder and Evaluator"),
    ui.input_select(id = "genre",
                    label = "Select a genre:",
                    choices = {item: pretty_genre(item) for item in genres.sort_values()},
                    selectize=True
                    ),
    ui.input_checkbox(id="isshow",
                    label = "Media type"),
    ui.output_text_verbatim("showtxt"),
    ui.input_checkbox(id = "by_director",
                      label = "Select by director?"),
    ui.panel_conditional("! input.by_director",
                         ui.input_slider(id = "av_dir_score", 
                                          label = "Average Director Score",
                                          value = 50.0,
                                          min = 0.0,
                                          max = 100.0)),
    ui.panel_conditional("input.by_director",
                         ui.input_select(id = "director", 
                                         label = "Director",
                                         choices = {x:x for x in directors},
                                         selectize=True)),
    ui.panel_conditional("input.by_director",
                         ui.output_text_verbatim("dirscore")),
    ui.input_select(id = "country",
                    label = "Select a release country:",
                    choices = countries,
                    selected = "United States",
                    selectize = True),
    ui.output_text_verbatim("txt"),
    ui.input_action_button(id = "stop",
                           label = "close app")
)


def server(input, output, session):
    @output
    @render.text
    def showtxt():
        if input.isshow():
            return "Selected: Show"
        return "Selected: Movie"
    
    @output
    @render.text
    def dirscore():
        return str(dir_av_score_dict[input.director()])
    
    @output
    @render.text
    def txt():
        model_input = tv_df[list(set(tv_df.columns).difference(set(["score"])))].loc[:0].copy()

        model_input["title"] = "My Movie"
        model_input["type"] = "Movie" if not input.isshow() else "TV Show"
        model_input["duration"] = np.nan
        model_input["cast_average_score"] = 50
        #model_input["rating"] =  np.nan
        model_input["country"] = np.nan
        model_input["release_year"] = 2023
        model_input[ModelHelpers.columnstartswith("genre",df=tv_df)] = False
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

        model_input[input.genre()] = True

        dirav = 0
        if not input.by_director():
            dirav = dir_av_score_dict[input.director()]
        else:
            dirav = input.av_dir_score()

        model_input["dir_average_score"] = 85

        pred = model.predict(model_input)[0]

        return f"Your movie has a predicted score of {round(pred,2)}."

    @reactive.Effect
    @reactive.event(input.stop)
    async def _():
        await session.close()



app = App(app_ui, server)

if __name__ == "__main__":
    import os
    try:
        os.startfile("http://127.0.0.1:8000")
    except:
        os.system('open %s' % "http://127.0.0.1:8000")
    run_app()
    exit()