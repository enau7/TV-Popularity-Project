from shiny import App, render, ui, run_app

import pandas as pd
import joblib
import sklearn
import os

abs_path = os.path.dirname(__file__)
tvpop = "TV-Popularity-Project/"
largest_folder_index = abs_path.find(tvpop)+len(tvpop)
largest_folder = abs_path[:largest_folder_index]


tv_df_filename = largest_folder + "Data/data/streaming_titles_clean.csv"
lm_filename = largest_folder + "Modeling/models/linear_regression.joblib"

tv_df = pd.read_csv(tv_df_filename)
lm = joblib.load(lm_filename)

genres = tv_df.columns[tv_df.columns.str.startswith('genre.')]
pretty_genre = lambda x: x[6:].replace("_"," ")

app_ui = ui.page_fluid(
    ui.input_select(id = "genre",
                    label = "Select a genre to be evaluated:",
                    choices = {item: pretty_genre(item) for item in genres.sort_values()}
                    ),
    ui.output_text_verbatim("txt"),
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

        return f"{pretty_genre(input.genre())} titles are predicted to have a score of {round(pred,2)}."


app = App(app_ui, server)

if __name__ == "__main__":
    import os
    os.startfile("http://127.0.0.1:8000")
    run_app()
    exit()