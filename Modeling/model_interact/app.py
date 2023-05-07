from shiny import App, render, reactive, ui, run_app

import pandas as pd
import joblib
import sklearn
import os

def truesum(iterable):
    print(iterable)
    if len(iterable) == 0:
        return None
    output = iterable[0]
    if len(iterable) == 1:
        return output
    for k in iterable[1:]:
        output += iterable
    return output

abs_path = os.path.dirname(__file__)
tvpop = "TV-Popularity-Project/"
largest_folder_index = abs_path.find(tvpop)+len(tvpop)
largest_folder = abs_path[:largest_folder_index]

tv_df_filename = largest_folder + "Data/data/streaming_titles_clean.csv"
lm_filename = largest_folder + "Modeling/models/linear_regression.joblib"

tv_df = pd.read_csv(tv_df_filename)
lm = joblib.load(lm_filename)

genres = tv_df.columns[tv_df.columns.str.startswith('genre.')]
directors = sorted(([print(str(k).split(", ")) for k in list(set(tv_df['director']))]))
countries = sorted([str(k) for k in list(set(tv_df['country']))])
pretty_genre = lambda x: x[6:].replace("_"," ")

app_ui = ui.page_fluid(
    ui.h1("Movie Builder and Evaluator"),
    ui.input_select(id = "genre",
                    label = "Select a genre:",
                    choices = {item: pretty_genre(item) for item in genres.sort_values()},
                    selectize=True
                    ),
    ui.input_checkbox(id = "dir_name_or_score",
                      label = "Select by director?"),
    ui.panel_conditional("! input.dir_name_or_score",
                         ui.input_numeric(id = "av_dir_score", 
                                          label = "Average Director Score",
                                          value = 50.0,
                                          min = 0.0,
                                          max = 100.0)),
    ui.panel_conditional("input.dir_name_or_score",
                         ui.input_select(id = "director", 
                                         label = "Director",
                                         choices = directors,
                                         selectize=True)),
    ui.input_select(id = "country",
                    label = "Select a release country:",
                    choices = countries,
                    selectize = True),
    ui.output_text_verbatim("txt"),
    ui.input_action_button(id = "stop",
                           label = "close app")
)


def server(input, output, session):
    @output
    @render.text
    def txt():
        model_input = tv_df.iloc[:0,:].copy()

        model_input.loc[0] = False
        try:
            model_input[input.genre()] = True
        except:
            return "An unexpected error occured."

        pred = lm.predict(model_input)[0]

        return f"Your movie has a predicted score of {round(pred,2)}."

    @reactive.Effect
    @reactive.event(input.stop)
    async def _():
        directors = [1,3,4]
        #await session.close()



app = App(app_ui, server)

if __name__ == "__main__":
    import os
    try:
        os.startfile("http://127.0.0.1:8000")
    except:
        os.system('open %s' % "http://127.0.0.1:8000")
    run_app()
    exit()